import contextlib

import yappi


@contextlib.contextmanager
def yapper():
    yappi.clear_stats()
    yappi.start()
    try:
        yield
    finally:
        yappi.stop()
