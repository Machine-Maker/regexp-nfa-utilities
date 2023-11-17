from abc import ABC, ABCMeta, abstractmethod
from typing import List


class RegexToken(ABC):
    _id: str

    # utility to make displaying the full token after more accurate to the input
    _parens: bool = False

    def __init__(self, token_id: str):
        self._id = token_id

    def _wrap(self, string_rep: str) -> str:
        return f"({string_rep})" if self._parens else string_rep


class LiteralToken(RegexToken):
    def __init__(self, token_id: str):
        super().__init__(token_id)

    def __repr__(self):
        return self._wrap(self._id)


class OperatorToken(RegexToken, metaclass=ABCMeta):

    @abstractmethod
    def consume_operands(self, operands: List[RegexToken]):
        ...


class UnaryOperatorToken(OperatorToken, metaclass=ABCMeta):
    target: RegexToken

    def __init__(self, token_id: str):
        super().__init__(token_id)

    def __repr__(self):
        return self._wrap(f"{self.target}{self._id}")

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

    def __repr__(self):
        return self._wrap(f"{self.left}{self._id}{self.right}")


class UnionToken(BinaryOperatorToken):
    def __init__(self):
        super().__init__("∪")


class IntersectionToken(BinaryOperatorToken):
    def __init__(self):
        super().__init__("∩")


class KleeneStarToken(UnaryOperatorToken):
    def __init__(self):
        super().__init__("*")
