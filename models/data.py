from dataclasses import dataclass

@dataclass
class DataPayload:
    id: int
    content: str
    timestamp: float
