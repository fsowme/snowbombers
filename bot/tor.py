import os
from time import sleep

import requests
from dotenv import load_dotenv
from stem import Signal
from stem.control import Controller

load_dotenv()

PASSWORD = os.getenv("TOR_PASSWORD")
PROXIES = {
    "http": "socks5h://localhost:9050",
    "https": "socks5h://localhost:9050",
}


class ConnectionManager:
    def __init__(self):
        self.new_ip = "0.0.0.0"
        self.old_ip = "0.0.0.0"
        # self.new_identity()

    @classmethod
    def _get_connection(self):
        with Controller.from_port(port=9051) as controller:
            controller.authenticate(password=PASSWORD)
            controller.signal(Signal.NEWNYM)
            controller.close()

    @classmethod
    def request(self, url, headers=None, proxies=None):
        headers = {} if headers is None else headers
        proxies = PROXIES if proxies is None else proxies
        response = requests.get(url, headers=headers, proxies=proxies)
        return response

    def new_identity(self):
        if self.new_ip == "0.0.0.0":
            self._get_connection()
            self.new_ip = self.request("http://icanhazip.com/").text
        else:
            self.old_ip = self.new_ip
            self._get_connection()
            self.new_ip = self.request("http://icanhazip.com/").text

        seg = 0

        while self.old_ip == self.new_ip:
            sleep(5)
            seg += 5
            print("Waiting to obtain new IP: %s Seconds" % seg)
            self.new_ip = self.request("http://icanhazip.com/").text

        print("New connection with IP: %s" % self.new_ip)
