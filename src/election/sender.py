import threading
import time
from replication.client import replicate


def heartbeat_sender():
    while True:
        replicate("HEARTBEAT")
        print("Heartbeat sent")
        time.sleep(1)


def start_heartbeat():
    thread = threading.Thread(
        target=heartbeat_sender,
        daemon=True,
        name="Heartbeat"
    )
    thread.start()
