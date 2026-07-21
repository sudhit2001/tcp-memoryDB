import threading
import time

class KeyValueStore:

    def __init__(self):
        self.db = {}
        self.lock = threading.Lock()

    def set(self, key, value):
        with self.lock:
            print(f"{threading.current_thread().name} acquired lock")

            time.sleep(10)

            self.db[key] = value

            print(f"{threading.current_thread().name} released lock")

    def get(self, key):
        with self.lock:
            return self.db.get(key)

    def delete(self, key):
        with self.lock:
            return self.db.pop(key, None)

    def exists(self, key):
        with self.lock:
            return key in self.db

store = KeyValueStore()

