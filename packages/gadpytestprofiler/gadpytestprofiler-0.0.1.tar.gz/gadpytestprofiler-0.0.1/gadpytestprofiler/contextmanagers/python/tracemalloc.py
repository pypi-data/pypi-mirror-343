import contextlib
import tracemalloc


@contextlib.contextmanager
def allocation():
    tracemalloc.start()
    try:
        yield
    finally:
        tracemalloc.stop()
