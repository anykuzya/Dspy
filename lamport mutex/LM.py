from queue import Queue

# from threading import Thread

REQUEST = "request"
RELEASE = "release"
ACK = "ack"

class Lamport_mutex:
    def __init__(self, network_manager, n, id):
        self.id = id
        self.tick = 0
        self.ids = [k for k in range(0, n) if k != id]
        self.messages_queue = Queue()
        self.requests_queue = []
        self.network_manager = network_manager
        self.waiting_acknowledgments_from = []
        self.is_granted = False

    def do_request(self):
        pass

    def do_release(self):
        pass

    def handle_request(self, message):
        pass

    def handle_release(self, message):
        pass

    def handle_ack(self, message):
        pass

    def handle_message(self, message):
        if message["type"] == REQUEST:
            self.handle_request(message)
        elif message["type"] == RELEASE:
            self.handle_release(message)
        elif message["type"] == ACK:
            self.handle_ack(message)

    def receive(self, message):
        self.handle_message(message)

    def send_to_all(self, message):
        self.network_manager.send(self, message)

    def send_to_one(self, message, to):
        self.network_manager.send(self, message, to)
