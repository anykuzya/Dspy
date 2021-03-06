from queue import Queue
import json
from _heapq import heappush
from threading import Thread
# from threading import Thread

REQUEST = "request"
RELEASE = "release"
ACK = "ack"

class LamportMutex:
    def __init__(self, network_manager, n, id):
        self.id = id
        self.tick = 0
        self.ids = [k for k in range(0, n) if k != id]
        self.messages_queue = Queue()
        self.requests_queue = []
        self.network_manager = network_manager
        self.waiting_acknowledgments_from = []
        self.is_granted = False

        def handle_messages_loop():
            while True:
                self.handle_message()
        t = Thread(target=handle_messages_loop)
        t.setDaemon(True)
        t.start()

    def do_request(self):
        if self.is_granted:
            print("lock has been acquired already")
            return

        self.tick += 1
        message = {"time": self.tick, "from": self.id, "type": REQUEST}
        self.put_to_request_queue(self.tick, self.id)
        self.send(message)
        self.waiting_acknowledgments_from = {id for id in self.ids}
        # wait for acknowledges and our mes is first in reqQueue
        while (not (len(self.waiting_acknowledgments_from) == 0
               and self.requests_queue[0][1] == self.id)):
            pass
            # self.handle_message()
        self.waiting_acknowledgments_from = None
        self.is_granted = True
        print("you have been granted with the resource at", self.tick)

    def do_release(self):
        if not self.is_granted:
            print("lock hasn't been acquired yet")
            return

        self.tick += 1
        message = {"time": self.tick, "from": self.id, "type": RELEASE}
        self.delete_from_requests_queue(self.id)
        self.is_granted = False
        self.send(message)
        print("you have released the resource at", self.tick)


    def handle_request(self, message):
        self.put_to_request_queue(message["time"], message["from"])
        answer = {"time": self.tick, "from": self.id, "type": ACK}
        self.send(answer, message["from"])

    def handle_release(self, message):
        self.delete_from_requests_queue(message["from"])

    def handle_ack(self, message):
        self.waiting_acknowledgments_from.remove(message["from"])

    def handle_message(self):
        message = self.messages_queue.get()
        self.tick = max(self.tick, message["time"]) + 1
        if message["type"] == REQUEST:
            self.handle_request(message)
        elif message["type"] == RELEASE:
            self.handle_release(message)
        elif message["type"] == ACK:
            self.handle_ack(message)
        self.messages_queue.task_done()

    def put_to_request_queue(self, time, id):
        heappush(self.requests_queue, [time, id])

    def delete_from_requests_queue(self, id):
        for time, rid in self.requests_queue:
            if rid == id:
                self.requests_queue.remove([time, rid])

    def receive(self, message):
        self.messages_queue.put(message)

    def send(self, message, to="all"):
        if to == "all":
            for id in self.ids:
                if id != self.id:
                    self.network_manager.send(message, self.id, id)
        else:
            self.network_manager.send(message, self.id, to)
