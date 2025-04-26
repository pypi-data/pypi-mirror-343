import asyncio
import typing

from sqlalchemy.dialects.postgresql import dialect
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.sql import Executable
from sqlalchemy.sql import text

from gadpytestprofiler import contextmanagers
from gadpytestprofiler import models
from gadpytestprofiler.utils import garbage
from gadpytestprofiler.utils import postgres
from gadpytestprofiler.utils import psutils
from gadpytestprofiler.utils import sqlalchemy
from gadpytestprofiler.utils import statistics
from gadpytestprofiler.utils import tracemalloc
from gadpytestprofiler.utils import yappi


class SqlalchemyProfiler:
    def __init__(self, session: AsyncSession, query: Executable, runs: int = 1, users: int | None = None) -> None:
        self._session = session
        self._orm = query
        self._sql = query.compile(dialect=dialect(), compile_kwargs={"literal_binds": True})
        self._runs = runs
        self._users = users

    async def tables(self) -> typing.Any:
        return (await self._session.execute(self._orm)).scalars().all()

    async def sql(self) -> tuple[tuple, tuple, tuple]:
        with contextmanagers.timer() as timer:
            rows = await self._session.execute(text(str(self._sql)))
        execute = timer()

        with contextmanagers.timer() as timer:
            rows.fetchall()
        fetch = timer()

        with contextmanagers.timer() as timer:
            rows.scalars().all()
        scalar = timer()

        return execute, fetch, scalar

    async def orm(self) -> tuple[tuple, tuple, tuple]:
        with contextmanagers.timer() as timer:
            rows = await self._session.execute(self._orm)
        execute = timer()

        with contextmanagers.timer() as timer:
            rows.fetchall()
        fetch = timer()

        with contextmanagers.timer() as timer:
            rows.scalars().all()
        scalar = timer()

        return execute, fetch, scalar

    async def once(self) -> tuple[typing.Any, tuple[tuple, tuple, tuple], tuple[tuple, tuple, tuple]]:
        return (
            await self.tables(),
            await self.sql(),
            await self.orm(),
        )

    async def iterate(self) -> tuple[list[tuple[tuple, tuple, tuple]], list[tuple[tuple, tuple, tuple]]]:
        sql, orm = [], []
        for _ in range(self._runs):
            _, _sql, _orm = await self.once()
            sql.append(_sql)
            orm.append(_orm)
        return sql, orm

    async def parallel(self) -> tuple[list[tuple[tuple, tuple, tuple]], list[tuple[tuple, tuple, tuple]]]:
        sql, orm = [], []
        for _ in range(self._runs):
            tasks = [self.once() for _ in range(self._users)]
            results = await asyncio.gather(*tasks)
            for _, _sql, _orm in results:
                sql.append(_sql)
                orm.append(_orm)
        return sql, orm

    async def explain(self) -> list[dict]:
        return (
            await self._session.execute(
                text(f"EXPLAIN (ANALYZE, VERBOSE, COSTS, BUFFERS, TIMING, SUMMARY, FORMAT JSON) {self._sql}")
            )
        ).scalar()

    async def analyze(self) -> tuple[typing.Any, models.SqlalchemyProfiling]:
        with (
            contextmanagers.yapper(),
            contextmanagers.allocation(),
            contextmanagers.garbagecollector(),
            contextmanagers.io() as io,
            contextmanagers.network() as network,
        ):
            explains = await self.explain()

            tables, sql, orm = await self.once()

            if self._users:
                sql, orm = await self.parallel()
            elif self._runs > 1:
                sql, orm = await self.iterate()
            else:
                sql, orm = [sql], [orm]

            execute, fetch, scalar = list(zip(*sql))
            sql = (
                statistics.report(execute),
                statistics.report(fetch),
                statistics.report(scalar),
            )

            execute, fetch, scalar = list(zip(*orm))
            orm = (
                statistics.report(execute),
                statistics.report(fetch),
                statistics.report(scalar),
            )

            report = models.SqlalchemyProfiling(
                query=sqlalchemy.report(sql=sql, orm=orm, explains=postgres.report(explains)),
                allocation=tracemalloc.report(),
                execution=yappi.report(),
                garbage=garbage.report(),
                network=psutils.netreport(network()),
                io=psutils.ioreport(io()),
            )

        return tables, report
