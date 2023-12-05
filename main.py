from regexp.parser import RegexParser
#from e_nfa.e_nfa_parser import EpsilonNFAParser
from e_nfa.e_nfa_parser2 import EpsilonNFAParser
from e_nfa.e_nfa_2 import Epsilon_NFA


def run():
    re = input("Enter a regular expression "
               "(valid operators are '*', '.', '∪', and '∩'; valid literals are all alphanumerics)"
               ": ")
    parser = RegexParser(re)
    final_token = parser.parse()
    print(final_token)
    enfaParser = EpsilonNFAParser(final_token)
    enfa = enfaParser.parse()
    print(enfa.startState)
    print(enfa.acceptingStates)
    print(enfa.transitions)


if __name__ == "__main__":
    run()
