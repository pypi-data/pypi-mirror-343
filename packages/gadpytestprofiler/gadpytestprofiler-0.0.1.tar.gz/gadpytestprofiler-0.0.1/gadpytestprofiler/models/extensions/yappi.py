import pydantic


class Execution(pydantic.BaseModel):
    class CPU(pydantic.BaseModel):
        time: float

    class Wall(pydantic.BaseModel):
        time: float

    cpu: CPU
    wall: Wall
    ratio: float
