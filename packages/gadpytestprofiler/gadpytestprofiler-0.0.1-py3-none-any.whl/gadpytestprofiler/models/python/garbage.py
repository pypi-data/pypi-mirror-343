import pydantic


class GarbageCollector(pydantic.BaseModel):
    collected: int
    uncollectable: int
