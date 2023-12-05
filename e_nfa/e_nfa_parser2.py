from regexp.tokens import RegexToken, UnaryOperatorToken, BinaryOperatorToken, OperatorToken, LiteralToken, ConcatToken, UnionToken, IntersectionToken, KleeneStarToken
from e_nfa.e_nfa_2 import Epsilon_NFA, constructLiteralNFA, kleeneStarNFA, concatNFA, unionNFA

class EpsilonNFAParser:
    regexp_T: RegexToken
    ENFA: Epsilon_NFA

    def __init__(self, regexp_T: RegexToken):
        self.regexp_T = regexp_T

    def parse(self) -> Epsilon_NFA:
        self.ENFA = self.__parse(self.regexp_T)
        return self.ENFA

    def __parse(self, regexp_t: RegexToken) -> Epsilon_NFA:
        if isinstance(regexp_t, OperatorToken):
            if isinstance(regexp_t, UnaryOperatorToken):
                E_NFA = self.__parse(regexp_t.target)
                return kleeneStarNFA(E_NFA)                    # return epsilon nfa of kleanestar

            elif isinstance(regexp_t, BinaryOperatorToken):
                E_NFA_L = self.__parse(regexp_t.getLeft())          #This will be an Epsilon NFA
                E_NFA_R = self.__parse(regexp_t.getRight())         #This will be an Epsilon NFA

                if isinstance(regexp_t, ConcatToken):
                    return concatNFA(E_NFA_L, E_NFA_R)        # return epsilon nfa of concat

                elif isinstance(regexp_t, UnionToken):
                    return unionNFA(E_NFA_L, E_NFA_R)         # return epsilon nfa of union

                elif isinstance(regexp_t, IntersectionToken):
                    return None                                     # NOT IMPLEMENTED, return epsilon nfa of intersection
                else:
                    raise Exception(f"Unexpected {regexp_t}, clasified as Binary Operator, Not assigned any child class")
            else:
                raise Exception(f"Unexpected {regexp_t}, clasified as Operator, Not assigned any child class")
        elif isinstance(regexp_t, LiteralToken):
            newENFA = Epsilon_NFA()
            return constructLiteralNFA(newENFA, regexp_t.getid())
        else:
            raise Exception(f"Unepected {regexp_t}, not an operator or literal")

