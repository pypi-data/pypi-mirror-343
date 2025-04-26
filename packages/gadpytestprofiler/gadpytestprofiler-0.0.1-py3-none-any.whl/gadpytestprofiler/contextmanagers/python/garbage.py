import contextlib
import gc


@contextlib.contextmanager
def garbagecollector():
    gc.collect()
    yield
