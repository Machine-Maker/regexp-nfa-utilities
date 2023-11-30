from typing import List, Optional
from regexp.tokens import LiteralToken

class StateToken:
    __transitions: list                     #This is a list of list[(LiteralToken, StateToken)]
    
    def __init__(self):
        self.__transitions = []
    
    def addTransition(self, tValue:LiteralToken, destination):  #addTransition(self, LiteralToken, StateToken)
        self.__transitions.append((tValue, destination))
        
    def searchTransitionDestination(self, tValue:LiteralToken) -> Optional[list]:
        destinations = []
        
        indicies = iter(range(len(self.__transitions)))
        for i in indicies:
            if self.__transitions[i][0] == tValue:
                destinations.append(self.__transitions[i][1])
                
        return None if len(destinations) == 0 else destinations
    
