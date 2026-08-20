import socket
import threading
from protocol.codec import decode, encode
from protocol.parser import parse
from executor import execute
from storage.wal import recover
from storage.snapshot import load_snapshot
from database import store
from replication.client import connect_replicas
from election.sender import start_heartbeat
from election.watchdog import start_watchdog
import cluster.state as state

import os

state.ROLE = os.getenv("ROLE", "primary")
PORT = int(os.getenv("PORT", 5000))
HOST = "0.0.0.0"

print(f"Starting {state.ROLE} server on port {PORT}")

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind((HOST, PORT))
server.listen(5)

print("Loading snapshot...")

snapshot = load_snapshot()

store.load(snapshot)

print("Snapshot loaded.")

print("Recovering database...")

commands = recover()

for message in commands:
    command = parse(message)
    execute(command, recovery=True)

print("Recovery complete.")

if state.ROLE == "primary":
    connect_replicas()
    start_heartbeat()
else:
    start_watchdog()

print("Waiting for clients...")


def handle_client(conn, addr):
    print(
        f"{threading.current_thread().name}: Connected {addr}"
    )

    while True:
        data = conn.recv(1024)

        if not data:
            break

        message = decode(data)

        if message == "HEARTBEAT":
            from election.heartbeat import received

            received()

            print(
                f"{threading.current_thread().name}: Heartbeat received"
            )

            continue

        elif message.startswith("REQUEST_VOTE"):

            from election.election import handle_vote_request

            handle_vote_request(message)

            continue

        command = parse(message)

        print(f"{threading.current_thread().name}: {command}")

        response = execute(command, replicate_to_replicas=(state.ROLE == "primary"))       
 
        conn.sendall(encode(response))

    conn.close()
    print(f"Disconnected: {addr}")


while True:
    conn, addr = server.accept()

    thread = threading.Thread(
        target=handle_client,
        args=(conn, addr),
        name=f"Client-{addr[1]}"
    )

    print(f"Main Thread: Created {thread.name}")

    thread.start()
