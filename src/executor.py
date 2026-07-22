from database import store
from storage.wal import append
from storage.snapshot import save_snapshot
import os
write_count = 0
SNAPSHOT_INTERVAL = 5

def execute(command, recovery=False):
    global write_count
    if command.cmd == "SET":

        if not recovery:
            append(f"SET {command.key} {command.value}")

        store.set(command.key, command.value)

        write_count += 1

        if write_count >= SNAPSHOT_INTERVAL:
            save_snapshot(store.dump())

            open("wal.log", "w").close()

            write_count = 0

        return "OK"

    elif command.cmd == "GET":
        value = store.get(command.key)
        return value if value is not None else "NOT FOUND"

    elif command.cmd == "DEL":

        if not recovery:
            append(f"DEL {command.key}")

        deleted = store.delete(command.key)
        
        write_count += 1

        if write_count >= SNAPSHOT_INTERVAL:
            save_snapshot(store.dump())

            open("wal.log", "w").close()

            write_count = 0

        return "OK" if deleted is not None else "NOT FOUND"

    elif command.cmd == "EXISTS":
        return "1" if store.exists(command.key) else "0"

    return "INVALID COMMAND"
