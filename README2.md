# Regex, NFA Converter, and String Membership Tester

This Python program allows testing of string memberships in the Language defined by a Regular Expression.

**How It Works**:
User Input is parsed, Epsilon NFA is created with State, transition, and symbol information based on construction algorithim. The NFA is then converted to an e-free NFA for testing.


## User Guide

Before you begin, ensure you have met the following requirements:

* Python is installed on your system.
* You may want to study up on RegEx and Automata Theory!

**Program Expected Inputs**
```
operators: '*', '.', '∪', and '∩'
literals characters: all alphanumerics

Important: Concatenation must be indicated with a .

Example:
(a ∪ b)*.a.b.b

not (a ∪ b)*.abb
```


## Program Options

1. Run python main.py optionally with the argument main.py menu for a simple CommandLine Menu.
2. Test RegEx expressions and sets of test strings from 3 options:
.csv, user input, or a randomly generated

## 

## Files and Folders
```
	regex-utils
	├── membership_test    - contains case testing functions and datasets
	└── regexp
        └── parser.py      - parses user input into RegEx
        main.py            - main program loop in run()
        nfa.py             - NFA class, State class, and functions
        main.cpp           - main program, setup and draw UI, connect to mysql
```
## Importance of RegEx and Language Membership
* Pattern Recognition in mathematical and computational contexts.
* Model Checking, a formal verification technique used to verify behaviors and  properties of state machines and systems.
* NLP, In linguistics and NLP, regular expressions are used to define language patterns and extract information from text.
* Database Queries: Regular expressions can be used in database queries for pattern matching and data extraction. For example, finding and filtering records based on specific text patterns.
* Validation and Parsing: Regular expressions are used to validate and parse structured data, such as dates, email addresses, and phone numbers, in mathematical and computational applications.


## Contributors

This page is the repository for our final project for CS: 454 - Theory of Automata

* [@yourusername](https://github.com/yourusername)
* [@contributor1](https://github.com/contributor1)
* [@jordannakamoto](https://github.com/jordannakamoto)

## Acknowledgements

Dr. Ravi

## License

This project uses the MIT Open Source License.