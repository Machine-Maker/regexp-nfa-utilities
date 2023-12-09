from nfa import NFA
from regexp.parser import RegexParser
from nfa import parse_regex_token
import csv

# membership_test

# isMember(nfa, input_string)
# each letter of the string is sequentially compared to the availability of a valid transition path
def isMember(nfa: NFA, input_string: str) -> bool:
    current_states = {nfa.initial} # init at start state

    for letter in input_string:
        next_states = set()
        for state in current_states:
            # Move to the next states for the current symbol
            if letter in state.transitions:
                next_states.update(state.transitions[letter])

        current_states = next_states

    # Check if any of the current states are accepting states
    if any(state in nfa.accepting for state in current_states):
        state_names = ', '.join([state.__repr__() for state in current_states])
        # print(f"The string '{input_string}' matches the NFA. Ending states: {state_names}")
        return True
    else:
        state_names = ', '.join([state.__repr__() for state in current_states])
        # print(f"The string '{input_string}' does not match the NFA. Ending states: {state_names}")
        return False
    
# prompt and test
def prompt_and_test_nfa(nfa: NFA):
    while True:
        input_string = input("Enter a test string (or type 'exit' to stop): ")
        if input_string.lower() == 'exit':
            print("Exiting test.")
            break

        if isMember(nfa, input_string):
            print(f"Yes: the string '{input_string}' is in the language.")
        else:
            print(f"No: the string '{input_string}' is not in the language.")


def parse_csv(file_path):
    patterns = []
    with open(file_path, newline='') as csvfile:
        reader = csv.reader(csvfile)
        for row in reader:
            if row and row[0] != 'Regex' and row[0] != 'Test String,Accepts':
                regex, test_string, expected_result = row
                patterns.append((regex, test_string, expected_result == 'Yes'))
    return patterns

def run_single_test(nfa, regex, test_string, expected, show_details=False):
    actual = isMember(nfa, test_string)
    if actual == expected:
        result = "✓"
    else:
        result = "✗"

    if show_details or result == "✗":
        print(f"Result: {result} | String: '{test_string}', Expected: {expected}, Found: {actual}")
    else:
        print(f"Result: {result} | String: '{test_string}'")


def test_regex_from_csv(filePath, show_details=False):
    patterns = parse_csv(filePath)
    last_regex = None
    nfa = None

    for regex, test_string, expected in patterns:
        if regex != last_regex:
            print(regex)
            parser = RegexParser(regex)
            final_token = parser.parse()
            nfa = parse_regex_token(final_token)
            nfa.collect_reachable_states()
            nfa.convert_e_to_efree()
            last_regex = regex

        run_single_test(nfa, regex, test_string, expected, show_details)