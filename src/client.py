import socket

NODES = [
    ("127.0.0.1", 5000),
    ("127.0.0.1", 5001),
    ("127.0.0.1", 5002),
]

client = None


def connect():

    global client

    if client:
        try:
            client.close()
        except:
            pass

    for host, port in NODES:

        try:

            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

            s.connect((host, port))

            client = s

            print(f"\nConnected to {host}:{port}\n")

            return

        except:

            print(f"Could not connect to {host}:{port}")

    raise Exception("No server available")


connect()

while True:

    msg = input("Enter your message: ")

    while True:

        try:

            client.sendall(msg.encode())

            data = client.recv(1024)

            print("Server:", data.decode())

            break

        except Exception:

            print("\nConnection lost.")

            print("Reconnecting...\n")

            connect()

            print("Retrying request...\n")
