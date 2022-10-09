from datetime import datetime

# disk = psutil.disk_io_counters()
# read: float = disk.read_bytes
# time: int = disk.read_time/1000
# read_per_sec: float = read/time
# print(read_per_sec)
# host = "192.168.98.130"
# net_if = psutil.net_if_addrs()
# net_if_target = ""
# for key, value in net_if.items():
#     for snic in value:
#         if snic.address == host:
#             net_if_target = key
#             break
#     if net_if_target != "":
#         break

# print(net_if_target)
# print(psutil.net_io_counters(pernic=True)[net_if_target])

print(datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
