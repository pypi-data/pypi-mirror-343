import tracemalloc

from gadpytestprofiler import models


def report() -> models.Allocation:
    current, peak = tracemalloc.get_traced_memory()
    return models.Allocation(current=current, peak=peak)
