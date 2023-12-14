from nfa import NFA
from regexp.parser import RegexParser
from nfa import parse_regex_token
import csv, textwrap

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
def prompt_and_test_membership(re, nfa: NFA):
    print("::Testing::")
    print(re)
    while True:
        input_string = input("Enter a test string (or type 'exit' to stop): ")
        if input_string.lower() == 'exit':
            print("Exiting test.")
            break

        if isMember(nfa, input_string):
            print(f"'{input_string}': Yes, the string is in the language.")
        else:
            print(f"'{input_string}': No, the string  is not in the language.")


# returns a tuple with a parsed row and a label if it has one
def parse_csv(file_path):
    patterns_with_labels = []
    current_label = None
    current_regex = None

    with open(file_path, newline='') as csvfile:
        reader = csv.reader(csvfile)
        for row in reader:
            # Check if the row is a label/description
            first_cell = row[0].strip()
            if first_cell.startswith('('):  # This row is a regex
                current_regex = first_cell
            elif row and row[0].startswith('#'):
                current_label = row[0][1:].strip()  # Store the label
            else:
                test_string, expected_result = row
                patterns_with_labels.append((current_label, (current_regex,test_string, expected_result == 'Yes')))
                current_label = None  # Reset the label memory after attaching it to a pattern
    return patterns_with_labels

def run_single_test(nfa, regex, test_string, expected, show_details=False):
    actual = isMember(nfa, test_string)
    if actual == expected:
        result = "✓"
    else:
        result = "✗"

    # Check if test_string is longer than 20 characters
    if len(test_string) > 20:
        wrapped_string = textwrap.fill(test_string, width=20)
        test_string_display = "\n'" + wrapped_string + "'"
    else:
        test_string_display = f"'{test_string}'"

    if show_details or result == "✗":
        print(f"Result: {result} | String: {test_string_display}, Expected: {expected}, Found: {actual}")
    else:
        print(f"Result: {result} | String: {test_string_display}")


def test_regex_from_csv(filePath, show_details=False):
    patterns_with_labels = parse_csv(filePath)
    last_regex = None
    nfa = None

    for label, (regex, test_string, expected) in patterns_with_labels:

        # Process the regex pattern
        if regex != last_regex:
            print('\n'+'Testing RegEx:\n'+regex)
            print(label+'\n')
            label = None
            parser = RegexParser(regex)
            final_token = parser.parse()
            nfa = parse_regex_token(final_token)
            nfa.collect_reachable_states()
            nfa.convert_e_to_efree()
            last_regex = regex

        run_single_test(nfa, regex, test_string, expected, show_details)

        # Print the label if present
        if label:
            print(label)
