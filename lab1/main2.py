from FiniteAutomation import FiniteAutomation

def main():
    # Define the FA configuration: states, alphabet, transitions, start state, final states
    states = {'q0', 'q1', 'q2', 'q3'}
    alphabet = {'a', 'b', 'c'}
    transitions = {
        'q0': {'a': 'q1', 'b': 'q2'},
        'q1': {'b': 'q1', 'b': 'q2'},  # Multiple 'b' transitions, adjust this
        'q2': {'c': 'q3'},
        'q3': {'a': 'q1'}
    }
    start_state = 'q0'
    final_states = {'q3'}
    
    # Create a Finite Automation instance
    fa = FiniteAutomation(states, alphabet, transitions, start_state, final_states)
    
    # Print the configuration of the Finite Automation
    print("Finite Automaton Configuration:")
    print(fa)

    # Test strings to see if they belong to the language
    # test_strings = ['abc', 'abbc', 'bca', 'ab', 'cba']
    
    # print("\nTesting strings:")
    # for string in test_strings:
    #     print(f"\nTesting string: {string}")
    #     result = fa.string_belongs_to_language(string)
    #     print(f"Result: {'Accepted' if result else 'Rejected'}")

    # Optionally, test other functions like checking the type of FA, epsilon closure, or converting to regular grammar
    print("\nFA Type:")
    print(f"FA Type: {fa.check_type()}")
    
    # Check epsilon closure of state 'q0'
    print("\nEpsilon Closure of q0:")
    print(fa.epsilon_closure('q0'))
    
    # Convert the FA to a regular grammar (if Grammar class is defined elsewhere)
    print("\nConverted Regular Grammar:")
    grammar = fa.to_regular_grammar()
    print(grammar)

    # Convert NFA to DFA if necessary
    print("\nConverting NFA to DFA (if applicable):")
    dfa = fa.nfa_to_dfa()
    print(dfa)

if __name__ == "__main__":
    main()
