from regexp.tokens import RegexToken, LiteralToken, ConcatToken, UnionToken, IntersectionToken, KleeneStarToken
from e_nfa.e_nfa import Regex_E_NFA
from e_nfa.state import StateToken

class EpsilonNFAParser:
    regexp_T: RegexToken
    e_nfa: Regex_E_NFA
    
    def __init__(self, regexp_T: RegexToken):
        self.regexp_T = regexp_T
        ## self.e_nfa = \

    #def LiteralEpsilonState(self, tran)

    def parse(self) -> Regex_E_NFA:
        self.Regex_E_NFA = self.__parse(self.regexp_T)
        return self.Regex_E_NFA
    
    def concatENFA(self, E_NFA_L: Regex_E_NFA, E_NFA_R: Regex_E_NFA) -> Regex_E_NFA:    # ++++++ CONCAT FUNCTION ++++++
        newENFA = Regex_E_NFA()                                                         # Create New Epsilon NFA.
        newENFA.setStartState(E_NFA_L.getStartState())                                  # Set the start state to the Left NFA's start state.
                    
        for i in E_NFA_R.getFinalStates():                                              # Set the accepting states to the Right NFA's accepting state.
            newENFA.appendFinalState(i)
        for j in E_NFA_L.getFinalStates():                                              # Add Epsilon Transition(s) from all Left NFA accapting states
            newEpsilonLiteralToken = LiteralToken("?")                                  # to the Right NFA Starting state.
            j.addTransition(newEpsilonLiteralToken, E_NFA_R.getStartState())
                        
        return newENFA                                                                  # return epsilon nfa of concat
    
    def unionENFA(self, E_NFA_L: Regex_E_NFA, E_NFA_R: Regex_E_NFA) -> Regex_E_NFA:     # ++++++ UNION FUNCTION ++++++
        newENFA = Regex_E_NFA()                                                         # Create New Epsilon NFA.
        
        newStartState = StateToken()                                                    # Create New Start State.
        newEpsilonLiteralToken = LiteralToken("?")                                           
        newStartState.addTransition(newEpsilonLiteralToken, E_NFA_L.getStartState())    # Add Epsilon transitions from the new start state to the
        newStartState.addTransition(newEpsilonLiteralToken, E_NFA_L.getStartState())    # start states of the Left and Right Epsilon NFAs.
        newENFA.setStartState(newStartState)                                            # Set the new start state as the start state of the new ENFA.
        
        for i in E_NFA_L.getFinalStates():                                              # Add the accepting states of the Left ENFA to the New ENFA
            newENFA.appendFinalState(i)
        for j in E_NFA_L.getFinalStates():                                              # Add the accepting states of the Right ENFA to the New ENFA
            newENFA.appendFinalState(j)
            
        return newENFA                                                                  # return epsilon nfa of union
    
    def kleeneStarENFA(self, E_NFA: Regex_E_NFA) -> Regex_E_NFA:                        # ++++++ KLEENESTAR FUNCTION ++++++
        newENFA = Regex_E_NFA()                                                         # Create New Epsilon NFA.
        
        newStartState = StateToken()                                                    # Create New Start State.
        newENFA.setStartState(newStartState)                                            # Set the new start state as the start state of the new ENFA.
        newENFA.appendFinalState(newStartState)                                         # Add the new start state to the accepting state(s) of the new ENFA
        
        newEpsilonLiteralToken = LiteralToken("?")                                      # Add Epsilon transition from the new start state to the
        newStartState.addTransition(newEpsilonLiteralToken, E_NFA.getStartState())      # start state of the old ENFA.
        
        for i in E_NFA.getFinalStates():                                                # Add Epsilon transitions from the accepting states to the
            newEpsilonLiteralToken = LiteralToken("?")                                  # old epsilon NFA's start state.
            i.addTransition(newEpsilonLiteralToken, E_NFA.getStartState())  
            newENFA.appendFinalState(i)                                                 # Add the accepting states of the ENFA to the New ENFA.
            
        return newENFA                                                                  # Return epsilon nfa of kleanestar
        
    def __parse(self, regexp_t) -> Regex_E_NFA:
        if (regexp_t.isOperatorToken()):
            if (regexp_t.isUnaryOperatorToken()):
                E_NFA = self.__parse(regexp_t.target)
                
                return self.kleeneStarENFA(E_NFA)               # return epsilon nfa of kleanestar
                   
            elif (regexp_t.isBinaryOperatorToken()):
                E_NFA_L = self.__parse(regexp_t.getLeft())           #This will be an Epsilon NFA
                E_NFA_R = self.__parse(regexp_t.getRight())          #This will be an Epsilon NFA
                               
                if (regexp_t.isConcatToken()):   
                    return self.concatENFA(E_NFA_L, E_NFA_R)    # return epsilon nfa of concat
                    
                elif (regexp_t.isUnionToken()): 
                    return self.unionENFA(E_NFA_L, E_NFA_R)     # return epsilon nfa of union
                    
                elif (regexp_t.isIntersectionToken()): 
                    return None                                 # NOT IMPLEMENTED, return epsilon nfa of intersection
                else:
                    raise Exception(f"Unexpected {regexp_t}, clasified as Binary Operator, Not assigned any child class")
                    
            else:
                raise Exception(f"Unexpected {regexp_t}, clasified as Operator, Not assigned any child class")
                
        elif (regexp_t.isLiteralToken):
            #Create the Starting and Accepting States.
            newAcceptingState = StateToken()
            newStartState = StateToken()
            #Add the transition to the Starting state, where it goes to Accepting State on Token
            newStartState.addTransition(regexp_t, newAcceptingState)
            
            #Create and assign the starting state and accepting state if the Epsilon NFA
            newENFA = Regex_E_NFA()
            newENFA.setStartState(newStartState)
            newENFA.appendFinalState(newAcceptingState)
            
            return newENFA
            
        else:
            raise Exception(f"Unexpected {regexp_t}, Not an Operator or Literal")  
            
        