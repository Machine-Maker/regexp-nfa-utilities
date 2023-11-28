from regexp.tokens import RegexToken
from e_nfa.e_nfa import Regex_E_NFA
from regexp.operators import is_operator

class EpsilonNFAParser:
    regexp_T: RegexToken
    e_nfa: Regex_E_NFA
    
    def __init__(self, regexp_T: RegexToken):
        self.regexp_T = regexp_T
        ## self.e_nfa = \

    def parse(self) -> Regex_E_NFA:
        self.Regex_E_NFA = self.__parse(self.regexp_T)
        return self.Regex_E_NFA
        
    def __parse(self, regexp_t) -> Regex_E_NFA:
        '''
        if (regexp_t.is_operator()):
            if (regexp_t.is_single_operator()):
                temp_E_NFA = __parse(regexp_t.target)
                ## return epsilon nfa of kleanestar
                
            elif (regexp_t.is_double_operator()):
                temp_E_NFA_1 = __parse(regexp_t.left)
                temp_E_NFA_2 = __parse(regexp_t.right)
               
                if (regexp_t.is_concatToken()):
                    ## return epsilon nfa of concat
                elif (regexp_t.is_unionToken()): 
                    ## return epsilon nfa of union
                elif (regexp_t.is_intersectionToken()): 
                    ## return epsilon nfa of intersection
                else:
                    ## ERROR
                    
            else:
                ## ERROR
                
        else:        
            ## return epsilon nfa of a variable 
        '''