# regexp-nfa-utilities

**How It Works**:
Epsilon NFA is created with State, transition, and symbol information based on construction algorithim. The state information is then processed iteratively to remove epsilon transitions into a deterministic model for string membership testing.


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
(a ∪ b)*abb
```


## Program Options

1. Run python main.py optionally with the argument main.py menu for a simple CommandLine Menu.
2. Test RegEx expressions and sets of test strings from 3 options:
.csv, user input, or a randomly generated
3. The csv dataset in ./membership_test/small_sample/dataset1 should illustrate the fundamental patterns the program recognizes. The format of csv input should be fairly recognizeable as a RegEx followed by a series of test strings, the expected outcome of the test and providing for comment lines.

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

* [@jakepotrebic](https://github.com/Machine-Maker)
* [@samuelhobbs](https://github.com/samuelhobbs)
* [@jordannakamoto](https://github.com/jordannakamoto)

## Runtime/Algorithim Information
The program should serve as a basic implementation, that can be optimized for various purposes specific to the languages being represented. For example; adding string pre-processing, indexing into certain parts of the NFA, and lazy construction are example methods to be of use for certain pattern-matching applications.

## Acknowledgements

Dr. Ravi

## License

This project uses the MIT Open Source License.
=======
Design Doc - Probably not that useful
https://docs.google.com/document/d/1tWiAd6sdG_nlba4SMwqguRaVR073G5wQG7L6K2hbgPU/edit
