

class Lamport_mutex:
    def __init__(self, network_manager):
        self.tick = 0
        self.network_manager = network_manager

    def recieve(self, message):
        print(message)

    def test(self):
        self.network_manager.send(self, '{"hello": "world"}')