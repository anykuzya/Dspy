from collections import deque
import requests
from flask import Flask, request
app = Flask(__name__)

message_counter = 0
known_execs = set()
queues = {}

@app.route("/messages", methods=['POST'])
def addMessage():
    global message_counter
    json = request.get_json()
    sender = json["from"]
    reciever = json["to"]
    for e in [sender, reciever]:
        if not e in known_execs:
            for known_exec in known_execs:
                queues[(e, known_exec)] = deque()
                queues[(known_exec, e)] = deque()
            known_execs.add(e)
    queues[(sender, reciever)].append((message_counter, json))
    message_counter += 1
    return "200"


@app.route("/messages", methods=['GET'])
def getMessages():
    pass

def dq_at(dq, i):
    for e in dq:
        if i == 0:
            return e
        else:
            i -= 1
    return None

def deliverMessage(msg, sender, reciever):
    requests.post(reciever, msg)

@app.route("/messages/deliver/<n>", methods=['POST'])
def deliverN(n):
    n = int(n)
    while n > 0:
        earliest_counter = message_counter
        earliest_msg = {}
        for key in queues:
            q = queues[key]
            msg = dq_at(q, 0)
            if msg and earliest_counter > msg[0]:
                earliest_counter = msg[0]
                earliest_msg = msg[1]
        deliverMessage(earliest_msg["payload"], earliest_msg["from"], earliest_msg["to"])
        n -= 1
    return "200"

if __name__ == '__main__':
    app.run()

