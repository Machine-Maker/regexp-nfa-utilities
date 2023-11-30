from e_nfa.state import StateToken

class Regex_E_NFA:
    startState: StateToken
    finalStates: list[StateToken]
    #stateList: list[StateToken]

    def __init__(self):
        self.finalStates = []
        self.startState = None
        
    def getStartState(self):
        return self.startState
    
    def setStartState(self, newStartState: StateToken):
        self.startState = newStartState
    
    def getFinalStates(self) -> list:
        return self.finalStates
    
    def appendFinalState(self, newFinalState: StateToken):
        self.finalStates.append(newFinalState)
        
    def isFinalState(self, state: StateToken) -> bool:
        for i in self.finalStates:
            if state == i:
                return True
        return False
    
    def printENFA(self):
        print(self.startState.)
        print(self.finalStates)
    