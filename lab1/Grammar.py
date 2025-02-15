import random
from FiniteAutomation import FiniteAutomation
class Grammar:
    def __init__(self, non_terminals, terminals, start_symbol, rules):
        self.non_terminals = set(non_terminals)
        self.terminals = set(terminals)
        self.start_symbol = start_symbol
        self.rules = rules 
        
    def is_terminal(self, symbol):
        return symbol in self.terminals
    
    def expand(self, symbol):
        return random.choice(self.rules.get(symbol, [[symbol]]))
    
    def generate_string(self, symbol = None, depth = 0, max_depth = 50):
        if symbol is None:
            symbol = self.start_symbol
        if depth > max_depth:
            return ""
        if self.is_terminal(symbol):
            return symbol
        expansion = self.expand(symbol)
        return "".join(self.generate_string(sym, depth+1, max_depth) for sym in expansion)
    
    def toFiniteAutomaton(self):
        states = self.non_terminals.copy()
        alphabet = self.terminals
        start_state = self.start_symbol
        final_states = set()
        transitions = {}

        for non_terminal, productions in self.rules.items():
            for production in productions:
                terminal = production[0]  

                if non_terminal not in transitions:
                    transitions[non_terminal] = {}

                if len(production) > 1:
                    next_state = production[1]  
                    transitions[non_terminal][terminal] = next_state
                else:
                    transitions[non_terminal][terminal] = non_terminal  
                    final_states.add(non_terminal)  

        return FiniteAutomation(states, alphabet, transitions, start_state, final_states)


    
        
