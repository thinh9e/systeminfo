import socket
from typing import NamedTuple

import psutil


class SystemInfo:
    def __init__(self) -> None:
        pass

    @staticmethod
    def __convert_type(data: NamedTuple) -> dict:
        """
        Convert NamedTuple type to dict
        :param data: NamedTuple data
        :return: dict data
        """
        data_dict = dict(data._asdict())
        return data_dict

    @staticmethod
    def __get_local_ip() -> str:
        ip = ""
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        try:
            s.connect(("192.168.255.255", 1))
            ip = s.getsockname()[0]
        except socket.error as ex:
            print(f"Get local IP error: {ex}")
        return ip

    @staticmethod
    def cpu(interval: int = 1) -> dict:
        cpu_data = dict()
        cpu_data["overall"] = psutil.cpu_percent(interval=interval)
        cpu_data["percpu"] = psutil.cpu_percent(interval=interval, percpu=True)
        return {"cpu": cpu_data}

    def memory(self) -> dict:
        memory_data = dict()
        memory_data["virtual"] = self.__convert_type(psutil.virtual_memory())
        memory_data["swap"] = self.__convert_type(psutil.swap_memory())
        return {"memory": memory_data}

    def disk(self) -> dict:
        disk_data = dict()
        disk_data["overall"] = self.__convert_type(psutil.disk_io_counters(perdisk=False))

        perdisk_data = dict()
        perdisk_rawdata = psutil.disk_io_counters(perdisk=True)
        for key, value in perdisk_rawdata.items():
            perdisk_data[key] = self.__convert_type(value)
        disk_data["perdisk"] = perdisk_data

        return {"disk": disk_data}

    def network(self) -> dict:
        network_data = dict()
        network_rawdata = psutil.net_io_counters(pernic=True)

        ip = self.__get_local_ip()
        net_if = psutil.net_if_addrs()
        net_if_target = ""
        for inf, snics in net_if.items():
            for snic in snics:
                if snic.address == ip:
                    net_if_target = inf
                    break
            if net_if_target != "":
                break

        network_data["target"] = dict()
        if net_if_target != "":
            network_data["target"] = self.__convert_type(network_rawdata[net_if_target])
        network_data["pernet"] = dict()
        for key, value in network_rawdata.items():
            network_data["pernet"][key] = self.__convert_type(value)
        return {"network": network_data}

    def all(self) -> dict:
        data = dict(**self.cpu(), **self.memory(), **self.disk(), **self.network())
        return data


if __name__ == "__main__":
    print(SystemInfo().all())
