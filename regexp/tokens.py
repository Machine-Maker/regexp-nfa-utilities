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
    
    def isLiteralToken(self) -> bool:
        return False
    
    def isOperatorToken(self) -> bool:
        return False


class LiteralToken(RegexToken):
    def __init__(self, token_id: str):
        super().__init__(token_id)

    def __repr__(self):
        return self._wrap(self._id)
    
    def isLiteralToken(self) -> bool:
        return True


class OperatorToken(RegexToken, metaclass=ABCMeta):

    @abstractmethod
    def consume_operands(self, operands: List[RegexToken]):
        ...
        
    def isOperatorToken(self) -> bool:
        return True
    
    def isUnaryOperatorToken(self) -> bool:
        return False
    
    def isBinaryOperatorToken(self) -> bool:
        return False


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
        
    def isUnaryOperatorToken(self) -> bool:
        return True
    
    def isKleeneStarToken(self) -> bool:
        return False


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
        
    def getLeft(self) -> RegexToken:
        return self.left
    
    def getRight(self) -> RegexToken:
        return self.right
        
    def isBinaryOperatorToken(self) -> bool:
        return True
    
    def isConcatToken(self) -> bool:
        return False
    
    def isUnionToken(self) -> bool:
        return False
    
    def isIntersectionToken(self) -> bool:
        return False


class ConcatToken(BinaryOperatorToken):
    def __init__(self):
        super().__init__(".")

    def __repr__(self):
        return self._wrap(f"{self.left}{self._id}{self.right}")
    
    def isConcatToken(self) -> bool:
        return True


class UnionToken(BinaryOperatorToken):
    def __init__(self):
        super().__init__("∪")
        
    def isUnionToken(self) -> bool:
        return True


class IntersectionToken(BinaryOperatorToken):
    def __init__(self):
        super().__init__("∩")
        
    def isIntersectionToken(self) -> bool:
        return True


class KleeneStarToken(UnaryOperatorToken):
    def __init__(self):
        super().__init__("*")
        
    def isKleeneStarToken(self) -> bool:
        return True
