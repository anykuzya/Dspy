#!/usr/bin/env python3
from network_manager import NetworkManager

LOCK = "LOCK"
UNLOCK = "UNLOCK"

if __name__ == '__main__':
    nm = NetworkManager()
    while True:
        command, id = input("try LOCK or UNLOCK by some ID:").split()
        id = int(id)
        nm.executors[id].do_request() if command == LOCK else nm.executors[id].do_releaset()
        print("handled")
