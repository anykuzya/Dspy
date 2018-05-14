import json
from LM import Lamport_mutex

class Network_manager:
    def __init__(self):
        with open("config.json") as config_file:
            config = json.load(config_file)
            self.executors = {}
            for address in config["executors"]:
                executor = Lamport_mutex(self)
                self.executors[executor] = address

    def send(self, executor, message):
        print(message)
        print(self.executors[executor])


    def test(self):
        for e in self.executors:
            address = self.executors[e]
            e.recieve(json.JSONEncoder().encode({"hi": "hello", "address": address}))
            e.test()
