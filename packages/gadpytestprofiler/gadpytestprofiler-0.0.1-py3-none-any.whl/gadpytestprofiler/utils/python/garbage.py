import gc

from gadpytestprofiler import models


def report() -> models.GarbageCollector:
    collected, uncollectable, _ = gc.get_count()
    return models.GarbageCollector(collected=collected, uncollectable=uncollectable)
