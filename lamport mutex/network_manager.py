import json
from LM import LamportMutex


class NetworkManager:
    def __init__(self):
        with open("config.json") as config_file:
            config = json.load(config_file)
            self.addresses = config["executors"]

        n = len(self.addresses)
        self.executors = [LamportMutex(self, n, i) for i in range(n)]

    # there is a dummy implementation without real network usage and thread per executor
    # it'll be modified later, step-by-step
    def send(self, message, receiver):
        self.executors[receiver].receive(message)
