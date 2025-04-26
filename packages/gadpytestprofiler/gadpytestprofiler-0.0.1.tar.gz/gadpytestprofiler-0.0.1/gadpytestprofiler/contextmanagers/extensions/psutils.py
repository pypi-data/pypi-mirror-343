import contextlib

import psutil


@contextlib.contextmanager
def network():
    start = psutil.net_io_counters()
    yield lambda: {
        "bytes_sent": psutil.net_io_counters().bytes_sent - start.bytes_sent,
        "bytes_recv": psutil.net_io_counters().bytes_recv - start.bytes_recv,
        "packets_sent": psutil.net_io_counters().packets_sent - start.packets_sent,
        "packets_recv": psutil.net_io_counters().packets_recv - start.packets_recv,
    }


@contextlib.contextmanager
def io():
    start = psutil.disk_io_counters()
    yield lambda: {
        "read_bytes": psutil.disk_io_counters().read_bytes - start.read_bytes,
        "write_bytes": psutil.disk_io_counters().write_bytes - start.write_bytes,
        "busy_time": psutil.disk_io_counters().busy_time - start.busy_time,
        "read_time": psutil.disk_io_counters().read_time - start.read_time,
        "write_time": psutil.disk_io_counters().write_time - start.write_time,
    }
