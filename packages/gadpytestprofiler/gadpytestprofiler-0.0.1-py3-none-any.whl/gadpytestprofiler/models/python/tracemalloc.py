import pydantic


class Allocation(pydantic.BaseModel):
    current: float
    peak: float
