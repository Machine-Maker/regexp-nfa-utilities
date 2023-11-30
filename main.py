from regexp.parser import RegexParser
from e_nfa.e_nfa_parser import EpsilonNFAParser


def run():
    re = input("Enter a regular expression "
               "(valid operators are '*', '.', '∪', and '∩'; valid literals are all alphanumerics)"
               ": ")
    parser = RegexParser(re)
    final_token = parser.parse()
    print(final_token)
    enfaParser = EpsilonNFAParser(final_token)
    enfa = enfaParser.parse()
    enfa.printENFA()
    


if __name__ == "__main__":
    run()
