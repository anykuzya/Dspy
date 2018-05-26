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


def listMessages():
    return [{"from": x[0], "to": x[1], "messages": list(queues[x])} for x in queues]

@app.route("/messages", methods=['GET'])
def getMessages():
    return jsonify({"messages": listMessages()})

def dq_at(dq, i):
    for e in dq:
        if i == 0:
            return e
        else:
            i -= 1
    return None


def deliverMessage(msg, sender, reciever):
    requests.post(reciever, json=msg)

def findByIdAndKey(id, key):
    try:
        q = queues[key]
        for msg in q:
            if msg[0] == id:
                return msg
    except():
        return None

#returns Key in queues and pair (id, msg)
def findById(id):
    if (queues):
        id = int(id)
        for key in queues:
            res = findByIdAndKey(id, key)
            if res is not None:
                return res, key

    print("no message with {}".format(id))
    return None, None


@app.route("/messages/deliver/<n>", methods=['POST'])
def deliverN(n):
    n = int(n)
    delivered = 0
    while delivered < n:
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
                id, earliest_msg = q.popleft()
                try:
                    deliverMessage(earliest_msg["payload"], earliest_msg["from"], earliest_msg["to"])
                    delivered += 1
                except:
                    q.appendleft((id, earliest_msg))
                    d_error = "deliver failed on message {}".format(id)
                    print(d_error)
                    return jsonify({"messages": listMessages(), "delivered": d_error})
            else:
                break
        else:
            break
    return jsonify({"messages": listMessages(), "delivered": "delivered {} out of {} messages".format(delivered, n)})


@app.route("/messages/deliver/one/<id>", methods=['POST'])
def deliverOne(id):
    pass


@app.route("/messages/deliver/each_pair/<n>", methods=['POST'])
def deliverN_each_pair(n):
    pass


@app.route("/messages/drop/<id>", methods=['POST'])
def removeMessage(id):
    msg, key = findById(id)
    queues[key].remove(msg)
    return jsonify({"messages": listMessages()})


@app.route("/messages/reorder/<id1>_<id2>", methods=['POST'])
def reorderMessage(id1, id2):
    pass

if __name__ == '__main__':
    app.run()

