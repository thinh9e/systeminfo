# systeminfo

Send system information in an HTTP request

## Build

```shell
pyinstaller --onefile server.py
pyinstaller --onefile client.py
```

## Run

1. Rename file `hosts_exp.txt` to `hosts.txt` and enter the host's IP line by line.
2. Run the `server.exe` file on the machine to be monitored.
3. Run the `client.exe` file to get the system info.
4. The raw data will be stored in the `data_json` folder, and the short data will be stored in the `data_csv` folder.

## Requirements

- Python >= 3.6
- psutil == 5.9.2
- pyinstaller == 4.10
- schedule == 1.1.0
