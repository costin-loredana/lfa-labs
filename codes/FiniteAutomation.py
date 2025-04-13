from collections import defaultdict

class FiniteAutomation:
    def __init__(self, states, alphabet, transitions, start_state, final_states):
        self.states = states
        self.alphabet = alphabet
        self.transitions = transitions
        self.start_state = start_state
        self.final_states = final_states

    def __repr__(self):
        return(f"Finite Automation:\n"
               f"States: {self.states}\n"
               f"Alphabet: {self.alphabet}\n"
               f"Start state: {self.start_state}\n"
               f"Final states: {self.final_states}\n"
               f"Transitions: \n" + "\n".join(f" {state} -- {symbol} --> {next_state}"
                                              for state, transitions in self.transitions.items()
                                              for symbol, next_state in transitions.items()))

    def string_belongs_to_language(self, input_string):
        current_state = self.start_state
        print(f"Starting state: {current_state}")
    
        for symbol in input_string:
            if symbol not in self.alphabet:
                print(f"Rejected: {symbol} is not in the alphabet")
                return False
        
            if current_state not in self.transitions or symbol not in self.transitions[current_state]:
                print(f"Rejected: No transition for {symbol} from state {current_state}")
                return False

            next_state = self.transitions[current_state][symbol]
        
            if isinstance(next_state, set):
                next_state = next(iter(next_state))  # Choose a single state (assuming DFA)

            current_state = next_state
            print(f"Transitioned to: {current_state}")
        return current_state in self.final_states

    def to_regular_grammar(self):
        from Grammar import Grammar  
        rules = {state: [] for state in self.states}
        terminals = set()

    # Convert transitions to grammar rules and print them
        print("\nRegular Grammar Productions:")
        for state, transitions in self.transitions.items():
            productions = []
            for symbol, next_states in transitions.items():
                terminals.add(symbol)
                for next_state in next_states:
                    productions.append(f"{symbol} {next_state}")
                    print(f"{state} -> {symbol} {next_state}")

            rules[state] = productions

    # Add and print epsilon transitions for final states
        for final_state in self.final_states:
            rules[final_state].append("ε")
            print(f"{final_state} -> ε")

        print("\nGrammar Components:")
        print(f"Non-terminals: {set(self.states)}")
        print(f"Terminals: {terminals}")
        print(f"Start symbol: {self.start_state}")

        return Grammar(
            terminals=terminals,
            non_terminals=set(self.states),
            start_symbol=self.start_state,
            rules=rules
    )


    def check_type(self):
        is_ndfa = False
        transition_map = {}

        for state, transitions in self.transitions.items():
            for symbol, next_states in transitions.items():
                if not isinstance(next_states, set):  # Ensure it's a set
                    next_states = {next_states}

                key = (state, symbol)

                if key in transition_map:
                    is_ndfa = True  # Multiple transitions for the same (state, symbol)
                    transition_map[key].update(next_states)
                else:
                    transition_map[key] = next_states

        # Check if any key has multiple transitions
        for (state, symbol), states in transition_map.items():
            if len(states) > 1:
                is_ndfa = True
                print(f"\nThe FA is non-deterministic because from state '{state}' on symbol '{symbol}', it can transition to multiple states: {states}")

        # Special case: If the start state has multiple transitions, it's immediately an NFA
        if len(self.transitions.get(self.start_state, {})) > 1:
            is_ndfa = True
            print("\nThe FA is non-deterministic because the start state has multiple outgoing transitions.")

        if is_ndfa:
            print("\nThe FA is an NFA.")
            return "NFA"
        else:
            print("\nThe FA is a DFA.")
            return "DFA"

    def nfa_to_dfa(self):
        dfa_states = []
        dfa_transitions = defaultdict(dict)
        dfa_final_states = set()

        start_state = frozenset([self.start_state])  # Use frozenset for unique state combinations
        unprocessed_states = [start_state]
        dfa_states.append(start_state)

        while unprocessed_states:
            current_dfa_state = unprocessed_states.pop()
            for symbol in self.alphabet:
                next_state = set()
                for nfa_state in current_dfa_state:
                    if nfa_state in self.transitions and symbol in self.transitions[nfa_state]:
                        next_state.update(self.transitions[nfa_state][symbol])

                if next_state:
                    next_state_frozen = frozenset(next_state)
                    if next_state_frozen not in dfa_states:
                        unprocessed_states.append(next_state_frozen)
                        dfa_states.append(next_state_frozen)

                    dfa_transitions[current_dfa_state][symbol] = next_state_frozen

                    if any(state in self.final_states for state in next_state):
                        dfa_final_states.add(next_state_frozen)

        return FiniteAutomation(
            states=[tuple(state) for state in dfa_states],
            alphabet=self.alphabet,
            transitions={tuple(k): {sym: tuple(v) for sym, v in trans.items()} for k, trans in dfa_transitions.items()},
            start_state=tuple(start_state),
            final_states=[tuple(state) for state in dfa_final_states]
        )


# Example Usage
states = ['q0', 'q1', 'q2', 'q3']
alphabets = ['a', 'b', 'c']
start = 'q0'
finals = ['q3']
transitions = {
    'q0': {'a': {'q1'}, 'b': {'q2'}},
    'q1': {'b': {'q2', 'q1'}},  
    'q2': {'c': {'q3'}},
    'q3': {'a': {'q1'}}
}

nfa = FiniteAutomation(states, alphabets, transitions, start, finals)

print("Original FA Type:", nfa.check_type())
automaton_type = nfa.check_type()
print("Original FA Type:", automaton_type)
dfa = nfa.nfa_to_dfa()

print("\nConverted DFA:")
print(dfa)
