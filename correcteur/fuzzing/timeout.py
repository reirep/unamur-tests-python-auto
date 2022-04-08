import signal
from contextlib import contextmanager

from correcteur.fuzzing.exceptions.TimeoutException import TimeoutException


@contextmanager
def timeout(seconds):
    def signal_handler(signum, frame):
        raise TimeoutException()
    signal.signal(signal.SIGALRM, signal_handler)
    signal.alarm(seconds)
    try:
        yield
    finally:
        signal.alarm(0)
