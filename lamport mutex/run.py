#!/usr/bin/env python3
import sys
import json
from LM import LamportMutex
import requests
from threading import Thread

from flask import Flask, request


LOCK = "LOCK"
UNLOCK = "UNLOCK"

host_prefix = "http://127.0.0.1:"
app = Flask(__name__)


@app.route("/", methods=["POST"])
def recv():
    message = request.get_json()
    nm.executor.receive(message)
    return "200"

class NetworkManager:
    def __init__(self, id):
        port = None
        with open("config.json") as config_file:
            config = json.load(config_file)
            ports = config["executors"]
            port = ports[id]
            self.addresses = [host_prefix + p for p in ports]
        def run_listener():
            app.run("localhost", int(port))

        t = Thread(target=run_listener)
        t.setDaemon(True)
        t.start()

        n = len(self.addresses)
        self.executor = LamportMutex(self, n, id)

    def send(self, message, receiver):
        url = self.addresses[receiver]
        requests.post(url, json=message)

if __name__ == '__main__':
    id = sys.argv[1]
    nm = NetworkManager(int(id))
    while True:
        command = input("try LOCK or UNLOCK:")
        nm.executor.do_request() if command == LOCK else nm.executor.do_release()
        print("handled")

