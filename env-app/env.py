from collections import deque

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
    msg = json["payload"]
    queues[(sender, reciever)].append((msg, message_counter))
    message_counter += 1
    print(known_execs)
    print(queues)
    return "200"


@app.route("/messages", methods=['GET'])
def getMessages():
    pass

# @app.route("/messages/<id>/deliver", methods=['POST'])
# def deliverOne(id):
#     pass


@app.route("/messages/deliver", methods=['POST'])
def deliverAll():
    pass


if __name__ == '__main__':
    app.run()

