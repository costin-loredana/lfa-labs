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

    def generate_string(self, symbol=None, depth=0, max_depth=50):
        if symbol is None:
            symbol = self.start_symbol
        if depth > max_depth:
            return ""
        if self.is_terminal(symbol):
            return symbol
        
        expansion = self.expand(symbol)
        return "".join(self.generate_string(sym, depth + 1, max_depth) for sym in expansion)

    def find_Chomsky_type(self):
        is_type3 = True
        is_type2 = True
        is_type1 = True
        
        for non_terminal, productions in self.rules.items():
            if non_terminal not in self.non_terminals:
                return "Type-0"  
            
            if len(non_terminal) != 1 or non_terminal not in self.non_terminals:
                is_type2 = False  

            for production in productions:
                if production == "":  
                    continue

                if all(symbol in self.terminals for symbol in production):
                    continue 
                
                if (len(production) >= 2 and 
                    all(symbol in self.terminals for symbol in production[:-1]) and 
                    production[-1] in self.non_terminals):
                    continue  
                
                is_type3 = False 

                lhs = non_terminal
                rhs = production
                if len(rhs) < len(lhs) or not any(symbol in self.non_terminals for symbol in rhs):
                    is_type1 = False  

        if is_type3:
            return "Type-3"
        if is_type2:
            return "Type-2"
        if is_type1:
            return "Type-1"
        return "Type-0"

    # def toFiniteAutomaton(self):
    #     states = self.non_terminals.copy()
    #     states.add('F')  
    #     alphabet = self.terminals
    #     start_state = self.start_symbol
    #     final_states = {'F'}  
    #     transitions = {}

    #     for non_terminal, productions in self.rules.items():
    #         for production in productions:
    #             if len(production) == 0:
    #                 continue
                
    #             terminal = production[0]

    #             if non_terminal not in transitions:
    #                 transitions[non_terminal] = {}

    #             if len(production) > 1:
    #                 next_state = production[1]
    #                 transitions[non_terminal][terminal] = next_state
    #             else:
    #                 transitions[non_terminal][terminal] = 'F'  

    #     return FiniteAutomation(states, alphabet, transitions, start_state, final_states)
