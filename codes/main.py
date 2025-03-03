from Grammar import Grammar
from FiniteAutomation import FiniteAutomation

def main():
    grammar = Grammar(
        non_terminals={'S', 'B', 'L'},
        terminals={'a', 'b', 'c'},
        start_symbol='S',
        rules={
            'S': [['a', 'B']],
            'B': [['b', 'B'], ['c', 'L']],
            'L': [['c', 'L'], ['a', 'S'], ['b']]
        }
    )
    fa = grammar.toFiniteAutomaton() 
    
    unique_strings = set()
    while len(unique_strings) < 5:
        generated = grammar.generate_string()
        unique_strings.add(generated)

    print("Generated unique strings:")
    for generated in unique_strings:
        print(generated)

    print("\nFinite Automaton transitions and states:")
    for state, transitions in fa.transitions.items():
        print(f"State: {state}")
        for symbol, next_state in transitions.items():
            print(f"  {symbol} -> {next_state}")

    print("\nChecking if FA accepts generated strings:")
    for generated in unique_strings:
        is_accepted = fa.string_belongs_to_language(generated)
        print(f"String '{generated}' accepted: {is_accepted}")

    chomsky_type = grammar.find_Chomsky_type()
    print(f"Grammar Chomsky Type: {chomsky_type}")
if __name__ == "__main__":
    main()