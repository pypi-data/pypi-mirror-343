import pydantic


class Network(pydantic.BaseModel):
    class Bytes(pydantic.BaseModel):
        sent: float
        received: float

    class Packets(pydantic.BaseModel):
        sent: int
        received: int

    bytes: Bytes
    packets: Packets


class IO(pydantic.BaseModel):
    class Time(pydantic.BaseModel):
        read: float
        write: float
        busy: float

    class Bytes(pydantic.BaseModel):
        read: float
        write: float

    time: Time
    bytes: Bytes
