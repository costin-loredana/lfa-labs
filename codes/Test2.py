import unittest
from collections import defaultdict
from FiniteAutomation import FiniteAutomation  # Assuming class is in finite_automation.py
from Grammar import Grammar

class TestFiniteAutomation(unittest.TestCase):
    def setUp(self):
        # Define the test data
        self.states = ['q0', 'q1', 'q2', 'q3']
        self.alphabet = ['a', 'b', 'c']
        self.start_state = 'q0'
        self.final_states = ['q3']
        self.transitions = {
            'q0': {'a': {'q1'}, 'b': {'q2'}},
            'q1': {'b': {'q2', 'q1'}},  
            'q2': {'c': {'q3'}},
            'q3': {'a': {'q1'}}
        }

        # Initialize the NFA
        self.nfa = FiniteAutomation(self.states, self.alphabet, self.transitions, self.start_state, self.final_states)

    def test_initialization(self):
        # Test initialization of the class
        self.assertEqual(self.nfa.states, self.states)
        self.assertEqual(self.nfa.alphabet, self.alphabet)
        self.assertEqual(self.nfa.start_state, self.start_state)
        self.assertEqual(self.nfa.final_states, self.final_states)
        self.assertEqual(self.nfa.transitions, self.transitions)

    def test_string_belongs_to_language(self):
        print("\n Check if it belongs to language")
        self.assertTrue(self.nfa.string_belongs_to_language("abc"))  # Should reach q3
        self.assertFalse(self.nfa.string_belongs_to_language("abb"))  # Stuck in q2
        self.assertFalse(self.nfa.string_belongs_to_language("acd"))  # Invalid symbol 'd'
        self.assertFalse(self.nfa.string_belongs_to_language(""))  # Empty string not accepted

    def test_check_type(self):
        print("\n Check if the type of FA")
        fa = FiniteAutomation(self.states, self.alphabet, self.transitions, self.start_state, self.final_states)
        self.assertEqual(fa.check_type(), "NFA")  # NFA should be detected

    def test_nfa_to_dfa(self):
        print("\n Conversion from NFA to DFA")
        fa = FiniteAutomation(self.states, self.alphabet, self.transitions, self.start_state, self.final_states)
        dfa = fa.nfa_to_dfa()
        self.assertEqual(dfa.check_type(), "NFA")  # The converted FA should be a DFA

    def test_to_regular_grammar(self):
        grammar = self.nfa.to_regular_grammar()
        self.assertIsInstance(grammar, Grammar)
        self.assertEqual(grammar.start_symbol, self.start_state)
    
    # Verify specific productions exist
        self.assertIn('q0', grammar.rules)
        self.assertIn('a q1', grammar.rules['q0'])
        self.assertIn('b q2', grammar.rules['q0'])
    
        self.assertIn('q1', grammar.rules)
        self.assertIn('b q1', grammar.rules['q1'])
        self.assertIn('b q2', grammar.rules['q1'])
    
        self.assertIn('q2', grammar.rules)
        self.assertIn('c q3', grammar.rules['q2'])
    
        self.assertIn('q3', grammar.rules)
        self.assertIn('a q1', grammar.rules['q3'])
        self.assertIn('ε', grammar.rules['q3'])


    def test_repr(self):
        repr_str = repr(self.nfa)
        self.assertIn("Finite Automation", repr_str)
        self.assertIn("States:", repr_str)
        self.assertIn("Transitions:", repr_str)

if __name__ == '__main__':
    unittest.main()
