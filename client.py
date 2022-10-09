import concurrent.futures
import csv
import http.client
import json
from datetime import datetime
from pathlib import Path
from time import sleep
from typing import Union

import schedule

ENCODING = "utf-8"
LOGGING_TIME_FORMAT = "%Y-%m-%d %H:%M:%S"


def log_console(msg: str) -> None:
    print(f"{datetime.now().strftime(LOGGING_TIME_FORMAT)} - {msg}")


class SystemConn:
    PORT = 9090
    METHOD = "GET"
    PATH = "/systeminfo"

    def __init__(self) -> None:
        self.__host = ""
        self.__conn = None
        self.__resp = None

    def request(self, host: str) -> None:
        self.__host = host
        try:
            self.__conn = http.client.HTTPConnection(self.__host, self.PORT)
            self.__conn.request(self.METHOD, self.PATH)
            self.__resp = self.__conn.getresponse()
        except Exception as exp:
            log_console(f"HTTPConnection error: Host: {host} - {exp}")
        finally:
            self.close()

    def close(self) -> None:
        if self.__conn is not None:
            self.__conn.close()

    def resp_json(self) -> dict:
        data = dict()
        if self.__resp is not None:
            data_str = self.__resp.read().decode(ENCODING).replace("\'", "\"")
            data = json.loads(data_str)
        return data


class FileHandler:
    CSV_DATA_DIR = "data_csv"
    CSV_HEADER = ("datetime", "host_ip", "cpu", "mem_vir", "mem_swap")
    JSON_DATA_DIR = "data_json"
    DIR_TIME_FORMAT = "%Y%m%d"

    def __init__(self) -> None:
        Path(self.CSV_DATA_DIR).mkdir(parents=True, exist_ok=True)
        Path(self.JSON_DATA_DIR).mkdir(parents=True, exist_ok=True)
        self.__active_date = datetime.now().strftime(self.DIR_TIME_FORMAT)
        self.__hostname = ""
        self.__csv_file = None
        self.__csv_writer = None

    @staticmethod
    def __is_exist_file(path: str) -> bool:
        filepath = Path(f"{path}")
        return filepath.exists()

    def check_active_date(self) -> None:
        """"Check and update active date"""
        current_date = datetime.now().strftime(self.DIR_TIME_FORMAT)
        if self.__active_date != current_date:
            self.__active_date = current_date

    def csv_add_header(self) -> None:
        self.csv_writerow(self.CSV_HEADER)

    def set_hostname(self, hostname: str) -> None:
        self.__hostname = hostname

    def csv_writer(self) -> None:
        self.check_active_date()
        csv_filename = f"data_{self.__active_date}.csv"

        is_add_header = False
        if not self.__is_exist_file(f"{self.CSV_DATA_DIR}/{csv_filename}"):
            is_add_header = True

        self.__csv_file = open(f"{self.CSV_DATA_DIR}/{csv_filename}", "+a", encoding=ENCODING, newline="")
        self.__csv_writer = csv.writer(self.__csv_file)

        if is_add_header:
            self.csv_add_header()

    def csv_writerow(self, rowdata: Union[list, tuple]) -> None:
        if self.__csv_writer is not None:
            self.__csv_writer.writerow(rowdata)

    def csv_close(self) -> None:
        if self.__csv_file is not None:
            self.__csv_file.close()

    def json_save_raw(self, data: dict) -> None:
        json_data_path = f"{self.JSON_DATA_DIR}/{self.__active_date}"
        Path(json_data_path).mkdir(parents=True, exist_ok=True)
        json_filename = f"data_{self.__hostname}.json.txt"
        with open(f"{json_data_path}/{json_filename}", "+a", encoding=ENCODING) as json_file:
            # minified json
            json.dump(data, json_file, separators=(",", ":"))
            json_file.write("\n")


def load_hosts() -> list:
    try:
        with open("hosts.txt", "r", encoding=ENCODING) as hosts_file:
            return hosts_file.read().splitlines()
    except FileNotFoundError as exp:
        log_console(f"FileNotFoundError error: {exp}")
        exit(1)


def get_data(host: str) -> dict:
    log_console(f"Get data from host: {host}")
    sysconn = SystemConn()
    sysconn.request(host)
    return sysconn.resp_json()


def save_data(handler: FileHandler) -> None:
    hosts = load_hosts()
    time_current = datetime.now().strftime(LOGGING_TIME_FORMAT)
    handler.csv_writer()
    with concurrent.futures.ThreadPoolExecutor(max_workers=5) as executor:
        for host, json_data in zip(hosts, executor.map(get_data, hosts)):
            data = list()
            if json_data != {}:
                data.append(time_current)
                data.append(host)
                data.append(json_data["data"]["cpu"]["overall"])
                data.append(json_data["data"]["memory"]["virtual"]["percent"])
                data.append(json_data["data"]["memory"]["swap"]["percent"])
                log_console(f"Save data for host: {host}")
                handler.set_hostname(host)
                handler.csv_writerow(data)
                handler.json_save_raw(json_data)
    handler.csv_close()


if __name__ == "__main__":
    file_handler = FileHandler()
    schedule.every(5).minutes.do(save_data, file_handler)

    try:
        log_console("Start client")
        while True:
            schedule.run_pending()
            sleep(1)
    except KeyboardInterrupt as ex:
        log_console("KeyboardInterrupt")
    finally:
        log_console("Stop client")
        file_handler.csv_close()
