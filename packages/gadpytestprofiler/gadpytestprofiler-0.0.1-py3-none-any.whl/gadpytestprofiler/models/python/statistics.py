import pydantic


class Statistics(pydantic.BaseModel):
    mean: float
    median: float
    stdev: float
    min: float
    max: float
