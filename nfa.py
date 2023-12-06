from __future__ import annotations
from regexp.tokens import RegexToken, UnaryOperatorToken, BinaryOperatorToken, OperatorToken, LiteralToken, UnionToken, IntersectionToken, KleeneStarToken, ConcatToken
from itertools import combinations, product

EPSILON = 'ε'

current_label = 65
class State:
    _label: chr
    transitions: dict[chr, set[State]]

    def __init__(self):
        global current_label
        if current_label > 65 + 26:
            raise Exception("Cannot create more than 26 labels with labels enabled")
        self._label = chr(current_label)
        self.transitions = {}
        current_label += 1

    def add_transition(self, literal: chr, to_state: State):
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
    left_states = left.collect_states()
    right_states = right.collect_states()
    language: set[chr] = set([literal for state in left_states for literal in state.transitions.keys()])
    language = language.union(set([literal for state in right_states for literal in state.transitions.keys()]))
    product_states = [(pair, State()) for pair in compute_pairs(left_states, right_states)]
    print(product_states)
    for ((left_state, right_state), state) in product_states:
        print(left_state, right_state, state)
    raise Exception("Not implemented.")

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

    def __init__(self, initial: State, accepting: set[State]):
        self.initial = initial
        self.accepting = accepting

    def collect_states(self) -> set[State]:
        states: set[State] = set()
        stack: list[State] = [self.initial]
        while len(stack) > 0:
            state = stack.pop()
            states.add(state)
            for (literal, next_states) in state.transitions.items():
                for next_state in next_states:
                    if next_state not in states:
                        stack.append(next_state)
        return states

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
