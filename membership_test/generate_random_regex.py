import random

# Works by generating a list of operators of input length, assigns operands to them from the alaphbet
# then randomly combines list items removing 2 and reinserting the combined item surrounded by ( )
# until there is only one final combined item representing the final list

def generate_operator_item(alphabet):
    operator = random.choice(['*', '.', '∪', '∩'])
    operand = random.choice(alphabet)
    
    if operator in ['*', '+']:
        return operand + operator
    else:
        second_operand = random.choice(alphabet)
        return operand + operator + second_operand

def generate_operator_expression(length, alphabet):
    return [generate_operator_item(alphabet) for _ in range(length)]

def generate_nested_pattern(operator_items):
    while len(operator_items) > 1:
        # Randomly select two different items
        a, b = random.sample(operator_items, 2)
        operator_items.remove(a)
        operator_items.remove(b)

        # Randomly select a binary operator
        binary_operator = random.choice(['.', '∪', '∩'])

        # Combine the items and add back to the list surrounded by "("   ")"
        new_item = f"({a}{binary_operator}{b})"
        operator_items.append(new_item)

    # The last remaining item is the final pattern
    return operator_items[0]

def generate_random_regex(length, alphabet):
    operator_items = generate_operator_expression(length, alphabet)
    nested_pattern = generate_nested_pattern(operator_items)
    return nested_pattern