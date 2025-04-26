import asyncio
import concurrent.futures
import typing

from gadpytestprofiler import contextmanagers
from gadpytestprofiler import models
from gadpytestprofiler.utils import garbage
from gadpytestprofiler.utils import psutils
from gadpytestprofiler.utils import statistics
from gadpytestprofiler.utils import tracemalloc
from gadpytestprofiler.utils import yappi


class FunctionProfiler:
    def __init__(self, func: typing.Callable, runs: int = 1, users: int | None = None) -> None:
        self._func = func
        self._runs = runs
        self._users = users

    def once(self) -> typing.Any:
        with contextmanagers.timer() as timer:
            result = self._func()
        return result, timer()

    def iterate(self) -> list[float]:
        durations = []
        for _ in range(self._runs):
            _, timer = self.once()
            durations.append(timer)
        return durations

    def parallel(self) -> list[float]:
        with concurrent.futures.ThreadPoolExecutor(max_workers=self._users) as pool:
            results = list(pool.map(lambda _: self.iterate(), range(self._users)))
        return [duration for result in results for duration in result]

    def analyze(self) -> typing.Tuple[typing.Any, models.FunctionProfiling]:
        with (
            contextmanagers.yapper(),
            contextmanagers.allocation(),
            contextmanagers.garbagecollector(),
            contextmanagers.io() as io,
            contextmanagers.network() as network,
        ):
            result, duration = self.once()

            if self._users:
                durations = self.parallel()
            elif self._runs > 1:
                durations = self.iterate()
            else:
                durations = [duration]

            report = models.FunctionProfiling(
                statistics=statistics.report(durations),
                allocation=tracemalloc.report(),
                execution=yappi.report(),
                garbage=garbage.report(),
                network=psutils.netreport(network()),
                io=psutils.ioreport(io()),
            )

        return result, report


class AsyncFunctionProfiler:
    def __init__(self, func: typing.Callable, runs: int = 1, users: int | None = None) -> None:
        self._func = func
        self._runs = runs
        self._users = users

    async def once(self) -> typing.Any:
        with contextmanagers.timer() as timer:
            result = await self._func()
        return result, timer()

    async def iterate(self) -> list[float]:
        durations = []
        for _ in range(self._runs):
            _, timer = await self.once()
            durations.append(timer)
        return durations

    async def parallel(self) -> list[float]:
        durations = []
        for _ in range(self._runs):
            tasks = [self.once() for _ in range(self._users)]
            results = await asyncio.gather(*tasks)
            durations.extend([timer for _, timer in results])
        return durations

    async def analyze(self) -> typing.Tuple[typing.Any, models.FunctionProfiling]:
        with (
            contextmanagers.yapper(),
            contextmanagers.allocation(),
            contextmanagers.garbagecollector(),
            contextmanagers.io() as io,
            contextmanagers.network() as network,
        ):
            result, duration = await self.once()

            if self._users:
                durations = await self.parallel()
            elif self._runs > 1:
                durations = await self.iterate()
            else:
                durations = [duration]

            report = models.FunctionProfiling(
                statistics=statistics.report(durations),
                allocation=tracemalloc.report(),
                execution=yappi.report(),
                garbage=garbage.report(),
                network=psutils.netreport(network()),
                io=psutils.ioreport(io()),
            )

        return result, report
