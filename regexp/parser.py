from typing import List, Optional
from regexp.tokens import RegexToken, LiteralToken
from regexp.operators import BINARY_OPERATOR_TOKEN_FACTORIES, is_operator, is_operator_higher_precedence
from utils import consume


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
            elif c.isalnum():
                self.operands.append(LiteralToken(c))
            else:
                raise Exception(f"Unexpected {c} found in {self.regexp}")

        while len(self.operators) > 0: # consume all the remaning operators
            self._apply_last_operator()

        if len(self.operators) != 0 or (not self.empty and len(self.operands) != 1):
            raise Exception(
                f"Badly formatted regular expression: exp: {self.regexp}, ops: {self.operators}, ands: {self.operands}")

        return None if len(self.operands) == 0 else self.operands[0]

    def _apply_last_operator(self):
        op_token = BINARY_OPERATOR_TOKEN_FACTORIES[self.operators.pop()]()
        op_token.consume_operands(self.operands)

    # returns the number to skip on the parent regular expression string
    def _process_paren_group(self, start: int) -> int:
        count = 0
        end = -1
        for i, c in enumerate(self.regexp[start:]):
            if c == '(':
                count += 1
            elif c == ')':
                assert(count > 0)
                count -= 1
                if count == 0:
                    end = start + i
                    break
        if end == -1:
            raise Exception(f"Mismatched parentheses found in {self.regexp}")
        sub_parser = RegexParser(self.regexp[start + 1:end])
        token = sub_parser.parse()
        if token:
            token._parens = True
            self.operands.append(token)
        return end - start
