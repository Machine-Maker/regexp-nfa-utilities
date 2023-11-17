from regexp.parser import RegexParser


def run():
    re = input("Enter a regular expression "
               "(valid operators are '*', '.', '∪', and '∩'; valid literals are all alphanumerics)"
               ": ")
    parser = RegexParser(re)
    final_token = parser.parse()
    print(final_token)


if __name__ == "__main__":
    run()
