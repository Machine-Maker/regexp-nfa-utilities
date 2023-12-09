import collections
from itertools import islice
from typing import Iterable


def consume(iterable: Iterable, count: int):
    """Skips 'count' iterations on the provided iterable"""
    if count is None:
        collections.deque(iterable, maxlen=0)
    else:
        next(islice(iterable, count, count), None)

def insert_implicit_concatenation(input: str) -> str:
    output = input;
    for i in range(len(input) - 1, 0, -1):
        if input[i].isalnum() and input[i - 1].isalnum(): # if it finds aa
            output = output[:i] + "." + output[i:]
        if input[i - 1] == ')' and input[i] == '(': # if it finds )(
            output = output[:i] + "." + output[i:]
        if input[i - 1] == '*' and (input[i].isalnum() or input[i] == '('): # if it finds *a or *(
            output = output[:i] + "." + output[i:]
    return output
