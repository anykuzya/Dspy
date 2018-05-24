from collections import deque
import requests
from flask import Flask, request, send_file, jsonify

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


@app.route("/")
def main_page():
    return send_file('index.html')


@app.route("/messages", methods=['GET'])
def getMessages():
    messages = [{"from": x[0], "to": x[1], "messages": list(queues[x])} for x in queues]
    return jsonify({"responce": messages})

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
        if (queues):
            earliest_key = list(queues.keys())[0]
            earliest_counter = message_counter
            for key in queues:
                q = queues[key]
                if (q):
                    msg = dq_at(q, 0)
                    if msg and earliest_counter > msg[0]:
                        earliest_counter = msg[0]
                        earliest_key = key
            q = queues[earliest_key]
            if (q):
                earliest_msg = q.popleft()[1]
                deliverMessage(earliest_msg["payload"], earliest_msg["from"], earliest_msg["to"])
                n -= 1
            else:
                break
        else:
            break
    return getMessages()


@app.route("/messages/deliver/each_pair/<n>", methods=['POST'])
def deliverN_each_pair(n):
    pass


@app.route("/messages/drop/<id>", methods=['POST'])
def removeMessage(id):
    pass


@app.route("/messages/reorder/<id1>_<id2>", methods=['POST'])
def reorderMessage(id1, id2):
    pass

if __name__ == '__main__':
    app.run()

