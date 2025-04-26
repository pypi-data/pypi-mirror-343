import pydantic

from gadpytestprofiler.models.extensions.psutils import IO
from gadpytestprofiler.models.extensions.psutils import Network
from gadpytestprofiler.models.extensions.sqlalchemy import Query
from gadpytestprofiler.models.extensions.yappi import Execution
from gadpytestprofiler.models.python.garbage import GarbageCollector
from gadpytestprofiler.models.python.tracemalloc import Allocation


class SqlalchemyProfiling(pydantic.BaseModel):
    query: Query
    allocation: Allocation
    execution: Execution
    garbage: GarbageCollector
    network: Network
    io: IO
