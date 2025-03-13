# export disk info from json to csv

import csv
import datetime
import json
import re
from pathlib import Path

ENCODING = "utf-8"
LOGGING_TIME_FORMAT = "%Y-%m-%d %H:%M:%S"


# CSV_HEADER: datetime,host_ip,read_count,write_count,read_bytes,write_bytes,read_time,write_time

def timestamp2datetime(timestamp: int) -> str:
    return datetime.datetime.fromtimestamp(timestamp / 1000).strftime(LOGGING_TIME_FORMAT)


def get_ip_from_filename(filename: str) -> str:
    """
    Get IP from file name
    :param filename: data_192.168.98.95.json.txt
    :return: 192.168.98.95
    """
    return re.search(r"\d.*\d", filename).group()


def write_csv(data: list):
    with open("data_csv/data.csv", "+a", encoding=ENCODING, newline="") as f:
        csv_writer = csv.writer(f)
        csv_writer.writerows(data)


def txt2list(file_path: Path) -> list:
    data = list()
    with open(file_path, "r", encoding=ENCODING) as f:
        lines = f.readlines()
        for line in lines:
            data.append(json.loads(line.strip()))
    return data
    # host_ip = get_ip_from_filename(file_path.name)
    # print(host_ip)
    # print(data[0]["data"]["disk"]["overall"])


def save_data(data_lst: list, file_path: Path):
    data_father = list()
    for d in data_lst:
        data_child = list()
        data_child.append(timestamp2datetime(d["header"]["generatedOn"]))
        data_child.append(get_ip_from_filename(file_path.name))
        disk_overall = d["data"]["disk"]["overall"]
        data_child.append(disk_overall["read_count"])
        data_child.append(disk_overall["write_count"])
        data_child.append(disk_overall["read_bytes"])
        data_child.append(disk_overall["write_bytes"])
        data_child.append(disk_overall["read_time"])
        data_child.append(disk_overall["write_time"])
        data_father.append(data_child)
    write_csv(data_father)


if __name__ == "__main__":
    path = Path('./data_json')
    for json_dir in path.iterdir():
        print(f"Get: {json_dir.name}")
        sub_path = Path(json_dir)
        for sub_json_dir in sub_path.iterdir():
            print(f"Read: {sub_json_dir.name}")
            data_list = txt2list(sub_json_dir)
            print(f"Save: {sub_json_dir.name}")
            save_data(data_list, sub_json_dir)
