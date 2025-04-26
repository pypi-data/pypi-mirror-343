from gadpytestprofiler import models


def report(
    sql: tuple[models.Statistics, models.Statistics, models.Statistics],
    orm: tuple[models.Statistics, models.Statistics, models.Statistics],
    explains: list[models.Explain],
) -> models.Query:
    return models.Query(
        sql=models.Query.Detail(execute=sql[0], fetch=sql[1], scalar=sql[2]),
        orm=models.Query.Detail(execute=orm[0], fetch=orm[1], scalar=orm[2]),
        explains=explains,
    )
