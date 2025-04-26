from gadpytestprofiler import models


def report(explains: list[dict]) -> list[models.Explain]:
    return [models.Explain(**explain) for explain in explains]
