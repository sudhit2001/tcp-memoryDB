import socket
import os

replica_sockets = []

def connect_replicas():
    global replica_sockets

    replica_sockets.clear()

    replicas = os.getenv("REPLICAS")

    if not replicas:
        return

    replicas = replicas.split(",")

    for replica in replicas:

        host, port = replica.split(":")

        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        s.connect((host, int(port)))

        replica_sockets.append(s)

        print(f"Connected to {host}:{port}")

def replicate(message):
    for replica in replica_sockets:
        replica.sendall(message.encode())
