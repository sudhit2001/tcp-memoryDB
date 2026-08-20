import socket

def is_node_alive(host, port):

    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.settimeout(2)

        s.connect((host, port))

        s.close()

        return True

    except Exception:
        return False
