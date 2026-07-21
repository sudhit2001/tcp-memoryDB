from dataclasses import dataclass

@dataclass
class Command:
    cmd: str
    key: str = ""
    value: str = ""
