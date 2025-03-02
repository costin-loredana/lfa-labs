class NFA:
    def __init__(self, states, alphabets, start, finals, transitions):
        self.states = states
        self.alphabets = alphabets
        self.start = start
        self.finals = finals
        self.transitions = transitions
        self.transition_table = dict()
        
        # Initialize transition table
        for state in self.states:
            for alphabet in self.alphabets:
                self.transition_table[(state, alphabet)] = []
        
        for transition in self.transitions:
            self.transition_table[(transition[0], transition[1])].append(transition[2])

    def get_transitions(self, state, symbol):
        return self.transition_table.get((state, symbol), [])

    def is_final(self, state):
        return state in self.finals


class DFA:
    def __init__(self, states, alphabets, start, finals, transitions):
        self.states = states
        self.alphabets = alphabets
        self.start = start
        self.finals = finals
        self.transitions = transitions

    def add_state(self, state, is_final=False):
        self.states.append(state)
        if is_final:
            self.finals.append(state)

    def add_transition(self, from_state, to_state, symbol):
        self.transitions.append([from_state, symbol, to_state])


def nfa_to_dfa(nfa):
    dfa_states = []
    dfa_transitions = []
    dfa_final_states = []
    start_state = (nfa.start,)

    # Initialize DFA
    dfa = DFA([], nfa.alphabets, start_state, [], [])
    dfa.add_state(str(start_state), nfa.is_final(nfa.start))

    # Stack to keep track of sets of NFA states
    unprocessed_states = [start_state]
    dfa_states.append(start_state)
    
    while unprocessed_states:
        current_dfa_state = unprocessed_states.pop()
        
        for symbol in nfa.alphabets:
            # Find where the NFA states go with the current symbol
            next_state = set()
            for nfa_state in current_dfa_state:
                next_state.update(nfa.get_transitions(nfa_state, symbol))

            if next_state:
                next_state_tuple = tuple(sorted(next_state))
                if next_state_tuple not in dfa_states:
                    unprocessed_states.append(next_state_tuple)
                    dfa_states.append(next_state_tuple)
                    dfa.add_state(str(next_state_tuple), any(nfa.is_final(state) for state in next_state_tuple))
                
                # Add transition to the DFA
                dfa.add_transition(str(current_dfa_state), str(next_state_tuple), symbol)
                
    return dfa


# Example NFA (No epsilon transitions, just simple states)
states = ['q0', 'q1', 'q2', 'q3']
alphabets = ['a', 'b', 'c']
start = 'q0'
finals = ['q3']
transitions = [
    ['q0', 'a', 'q1'],
    ['q1', 'b', 'q2'],
    ['q2', 'c', 'q3'],
    ['q3', 'a', 'q1'],
    ['q1', 'b', 'q1'],
    ['q0', 'b', 'q2']
]

nfa = NFA(states, alphabets, start, finals, transitions)

# Convert NFA to DFA
dfa = nfa_to_dfa(nfa)

# Output DFA
print("DFA States:", dfa.states)
print("DFA Final States:", dfa.finals)
print("DFA Transitions:")
for transition in dfa.transitions:
    print(f"From {transition[0]} to {transition[2]} on symbol {transition[1]}")
