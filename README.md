## regexp-nfa-utilities

A Project to parse a simplified Regular Expression into an NFA data structure and convert to epsilon-free NFA.
It provides an interface for testing of string memberships in the Language defined by a Regular Expression.
<br>
<br>
<p>
	<img width="600" alt="image" src="https://github.com/Machine-Maker/regexp-nfa-utilities/assets/18277544/e545426b-ca0c-4cdc-a722-ca8bd639f0d6">
</p>

**How It Works**:
NFA is created from parsed user input based on 'ε'(epsilon) construction algorithim. It is then processed into an ε-free model for testing.
<p>
<img width="150" alt="image" src="https://github.com/Machine-Maker/regexp-nfa-utilities/assets/18277544/fbe97717-3797-41c8-af2f-bb7cc6aba806">
<img width="180" alt="image" src="https://github.com/Machine-Maker/regexp-nfa-utilities/assets/18277544/2e5dff71-24f0-4918-8d0f-2361c79110be">
<img width="180" alt="image" src="https://github.com/Machine-Maker/regexp-nfa-utilities/assets/18277544/73aea863-e7ab-4fb5-aa37-69e0489ee740">
<img width="110" alt="image" src="https://github.com/Machine-Maker/regexp-nfa-utilities/assets/18277544/1785aeca-ca81-4688-9499-1d81f93f59d1">
<br>
<sub>NFA element construction forms ('.', '∪', *',  and '∩')</sub>
</p>

## User Guide

Before you begin, ensure you have met the following requirements:

* Python is installed on your system.
* You may want to study up on RegEx and Automata Theory!

**Program Expected Inputs**
```
operators: '*', '.', '∪', and '∩'
literals characters: all alphanumerics

Important: Concatenation may be indicated with a . or implied

Example:
(a ∪ b)*.a.b.b
(a ∪ b)*abb
```


## Program Options

1. Run python main.py optionally with the argument **main.py menu** for a simple CommandLine Menu.
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

Dr. Ravi <br>
Sonoma State University

## License

This project uses the MIT Open Source License.
=======
