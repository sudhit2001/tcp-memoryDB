from database import store

def execute(command):
    if command.cmd == "SET":
        store.set(command.key, command.value)
        return "OK"

    elif command.cmd == "GET":
        value = store.get(command.key)
        return value if value is not None else "NOT FOUND"

    elif command.cmd == "DEL":
        deleted = store.delete(command.key)
        return "OK" if deleted is not None else "NOT FOUND"

    elif command.cmd == "EXISTS":
        return "1" if store.exists(command.key) else "0"

    return "INVALID COMMAND"
