import socket
import threading
from protocol.codec import decode, encode
from protocol.parser import parse
from executor import execute
HOST = "0.0.0.0"
PORT = 5000

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind((HOST, PORT))
server.listen(5)

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

        command = parse(message)

        print(f"{threading.current_thread().name}: {command}")

        response = execute(command)

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
