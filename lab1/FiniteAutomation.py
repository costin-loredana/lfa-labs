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