from abc import ABC, ABCMeta, abstractmethod
from typing import List, Callable, Mapping, Optional
from itertools import islice
import collections


class RegexToken(ABC):
    _id: str

    # utility to make displaying the full token after
    _parens: bool = False

    def __init__(self, token_id: str):
        self._id = token_id

    def _wrap(self, string_rep: str) -> str:
        return f"({string_rep})" if self._parens else string_rep


class LiteralToken(RegexToken):
    def __init__(self, token_id: str):
        super().__init__(token_id)

    def __repr__(self):
        return self._id


class OperatorToken(RegexToken, metaclass=ABCMeta):

    @abstractmethod
    def consume_operands(self, operands: List[RegexToken]):
        ...


class UnaryOperatorToken(OperatorToken, metaclass=ABCMeta):
    target: RegexToken

    def __init__(self, token_id: str):
        super().__init__(token_id)

    def consume_operands(self, operands: List[RegexToken]):
        if len(operands) < 1:
            raise Exception(f"The {self._id} operator expects 1 operands, found {len(operands)}")
        self.target = operands.pop()
        operands.append(self)


class BinaryOperatorToken(OperatorToken, metaclass=ABCMeta):
    left: RegexToken
    right: RegexToken

    def __init__(self, token_id: str):
        super().__init__(token_id)

    def __repr__(self):
        return self._wrap(f"{self.left} {self._id} {self.right}")

    def consume_operands(self, operands: List[RegexToken]):
        if len(operands) < 2:
            raise Exception(f"The {self._id} operator expects 2 operands, found {len(operands)}")
        self.right = operands.pop()
        self.left = operands.pop()
        operands.append(self)


class ConcatToken(BinaryOperatorToken):
    def __init__(self):
        super().__init__(".")


class UnionToken(BinaryOperatorToken):
    def __init__(self):
        super().__init__("∪")


class IntersectionToken(BinaryOperatorToken):
    def __init__(self):
        super().__init__("∩")


class KleeneStarToken(UnaryOperatorToken):
    def __init__(self):
        super().__init__("*")

    def __repr__(self):
        return self._wrap(f"{self.target}*")


BINARY_OPERATORS: List[List[str]] = [
    ["."],
    ["∪", "∩"]
]

BINARY_OPERATOR_TOKEN_FACTORIES: Mapping[str, Callable[[], OperatorToken]] = {
    "*": KleeneStarToken,
    ".": ConcatToken,
    "∪": UnionToken,
    "∩": IntersectionToken,
}


def is_operator_higher_precedence(op: str, prev_op: str):
    if op == prev_op:
        return False  # return False, so the first one will be applied
    for (idx, ops) in enumerate(BINARY_OPERATORS):
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
    return char == "*" or any([True for ops in BINARY_OPERATORS if char in ops])


def consume(iterator, count):
    if count is None:
        collections.deque(iterator, maxlen=0)
    else:
        next(islice(iterator, count, count), None)


class RegexParser:
    operators: List[str]
    operands: List[RegexToken]
    regexp: str
    empty: bool = True

    def __init__(self, regexp: str):
        self.operators = []
        self.operands = []
        self.regexp = regexp

    def parse(self) -> Optional[RegexToken]:
        indices = iter(range(len(self.regexp)))
        for i in indices:
            c = self.regexp[i]
            if c.isspace():  # skip whitespace, whitespace is not important for parsing a reg expr.
                continue
            self.empty = False
            if c == "(":
                consume(indices, self._process_paren_group(i))
            elif is_operator(c):
                if c == "*":  # only 1 unary op, and its highest prio
                    self.operators.append(c)
                    self._apply_last_operator()
                    continue
                elif len(self.operators) != 0 and not is_operator_higher_precedence(c, self.operators[-1]):
                    self._apply_last_operator()
                    self.operators.append(c)
                else:
                    self.operators.append(c)
            else:
                self.operands.append(LiteralToken(c))

        if len(self.operators) == 1:  # there will sometimes be 1 single operator left that needs to be applied
            self._apply_last_operator()

        if len(self.operators) != 0 or (not self.empty and len(self.operands) != 1):
            raise Exception(f"Badly formatted regular expression: exp: {self.regexp}, ops: {self.operators}, ands: {self.operands}")

        return None if len(self.operands) == 0 else self.operands[0]

    def _apply_last_operator(self):
        op_token = BINARY_OPERATOR_TOKEN_FACTORIES[self.operators.pop()]()
        op_token.consume_operands(self.operands)

    # returns the number to skip on the parent regular expression string
    def _process_paren_group(self, start: int) -> int:
        end = self.regexp.rfind(')')
        if end == -1:
            raise Exception(f"Mismatched parentheses found in {self.regexp}")
        sub_parser = RegexParser(self.regexp[start + 1:end])
        token = sub_parser.parse()
        if token:
            token._parens = True
            self.operands.append(token)
        return end - start


def run():
    re = input("Enter a regular expression: ")
    parser = RegexParser(re)
    final_token = parser.parse()
    print(final_token)
    # print(re)


if __name__ == "__main__":
    run()


