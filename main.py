from regexp.parser import RegexParser
from nfa import parse_regex_token
from e_nfa.e_nfa_2 import Epsilon_NFA


def run():
    re = input("Enter a regular expression "
               "(valid operators are '*', '.', '∪', and '∩'; valid literals are all alphanumerics)"
               ": ")
    parser = RegexParser(re)
    final_token = parser.parse()
    print(final_token)
    nfa = parse_regex_token(final_token)
    print(nfa.collect_states())
    print(nfa)


if __name__ == "__main__":
    run()
