from __future__ import annotations
from regexp.tokens import RegexToken, UnaryOperatorToken, BinaryOperatorToken, OperatorToken, LiteralToken, UnionToken, IntersectionToken, KleeneStarToken, ConcatToken
from itertools import combinations, product

EPSILON = 'ε'
current_label = 65
class State:
    _label: chr
    transitions: dict[chr, set[State]]
    epsilon_closure: set()

    def __init__(self):
        global current_label
        if current_label > 64 + 26:
            order = int((current_label-64) // 26)
            self._label = chr((current_label - 64) % 26 + 65) + str(order+1)
            # raise Exception("Cannot create more than 26 labels with labels enabled")
        else:
            self._label = chr(current_label)
        self.transitions = {}
        self.epsilon_closure = ()
        current_label += 1

    def add_transition(self, literal: chr, to_state: State):
        assert(to_state is not None)
        assert(literal is not None)
        if literal not in self.transitions:
            self.transitions[literal] = {to_state}
        else:
            self.transitions[literal].add(to_state)

    def __repr__(self):
        return f"{self._label}"




def parse_literal_token(token: LiteralToken) -> NFA:
    initial = State()
    accepting = State()
    initial.add_transition(token.getid(), accepting)
    return NFA(initial, {accepting})

def parse_union_token(token: UnionToken) -> NFA:
    left = parse_regex_token(token.left)
    right = parse_regex_token(token.right)
    initial = State()  # create a new initial state
    initial.add_transition(EPSILON, left.initial)  # add epsilon transition to the left's initial
    initial.add_transition(EPSILON, right.initial)  # add epsilon transition to the right's initial
    accepting = left.accepting.union(right.accepting)  # accepting states are the left + right's accepting states
    return NFA(initial, accepting)

# https://stackoverflow.com/questions/35270766/python-getting-unique-pairs-from-multiple-lists-of-different-lengths
def compute_pairs(*lists):
    for t in combinations(lists, 2):
        for pair in product(*t):
            yield pair

def parse_intersection_token(token: IntersectionToken) -> NFA:
    left = parse_regex_token(token.left)
    right = parse_regex_token(token.right)
    left_states = left.collect_reachable_states()
    right_states = right.collect_reachable_states()
    product_states = { pair:State() for pair in compute_pairs(left_states, right_states) }
    initial_state = None
    accepting_states = set()
    for ((left_state, right_state), state) in product_states.items():
        if left_state is left.initial and right_state is right.initial:  # the initial state is the state that makes up the pair of initial states in the original NFAs
            assert(initial_state is None)  # only 1 state should meet this criteria
            initial_state = state
        if left_state in left.accepting and right_state in right.accepting:  # the accepting states are all states whose pairs are in the accepting states of the original NFAs
            accepting_states.add(state)
        common_symbols = set(left_state.transitions.keys()).intersection(set(right_state.transitions.keys()))  # all output symbols for the 2 states (handle EPSILON separately)
        common_symbols.discard(EPSILON)
        for symbol in common_symbols:
            for (next_left_state, next_right_state) in compute_pairs(left_state.transitions[symbol], right_state.transitions[symbol]):
                state.add_transition(symbol, product_states[(next_left_state, next_right_state)])
        if EPSILON in left_state.transitions.keys() or EPSILON in right_state.transitions.keys():
            for (next_left_state, next_right_state) in compute_pairs(left_state.transitions.get(EPSILON, set()).union({left_state}), right_state.transitions.get(EPSILON, set()).union({right_state})):
                state.add_transition(EPSILON, product_states[(next_left_state, next_right_state)])
    #     print("="*20)
    # print(f"initial: {initial_state}")
    # print(f"accepting: {accepting_states}")
    return NFA(initial_state, accepting_states)
    # raise Exception("Not implemented.")

def parse_concat_token(token: ConcatToken) -> NFA:
    left = parse_regex_token(token.left)
    right = parse_regex_token(token.right)
    initial = left.initial  # initial state is the initial state of the "left" expression
    accepting = right.accepting # accepting state is the accepting state of the "right" expression
    for accept in left.accepting: # add transitions from the left's accepting to the right's initial
        accept.add_transition(EPSILON, right.initial)
    return NFA(initial, accepting)

def parse_kleene_star_token(token: KleeneStarToken) -> NFA:
    root = parse_regex_token(token.target)
    initial = State() # create new initial state
    accepting = {initial}
    initial.add_transition(EPSILON, root.initial)  # add transition to the root's initial state
    for accept in root.accepting:  # add epsilon transitions from the root's accepting states to the root's initial states
        accept.add_transition(EPSILON, root.initial)
    accepting = accepting.union(root.accepting)  # accepting states are the new initial state and the root's accepting states
    return NFA(initial, accepting)

def parse_unary_op_token(token: UnaryOperatorToken) -> NFA:
    if isinstance(token, KleeneStarToken):
        return parse_kleene_star_token(token)
    else:
        raise Exception(f"Unexpected unary op token {token}")

def parse_binary_op_token(token: BinaryOperatorToken) -> NFA:
    if isinstance(token, ConcatToken):
        return parse_concat_token(token)
    elif isinstance(token, UnionToken):
        return parse_union_token(token)
    elif isinstance(token, IntersectionToken):
        return parse_intersection_token(token)
    else:
        raise Exception(f"Unexpected binary op token {token}")

def parse_operator_token(token: OperatorToken) -> NFA:
    if isinstance(token, UnaryOperatorToken):
        return parse_unary_op_token(token)
    elif isinstance(token, BinaryOperatorToken):
        return parse_binary_op_token(token)
    else:
        raise Exception(f"Unexpected operator token {token}")

def parse_regex_token(token: RegexToken) -> NFA:
    if isinstance(token, LiteralToken):
        return parse_literal_token(token)
    elif isinstance(token, OperatorToken):
        return parse_operator_token(token)
    else:
        raise Exception(f"Unexpected token {token}")

class NFA:
    initial: State
    accepting: set[State]
    states: set[State]

    def __init__(self, initial: State, accepting: set[State]):
        self.initial = initial
        self.accepting = accepting
        self.states = set()

    def collect_reachable_states(self) -> set[State]:
        #states: set[State] = set()
        stack: list[State] = [self.initial]
        while len(stack) > 0:
            state = stack.pop()
            self.states.add(state)
            for (literal, next_states) in state.transitions.items():
                for next_state in next_states:
                    if next_state not in self.states:
                        stack.append(next_state)
        return self.states #promoted states to class member.

    # ----------   
    # Jordan's Code #
    # CONVERT ε-NFA to εfree-NFA
    #
    # ForEach NFA State:
    # 1. determine epsilon closure                ~ following ε-transitions alone find set of states reachable. Includes the state itself.
    # 2. build new transition set:
    #       2a. copy transitions to current state from its e-clo members. Since the state itself exists in its e-clo, its non ε-transitions will be maintained as expected.
    #       2b. new set ignores ε-transitions which acts as their removal step
    # 
    # Then:
    #    update accepting states: If a state leads to a final(accepting) state on an ε-transition, it should become a final state itself by inheritance on the epsilon move.
    # ----------

    # the following functions run this process for each state in the NFA
    
    # Step 1. determine epsilon closures
    def determine_epsilon_closures(self):
        # iterate over states
        for state in self.states:
            epsilon_closure = set() # temporary set for building state.eCLO
            visited_states = set()

             # recursive function dfs: (depth first search)
             # adds destination_state(s) of 'ε' current_state.transitions
             # to current_state.epsilon_closure
            def dfs(current_state):
                visited_states.add(current_state)
                epsilon_closure.add(current_state)

                for destination_state in current_state.transitions.get('ε', []):
                    if destination_state not in visited_states:
                        dfs(destination_state)

            dfs(state)
            state.epsilon_closure = epsilon_closure


    # Step 2. build new transitions
    def build_transitions_from_epsilon_closure(self):
        for state in self.states:
            new_transitions = {} # temporary set for building new transitions

            # Iterate over the current state's ε-CLO
            # create new transitions for current state based on the transitions from its epsilon-reachable states
            for epsilon_reachable_state in state.epsilon_closure:
                for symbol, states in epsilon_reachable_state.transitions.items():
                    if symbol == 'ε':
                        continue
                    if symbol in new_transitions:
                        # If the symbol key exists, add the new states to the existing set
                        new_transitions[symbol] = new_transitions[symbol].union(states)
                    else:
                        # If the symbol key does not exist, create a new set with these states for transition[symbol,set(states)]
                        new_transitions[symbol] = set(states)

            # Update the transitions for the current state, ε-transitions have now been excluded
            state.transitions = new_transitions

    # Step 3. 
    def update_accepting_states_from_epsilon_closure(self):
        # iterate over states
        for state in self.states:
            # Check each state in its epsilon closure
            for epsilon_reachable_state in state.epsilon_closure:
                # If the epsilon closure state is in the set of accepting states
                if epsilon_reachable_state in self.accepting:
                    # This state becomes an accepting state by inheritance
                    self.accepting.add(state)

    # Composite Convert Function
    # call from main.py
    def convert_e_to_efree(self):
        self.determine_epsilon_closures()
        self.build_transitions_from_epsilon_closure()
        self.update_accepting_states_from_epsilon_closure()

    # Print Functions
    # print Epsilon Closures Table
    def print_epsilon_closure_table(self):
        print(f"\nEpsilon Closures Table")
        for state in self.states:
                # gather eCLO state label strings for output
                epsilon_closure_labels = [s._label for s in state.epsilon_closure]
                print(f"εCLO[{state._label}]: {', '.join(epsilon_closure_labels)}")
        print("")

    # End Jordan's Code #
        
     # natural print function for class NFA
    def __repr__(self):
        s = f"initial: {self.initial}"
        s+= f"\naccepting: {{ {', '.join(map(str, self.accepting))} }}"
        s += f"\nDelta Function Table"
        stack: list[State] = [self.initial]
        visited: set[State] = set()
        while len(stack) > 0:
            state = stack.pop();
            visited.add(state)
            s += f"\n\tTransitions for {state}"
            print(f"state: {state}, transitions: {state.transitions}")
            for (literal, next_states) in state.transitions.items():
                for next_state in next_states:
                    s += f"\n\t{literal} -> {next_state}"
                    if next_state not in visited:
                        stack.append(next_state)
        return s