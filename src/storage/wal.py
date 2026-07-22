import os

WAL_FILE = "wal.log"


def append(command):
    with open(WAL_FILE, "a") as f:
        f.write(command + "\n")


def recover():
    if not os.path.exists(WAL_FILE):
        return []

    with open(WAL_FILE, "r") as f:
        return [line.strip() for line in f]
