from typing import List, Callable
from regexp.tokens import OperatorToken, KleeneStarToken, ConcatToken, UnionToken, IntersectionToken

BINARY_OPERATOR_PRECEDENCE: List[List[str]] = [
    # parens
    # kleene star
    ["."],
    ["∩"],
    ["∪"]
]

BINARY_OPERATOR_TOKEN_FACTORIES: dict[str, Callable[[], OperatorToken]] = {
    "*": KleeneStarToken,
    ".": ConcatToken,
    "∪": UnionToken,
    "∩": IntersectionToken,
}


def is_operator_higher_precedence(op: str, prev_op: str):
    if op == prev_op:
        return False  # return False, so the first one will be applied
    for ops in BINARY_OPERATOR_PRECEDENCE:
        if op in ops and prev_op in ops:  # if in the same category, previous is higher precedence
            return False
        elif op in ops:  # if you find the current op first, it is higher precedence
            return True
        elif prev_op in ops:  # if you find the prev op first, it is higher precedence
            return False
        else:
            continue
    raise Exception(f"Shouldn't happen: {op}, {prev_op}")


def is_operator(char: str):
    return char in BINARY_OPERATOR_TOKEN_FACTORIES.keys()
