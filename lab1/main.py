from collections import defaultdict
from FiniteAutomation import FiniteAutomation

def main():
    # Define DFA states, alphabet, transitions, start state, and final states
    states = {"q0", "q1", "q2", "q3"}
    alphabet = {"a", "b", "c"}
    transitions = {
        "q0": {"a": "q1", "b": "q2"},
        "q1": {"b": "q2"},
        "q2": { "c": "q3"},
        "q3": {"a": "q1"}
    }
    start_state = "q0"
    final_states = {"q3"}
    
    # Create FiniteAutomation instance
    dfa = FiniteAutomation(states, alphabet, transitions, start_state, final_states)
    
    # Print FiniteAutomation details
    print(dfa)
    
    # Test string acceptance
    test_strings = ["aab", "abba", "abab", "bbb", "aaa"]
    for s in test_strings:
        result = dfa.string_belongs_to_language(s)
        print(f'String "{s}" accepted? {result}')
    
    # Check automaton type
    print("Automaton type:", dfa.check_type())
    
    # Convert to Regular Grammar (if applicable)
    grammar = dfa.to_regular_grammar()
    print("Equivalent Regular Grammar:")
    print(grammar)
    
    # Convert NFA to DFA (if needed)
    if dfa.check_type() != "DFA":
        converted_dfa = dfa.nfa_to_dfa()
        print("Converted DFA:")
        print(converted_dfa)

if __name__ == "__main__":
    main()