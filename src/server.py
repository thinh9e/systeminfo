import json
from datetime import datetime
from http.server import BaseHTTPRequestHandler, HTTPServer
from time import time

from systeminfo import SystemInfo

ENCODING = "utf-8"
LOGGING_TIME_FORMAT = "%Y-%m-%d %H:%M:%S"


def log_console(msg: str) -> None:
    print(f"{datetime.now().strftime(LOGGING_TIME_FORMAT)} - {msg}")


class ServerHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        if self.path == "/systeminfo":
            self.send_response(200)
            self.send_header("Content-Type", "application/json")
            self.end_headers()
            data = json.dumps(self.formatter(SystemInfo().all()))
            self.wfile.write(data.encode(ENCODING))
        else:
            self.send_error(404, "Page not found")

    @staticmethod
    def formatter(data_raw: dict) -> dict:
        data = dict()
        data["header"] = {}
        data["header"]["generatedOn"] = int(time() * 1000)
        data["data"] = data_raw
        return data


class Server:
    IP = "0.0.0.0"
    PORT = 9090

    def __init__(self) -> None:
        self.server_address = (self.IP, self.PORT)
        self.httpd = None

    def run(self):
        try:
            self.httpd = HTTPServer(self.server_address, ServerHandler)
        except OSError as exp:
            log_console(f"Cannot start server: {exp}")
            exit(1)

        if self.httpd is not None:
            try:
                log_console("Start server")
                self.httpd.serve_forever()
            except KeyboardInterrupt:
                log_console("KeyboardInterrupt")
            finally:
                log_console("Stop server")
                self.httpd.server_close()


if __name__ == "__main__":
    Server().run()
