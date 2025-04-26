import pydantic

from gadpytestprofiler.models.extensions.postgres import Explain
from gadpytestprofiler.models.python.statistics import Statistics


class Query(pydantic.BaseModel):
    class Detail(pydantic.BaseModel):
        execute: Statistics
        fetch: Statistics
        scalar: Statistics

    sql: Detail
    orm: Detail
    explains: list[Explain]
