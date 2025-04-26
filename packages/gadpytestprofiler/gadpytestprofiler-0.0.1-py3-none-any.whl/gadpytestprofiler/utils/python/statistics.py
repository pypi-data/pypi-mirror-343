import statistics

from gadpytestprofiler import models


def report(durations: list[float]) -> models.Statistics:
    return models.Statistics(
        mean=statistics.mean(durations),
        median=statistics.median(durations),
        stdev=statistics.stdev(durations) if len(durations) > 1 else 0.0,
        min=min(durations),
        max=max(durations),
    )
