import json
from LM import Lamport_mutex

class Network_manager:
    def __init__(self):
        with open("config.json") as config_file:
            config = json.load(config_file)


            addresses = config["executors"]
            n = len(addresses)

            self.executors = {}
            for i in range(n):
                executor = Lamport_mutex(self, i, n)
                self.executors[executor] = addresses[i]

    # there is a dummy implementation without real network usage and thread per executor
    # it'll be modified later, step-by-step
    def send(self, executor, message, reciever="all"):
        for e in self.executors:
            address = self.executors[e]
            if address == reciever or reciever == "all":
                e.receive(message)
        print(message)
        print("from", self.executors[executor])
