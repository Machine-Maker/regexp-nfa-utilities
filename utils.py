import collections
from itertools import islice
from typing import Iterable


def consume(iterable: Iterable, count: int):
    """Skips 'count' iterations on the provided iterable"""
    if count is None:
        collections.deque(iterable, maxlen=0)
    else:
        next(islice(iterable, count, count), None)
