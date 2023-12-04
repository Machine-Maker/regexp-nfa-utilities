from regexp.tokens import RegexToken, LiteralToken, ConcatToken, UnionToken, IntersectionToken, KleeneStarToken
from e_nfa.e_nfa_2 import Epsilon_NFA, LiteralNFA, kleeneStarNFA, concatNFA, unionNFA

class EpsilonNFAParser:
    regexp_T: RegexToken
    ENFA: Epsilon_NFA
    
    def __init__(self, regexp_T: RegexToken):
        self.regexp_T = regexp_T
    
    def parse(self) -> Epsilon_NFA:
        self.ENFA = self.__parse(self.regexp_T)
        return self.ENFA
    
    def __parse(self, regexp_t) -> Epsilon_NFA:
        if (regexp_t.isOperatorToken()):
            if (regexp_t.isUnaryOperatorToken()):
                E_NFA = self.__parse(regexp_t.target)
                return kleeneStarNFA(E_NFA)                    # return epsilon nfa of kleanestar
                   
            elif (regexp_t.isBinaryOperatorToken()):
                E_NFA_L = self.__parse(regexp_t.getLeft())          #This will be an Epsilon NFA
                E_NFA_R = self.__parse(regexp_t.getRight())         #This will be an Epsilon NFA
                               
                if (regexp_t.isConcatToken()):   
                    return concatNFA(E_NFA_L, E_NFA_R)        # return epsilon nfa of concat
                    
                elif (regexp_t.isUnionToken()): 
                    return unionNFA(E_NFA_L, E_NFA_R)         # return epsilon nfa of union
                    
                elif (regexp_t.isIntersectionToken()): 
                    return None                                     # NOT IMPLEMENTED, return epsilon nfa of intersection
                else:
                    raise Exception(f"Unexpected {regexp_t}, clasified as Binary Operator, Not assigned any child class")
                    
            else:
                raise Exception(f"Unexpected {regexp_t}, clasified as Operator, Not assigned any child class")
                
        elif (regexp_t.isLiteralToken):
            newENFA = Epsilon_NFA()
            return LiteralNFA(newENFA, regexp_t.getid())
            