
EPSILON_SYMBOL = "E"

class Epsilon_NFA:
    startState: int
    acceptingStates: list[bool]
    transitions: list[list[(str,int)]]  #[states][transitions of state]->(input, next state)

    def __init__(self):
        self.acceptingStates = []
        self.transitions = []
        self.startState = None

    def getStartState(self):
        return self.startState

    def setStartState(self, newStartState: int):
        self.startState = newStartState

    def setAcceptingState(self, state: int, accept: bool):
        #while (state >= len(self.finalStates)):
        #    self.finalStates.append(False)
        assert(state < len(self.acceptingStates))
        self.acceptingStates[state] = accept

    def addState(self, accepting = False) -> int:
        # appends an empty list to transitions
        # appends "accepting" to accepting States
        #  and returns the index
        self.transitions.append([])
        self.acceptingStates.append(accepting)
        assert (len(self.transitions) == len(self.acceptingStates))
        return len(self.transitions) - 1

    def addTransition(self, currState: int, inputV: str, nextState: int):
        # if currState is out of bounds of the Transistion list fail
        # else append to the transitions[currState] the tuple (inputV, nextState)
        assert(currState < len(self.transitions))
        self.transitions[currState].append((inputV,nextState))


def constructLiteralNFA(ENFA: Epsilon_NFA, transitionOn: str) -> Epsilon_NFA:
    assert(len(ENFA.transitions) == 0)
    newStartState = ENFA.addState()
    newAcceptState = ENFA.addState(True)
    ENFA.setStartState(newStartState)
    ENFA.addTransition(newStartState, transitionOn, newAcceptState)
    return ENFA

def kleeneStarNFA(ENFA: Epsilon_NFA) -> Epsilon_NFA:
    oldStartState = ENFA.getStartState()
    for i in range(len(ENFA.acceptingStates)):
        if ENFA.acceptingStates[i] == True:
            ENFA.addTransition(i, EPSILON_SYMBOL, oldStartState)
            
    newStartState = ENFA.addState(True)
    ENFA.addTransition(newStartState, EPSILON_SYMBOL, oldStartState)
    ENFA.setStartState(newStartState)
    return ENFA
    
def concatNFA(ENFA1: Epsilon_NFA, ENFA2: Epsilon_NFA) -> Epsilon_NFA:
    numStates_ENFA1 = len(ENFA1.acceptingStates)
    numStates_ENFA2 = len(ENFA2.acceptingStates)
    startState_ENFA2_in_ENFA1 = ENFA2.getStartState() + numStates_ENFA1
    
    for i in range(numStates_ENFA2):                                                                # Add states from ENFA2 to ENFA1
        ENFA1.addState()
    for i in range(numStates_ENFA1, numStates_ENFA1 + numStates_ENFA2):                             # Transfer ENFA2 transitions into ENFA1 with their new state numbers
        for j in ENFA2.transitions[i - numStates_ENFA1]:
            ENFA1.addTransition(i, j[0], j[1] + numStates_ENFA1)
    for i in range(numStates_ENFA1):                                                                # Go through and set ENFA1's accepting states to transition to
       if ENFA1.acceptingStates[i] == True:                                                         # ENFA2's start state in ENFA1.
           ENFA1.addTransition(i, EPSILON_SYMBOL, startState_ENFA2_in_ENFA1)
           ENFA1.setAcceptingState(i, False)                                                        # Set all ENFA1's accepting states equal to FALSE
    for i in range(numStates_ENFA2):                                                                # Set the new ENFA1, ENFA2, states to accepting if they accepted in ENFA2
        if (ENFA2.acceptingStates[i] == True):
            ENFA1.setAcceptingState(i + numStates_ENFA1, True)
    return ENFA1

def unionNFA(ENFA1: Epsilon_NFA, ENFA2: Epsilon_NFA) -> Epsilon_NFA:
    numStates_ENFA1 = len(ENFA1.acceptingStates)
    numStates_ENFA2 = len(ENFA2.acceptingStates)

    for i in range(numStates_ENFA2):                                                                # Add states from ENFA2 to ENFA1
        ENFA1.addState()
    for i in range(numStates_ENFA1, numStates_ENFA1 + numStates_ENFA2):                             # Transfer ENFA2 transitions into ENFA1 with their new state numbers
        for j in ENFA2.transitions[i - numStates_ENFA1]:
            ENFA1.addTransition(i, j[0], j[1] + numStates_ENFA1)
    for i in range(numStates_ENFA2):                                                                # Set the new ENFA1, ENFA2, states to accepting if they accepted in ENFA2
        if (ENFA2.acceptingStates[i] == True):
            ENFA1.setAcceptingState(i + numStates_ENFA1, True)

    newStartState = ENFA1.addState()                                                                # Create the new start state and add transitions from it to the two old starting states
    ENFA1.addTransition(newStartState, EPSILON_SYMBOL, ENFA1.getStartState())
    ENFA1.addTransition(newStartState, EPSILON_SYMBOL, ENFA2.getStartState() + numStates_ENFA1)
    ENFA1.setStartState(newStartState)
    return ENFA1

