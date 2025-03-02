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
            current_state = self.transitions[current_state][symbol]
            print(f"Transitioned to: {current_state}")
        return current_state in self.final_states
    
    def to_regular_grammar(self):
        from Grammar import Grammar 
        rules = {state: [] for state in self.states}

        for state, transitions in self.transitions.items():
            for symbol, next_states in transitions.items():
                # Ensure next_states is a list (for handling NFAs)
                if not isinstance(next_states, list):
                    next_states = [next_states]
                for next_state in next_states:
                    rules[state].append(f"{symbol} {next_state}")

        for final_state in self.final_states:
            rules[final_state].append("ε")  

        return Grammar(
            non_terminals=set(self.states),
            terminals=set(self.alphabet),
            start_symbol=self.start_state,
            rules=rules)

    def check_type(self):
        has_epsilon_transitions = False
        is_nfa = False

        for state, transitions in self.transitions.items():
            seen_symbols = set()
            for symbol, next_states in transitions.items():
                if symbol == "ε":
                    has_epsilon_transitions = True
                if not isinstance(next_states, list):
                    next_states = [next_states]
                if len(next_states) > 1 or symbol in seen_symbols:
                    is_nfa = True
                seen_symbols.add(symbol)
        if has_epsilon_transitions:
            return "ε-NFA"  # Special type of NFA
        elif is_nfa:
            return "NFA"
        else:
            return "DFA"

    # def nfa_to_dfa(self):
    # # Create initial state tuple
    #     initial_state = (self.start_state,)
    #     states_to_process = [initial_state]
    #     dfa_states = [initial_state]
    #     dfa_transitions = []
    #     dfa_final_states = []

    #     while states_to_process:
    #         current_state = states_to_process.pop(0)
        
    #     # Check if current state is final
    #         if any(state in self.final_states for state in current_state):
    #             dfa_final_states.append(current_state)
            
    #     # Process each symbol in the alphabet
    #         for symbol in self.alphabet:
    #             next_states = set()
    #             for state in current_state:
    #                 if state in self.transitions and symbol in self.transitions[state]:
    #                     next_state = self.transitions[state][symbol]
    #                     if isinstance(next_state, list):
    #                         next_states.update(next_state)
    #                     else:
    #                         next_states.add(next_state)
                        
    #             if next_states:
    #                 next_state_tuple = tuple(sorted(next_states))
    #                 dfa_transitions.append((current_state, next_state_tuple, symbol))
                
    #                 if next_state_tuple not in dfa_states:
    #                     dfa_states.append(next_state_tuple)
    #                     states_to_process.append(next_state_tuple)

    # # Print in the exact format requested
    #     print("DFA States:", [str(state) for state in dfa_states])
    #     print("DFA Final States:", [str(state) for state in dfa_final_states])
    #     print("\nDFA Transitions:")
    #     for transition in dfa_transitions:
    #         print(f"From {transition[0]} to {transition[1]} on symbol {transition[2]}")





