import random, time
# Works by generating a list of operators of input length, assigns operands to them from the alaphbet
# then randomly combines list items removing 2 and reinserting the combined item surrounded by ( )
# until there is only one final combined item representing the final list

# add back intersection by devising a deck of valid intersections and flipping to include or not include them

def generate_operator_item(alphabet):
    operator = random.choice(['*', '.', '∪'])
    operand = random.choice(alphabet)
    
    if operator in ['*', '+']:
        return operand + operator
    else:
        second_operand = random.choice(alphabet)
        return operand + operator + second_operand

def generate_operator_expression(length, alphabet):
    return [generate_operator_item(alphabet) for _ in range(length)]

def generate_nested_pattern(operator_items, alphabet):
    while len(operator_items) > 1:
        # Randomly select two different items
        a, b = random.sample(operator_items, 2)
        operator_items.remove(a)
        operator_items.remove(b)

        # Randomly select a binary operator
        binary_operator = random.choices(['.', '∪', '∩'], weights=[4, 2, 1], k=1)[0]

        # Special process to create a valid intersectional pattern
        if(binary_operator == '∩'):
            # Decide which item to keep and which to discard
            kept_item = random.choice([a, b])
            # Create a variation of the kept item
            varied_item1 = create_variation(kept_item, alphabet)
            # Create a variation of the kept item
            varied_item2 = create_variation(kept_item, alphabet)
            new_item = f"({'('+varied_item1+')'}{binary_operator}{'('+varied_item2+')'})"
        else:
            # Combine the items and add back to the list surrounded by "("   ")"
            new_item = f"({a}{binary_operator}{b})"
        operator_items.append(new_item)

    # The last remaining item is the final pattern
    return operator_items[0]

def generate_random_regex(length, alphabet):
    operator_items = generate_operator_expression(length, alphabet)
    nested_pattern = generate_nested_pattern(operator_items, alphabet)
    return nested_pattern


def create_variation(item, alphabet):
    # Generate a small nested pattern to append to the item
    # Limit the length to a small number for simplicity
    mini_length = random.randint(1,2)  # For example, a length between 1 and 3
    mini_operator_items = generate_operator_expression(mini_length, alphabet)
    mini_nested_pattern = generate_nested_pattern(mini_operator_items, alphabet)
    
    # Randomly choose between concatenation and union as the connector
    connector = random.choice(['.', '∪'])

    # Combine the original item with the mini nested pattern using the connector
    return f"({item}{connector}{mini_nested_pattern})"