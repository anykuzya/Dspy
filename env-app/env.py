from collections import deque
import requests
import http.client
from heapq import heappush
from flask import Flask, request
app = Flask(__name__)

"""
Что нужно сделать:
    * добавить глобальный счетчик, чтобы по нему упорядочивать все сообщения, которые нас попросили доставить
    * добавить переменную, в которой хранить очереди сообщений. Хранить как словарь (from, to) -> <очередь сообщений>
    * написать код, котодый будет в addMessage: парсить пришедший json,
        * заводить, при необходимости, очереди, с его участием (участием его адресата)
        * класть сообщение в очередь 
    * погуглить, как отправлять http в python
"""
message_counter = 0
known_execs = set()
queues = {}
to_be_delivered = []

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

# @app.route("/messages/<id>/deliver", methods=['POST'])
# def deliverOne(id):
#     pass

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
    while True:
        if len(to_be_delivered) >= n:
            break
        for key in queues:
            q = queues[key]
            if q:
                heappush(to_be_delivered, q.popleft())

    for msg in to_be_delivered:
        if n == 0:
            break
        data = msg[1]
        deliverMessage(data["payload"], data["from"], data["to"])
        n -= 1


if __name__ == '__main__':
    app.run()

