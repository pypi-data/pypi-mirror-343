import yappi

from gadpytestprofiler import models


def report() -> models.Execution:
    statistics = yappi.get_func_stats()

    wall = yappi.get_clock_time()

    cpu = sum([s.ttot for s in statistics])

    ratio = cpu / wall if wall > 0 else 0

    return models.Execution(cpu=models.Execution.CPU(time=cpu), wall=models.Execution.Wall(time=wall), ratio=ratio)
