from regexp.parser import RegexParser
from nfa import parse_regex_token
from e_nfa.e_nfa_2 import Epsilon_NFA
from utils import insert_implicit_concatenation
from membership_test.generate_random_regex import generate_random_regex
from membership_test.membership_test import test_regex_from_csv, prompt_and_test_membership
import sys


def run():

    if len(sys.argv) > 1 and sys.argv[1] == 'menu':
        menu_mode()
    else:
        script_mode()
        

    

def script_mode():
    # Enable following lines...
    #     if you want to source input RegEx from csv, random generation, or just a written string
    # test_regex_from_csv('membership_test/small_sample/dataset1/dataset1.csv') # add "True" to arg[1] to Show Details: expected [Y/N] vs actual
    # re = generate_random_regex(6, 'abcd')
    # re = '((c.b ∩ c ∪ c) ∪ (b ∪ a ∩ a*)) ∪ ((a* ∩ a*).b ∩ b)'

    re = input("Enter a regular expression "
               "(valid operators are '*', '.', '∪', and '∩'; valid literals are all alphanumerics)"
               ": ")
    re = insert_implicit_concatenation(re)
    parser = RegexParser(re)
    final_token = parser.parse()
    print(final_token)
    nfa = parse_regex_token(final_token)
    print("reachable states", nfa.collect_reachable_states())
    print(nfa)

    # convert and print again
    nfa.convert_e_to_efree()
    nfa.print_epsilon_closure_table()
    print(nfa)

    prompt_and_test_membership(re,nfa)

def menu_mode():
    while True:
        printMenuSlide()
        choice = input("")
        
        # Menu Selection Items
        if choice == '1':
            re = input("Enter a regular expression "
               "(valid operators are '*', '.', '∪', and '∩'; valid literals are all alphanumerics)"
               ": ")
            run_regex_test1(re)
        elif choice == '2': # choose from a list of preset csv filePaths, choose to display test details (y/n)
            printCSVSlide()
            csv_choice = input("")

            if csv_choice == '1':
                csv_file = 'membership_test/small_sample/dataset1/dataset1.csv'
            elif csv_choice == '2':
                csv_file = 'membership_test/real_data/dataset1/dataset1.csv'
            else:
                print("Invalid key input.")
                continue

            show_details = input("Show Details (y/n): ")
            if show_details.lower() == 'y':
                test_regex_from_csv(csv_file, True)
            else:
                test_regex_from_csv(csv_file, False)
            pass
        elif choice == '3': # randomly generate re string
            num_operators = int(input("Enter the number of operators(recommended: 5): "))
            alphabet_letters = input("Enter the letters in the alphabet (e.g., 'abcd'): ")
            re = generate_random_regex(num_operators, alphabet_letters)
            print(f"Randomly Generated Regular Expression: {re}")
            run_regex_test1(re)
        elif choice == '4':
            print("Exiting the program.")
            exit()
        else:
            print("Invalid choice. Please select a valid option (1/2/3/4).")


# Regex > NFA processing we've been using in main up to this point simply turned into a function
def run_regex_test1(re):
    parser = RegexParser(re)
    final_token = parser.parse()
    print(final_token)
    nfa = parse_regex_token(final_token)
    print("reachable states", nfa.collect_reachable_states())
    print(nfa)
    nfa.convert_e_to_efree()
    nfa.print_epsilon_closure_table()
    print(nfa)
    prompt_and_test_membership(re,nfa)

def printMenuSlide():
    print("\n╔══════════════════════════════╗")
    print("║             Menu             ║")
    print("╠══════════════════════════════╣")
    print("║ 1. Test from User Input      ║")
    print("║ 2. Test from CSV (Choose CSV)║")
    print("║ 3. Test Randomly Generated   ║")
    print("║ 4. Exit                      ║")
    print("╚══════════════════════════════╝")

def printCSVSlide():
    print("\n╔══════════════════════════════╗")
    print("║      Choose a CSV file       ║")
    print("╠══════════════════════════════╣")
    print("║ 1. Small Sample 1            ║")
    print("║ 2. 50char dataset            ║")
    print("╚══════════════════════════════╝")

if __name__ == "__main__":
    run()
