import unittest
from Grammar import Grammar
from FiniteAutomation import FiniteAutomation

class Test1(unittest.TestCase):
    def setUp(self):
        self.grammar = Grammar(
            non_terminals={'S', 'B', 'L'},
            terminals={'a', 'b', 'c'},
            start_symbol='S',
            rules={
                'S': [['a', 'B']],
                'B': [['b', 'B'], ['c', 'L']],
                'L': [['c', 'L'], ['a', 'S'], ['b']]
            }
        )
        self.fa = self.grammar.toFiniteAutomaton()  # Ensure this method exists

    def test_generated_string(self):
        unique_strings = set()
        for _ in range(4):
            generated = self.grammar.generate_string()
            unique_strings.add(generated)
            self.assertTrue(
                all(char in self.grammar.terminals for char in generated),
                f"Generated string contains invalid characters: {generated}"
            )
        self.assertEqual(len(unique_strings), 5, "Not enough unique strings generated")

    def test_conversion_to_finite_automaton(self):
        self.assertIsInstance(self.fa, FiniteAutomation, "Conversion didn't produce a finite automaton object")
        self.assertIn(self.grammar.start_symbol, self.fa.states, "Start state missing in automaton")

    def test_finite_automaton_recognition(self):
        for _ in range(4):
            string = self.grammar.generate_string()
            self.assertTrue(
                self.fa.string_belongs_to_language(string),
                f"Finite Automaton didn't accept valid string: {string}"
            )

    def test_fa_initialization(self):
        self.assertIsInstance(self.fa, FiniteAutomation, "FA is not correctly instantiated.")
        self.assertIn(self.grammar.start_symbol, self.fa.states, "Start state missing from FA.")
        self.assertGreater(len(self.fa.states), 0, "FA should have at least one state.")

    def test_state_transitions(self):
        """Test if the state transitions are correctly set."""
        for state, transitions in self.fa.transitions.items():
            for symbol, next_state in transitions.items():
                self.assertIn(symbol, self.fa.alphabet, f"Symbol {symbol} not in FA alphabet")
                self.assertIn(next_state, self.fa.states, f"Next state {next_state} not in FA states")

    def test_invalid_string_rejection(self):
        """Test if the FA correctly rejects invalid strings."""
        invalid_strings = ["xyz", "abc123", "aaaa", "bbb", "ccccc"]
        for invalid_string in invalid_strings:
            self.assertFalse(
                self.fa.string_belongs_to_language(invalid_string),
                f"FA incorrectly accepted an invalid string: {invalid_string}"
            )
    
    def test_state_transitions_sequence(self):
        """Test specific transition sequences"""
        # Test q0 -> q1 -> q2 -> q3 path
        current_state = 'q0'
        self.assertEqual(self.fa.transitions[current_state]['a'], 'q1')
        current_state = 'q1'
        self.assertEqual(self.fa.transitions[current_state]['b'], 'q2')
        current_state = 'q2'
        self.assertEqual(self.fa.transitions[current_state]['c'], 'q3')

    def test_cycle_transitions(self):
        """Test the cycle q3 -> q1 -> q1"""
        current_state = 'q3'
        self.assertEqual(self.fa.transitions[current_state]['a'], 'q1')
        current_state = 'q1'
        self.assertEqual(self.fa.transitions[current_state]['b'], 'q1')

    def test_alternative_path(self):
        """Test the alternative path q0 -> q2"""
        self.assertEqual(self.fa.transitions['q0']['b'], 'q2')

    def test_final_state_membership(self):
        """Test if q3 is the only final state"""
        self.assertEqual(self.fa.final_states, {'q3'})
        self.assertEqual(len(self.fa.final_states), 1)

if __name__ == "__main__":
    unittest.main()
