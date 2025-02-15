# Regular Grammars and Finite Automata

**Course**: Formal Languages & Finite Automata  
**Author**: Loredana Costin

---

## Theory

A grammar is an ordered quadruple G = (Vn, Vt, S, P), where Vn are the non terminal symbols, Vt are the terminal symbols, S is the start symbol and P is the set of rules the grammar is following.
There are 4 types of grammars: 
1. Recursively enumerable languages(type 0) - there are no restriction rules, but the left side should not be an empty string;
2. Context sensitive languages(type 1) - there is accepted empty string, also the length of the left side should be smaller or equal to the right side.The left side could have at least one non-terminal symbol
3. Context-free languages(type 2) - The left side should only have a one variable and the symbol should be non-terminal. 
4. Regular languages(type 3) - The left side should be a non-terminal symbol and if n the right side there is a non-terminal symbol on the right part, all the other non-terminal symbols should be placed on the right part. And also it should contain only one non-terminal symbol. Also, here is accepted empty string.

There are 3 types of finite automata: DFA(deterministic), Non-DFA(non deterministic), and epsilon NFA;
Finite automata is a finite set of states a machine can have. It is consisited of a start state, transitions, intermediate states and  then final states. Basically, it's got a set of input symbols, and is jumping through a states, based on transition functions.
In our case, we have DFA, which is a 5-tuple, consisted of a finite set of states, an alphabet, a transition function, an initial state, and a set of final states. 

---

## Objectives:

- Discover what a language is and what it needs to have in order to be considered a formal one;
- Provide the initial setup for the evolving project that you will work on during this semester.
- Get the grammar definition and do the following:  
    a. Implement a type/class for your grammar;  
    b. Add one function that would generate 5 valid strings from the language expressed by your given grammar;  
    c. Implement some functionality that would convert an object of type Grammar to one of type Finite Automaton;  
    d. For the Finite Automaton, add a method that checks if an input string can be obtained via state transitions.

---

## Implementation Description

1. **The Grammar class**  
   In this class, I implemented a method that generates a valid string from a specific grammar. I designed it to always start with the start symbol, expanding the string until it encounters a terminal symbol. I also set a maximum depth of 50 characters to prevent excessive recursion and improve performance.

    ```python
    def generate_string(self, symbol=None, depth=0, max_depth=50):
        if symbol is None:
            symbol = self.start_symbol
        if depth > max_depth:
            return ""
        if self.is_terminal(symbol):
            return symbol
        expansion = self.expand(symbol)
        return "".join(self.generate_string(sym, depth+1, max_depth) for sym in expansion)
    ```

   I also implemented a method that converts a grammar object into a finite automaton (Deterministic Finite Automaton). Here, I declared the set of states (derived from non-terminal symbols), the alphabet (derived from terminal symbols), the start state, the final states, and the set of transitions. I chose to begin with a terminal symbol, which in my case is `'a'`, transitioning to `S` (a non-terminal, as intended). The final state is also selected from non-terminal symbols, which in my case is `L`.

   ```python
   def to_finite_automaton(self):
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

        return FiniteAutomaton(states, alphabet, transitions, start_state, final_states)
    ```
2. **The FiniteAutomaton class**
    Here, I implemented a method to check whether a string belongs to the language defined by the grammar. The method verifies if the symbols exist in the current alphabet and whether the state is valid within the set of transitions. If not, the string is rejected.
    ```python
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
    ```
3. **The main script**
    In this part, I declared the specific grammar I had to work with, and made sure to not have the same string over and over again.

---
## Results and Conclusion
![The conversion from an object of grammar to an object of FA](outputs/lab1.png)
In conclusion, I can say that the program worked as intended, the grammar was respected and the final state of each word was L, because there was only one final state due to a terminal symbo - L. This ensures the fact that all of the words generated belong to the same language. 

---
## References  

1. **Online Resources:**  
   - [Neso Academy - Finite Automata](https://www.youtube.com/watch?v=62JAy4oH6lU&ab_channel=NesoAcademy)  
   - [Top GATE - Formal Languages](https://www.youtube.com/watch?v=VCx8lcsYjgA&list=PL4x4VD79Gu5rNbkj4QM_7F5U6BfLnCWoh&index=2&ab_channel=TopGATE)  

2. **Books and Slides:**  
   - [Automata Theory, Languages, & Computation - 3rd Edition (PDF)](https://mrce.in/ebooks/Automata%20Theory,%20Languages,%20&%20Computation%20Introduction%203rd%20Ed.pdf)  
   - [Course Slides (Google Drive)](https://drive.google.com/file/d/1rBGyzDN5eWMXTNeUxLxmKsf7tyhHt9Jk/view)  
