from gadpytestprofiler import models


def netreport(diff: dict) -> models.Network:
    return models.Network(
        bytes=models.Network.Bytes(
            sent=diff["bytes_sent"],
            received=diff["bytes_recv"],
        ),
        packets=models.Network.Packets(
            sent=diff["packets_sent"],
            received=diff["packets_recv"],
        ),
    )


def ioreport(diff: dict) -> models.IO:
    return models.IO(
        bytes=models.IO.Bytes(
            read=diff["read_bytes"],
            write=diff["write_bytes"],
        ),
        time=models.IO.Time(
            read=diff["read_time"],
            write=diff["write_time"],
            busy=diff["busy_time"],
        ),
    )
