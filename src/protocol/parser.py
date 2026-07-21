from command import Command

def parse(message: str):
    parts = message.split()

    if not parts:
        return None

    cmd = parts[0].upper()

    key = parts[1] if len(parts) > 1 else ""
    value = parts[2] if len(parts) > 2 else ""

    return Command(cmd, key, value)
