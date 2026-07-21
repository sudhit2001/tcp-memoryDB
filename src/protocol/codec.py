def decode(data: bytes) -> str:
    return data.decode("utf-8").strip()


def encode(message: str) -> bytes:
    return message.encode("utf-8")
