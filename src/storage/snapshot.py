import json
import os

SNAPSHOT_FILE = "/data/snapshot.json"


def save_snapshot(db):
    with open(SNAPSHOT_FILE, "w") as f:
        json.dump(db, f)


def load_snapshot():
    if not os.path.exists(SNAPSHOT_FILE):
        return {}

    with open(SNAPSHOT_FILE, "r") as f:
        return json.load(f)
