import unittest
from Grammar import Grammar
from FiniteAutomation import FiniteAutomation

class Test1(unittest.TestCase):
    def setUp(self):
        self.grammar = Grammar( non_terminals = {'S', 'B', 'L'},
                       terminals = {'a', 'b', 'c'},
                       start_symbol = 'S',
                       rules = {
                                'S' : [['a', 'B']],
                                'B' : [['b', 'B'], ['c', 'L']],
                                'L' : [['c', 'L'], ['a', 'S'], ['b']]})
        self.fa = self.grammar.toFiniteAutomaton()

    def test_generated_string(self):
        unique_strings = set()
        for _ in range(5):
            generated = self.grammar.generate_string()
            unique_strings.add(generated)
            self.assertTrue(all(char in self.grammar.terminals for char in generated),
                        f"Generated string contains invalid characters: {generated}")
        self.assertEqual(len(unique_strings), 5, "Not enough unique strings generated")
    
    def test_conversion_to_finite_automaton(self):
        self.assertIsInstance(self.fa, FiniteAutomation, "Conversion didn't produce a finite automaton object")
        self.assertIn(self.grammar.start_symbol, fa.states, "Start state missing in automaton")
    
    def test_finite_automaton_recognition(self):
        for _ in range(5):
            string = self.grammar.generate_string()
            self.assertTrue(self.fa.string_belongs_to_language(string),
                            f"Finite Automaton did't accept valid strings: {string}")
            
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

    # def test_valid_string_recognition(self):
    #     """Test if the FA correctly recognizes valid strings."""
    #     for _ in range(5):
    #         valid_string = self.grammar.generate_string()
    #         self.assertTrue(self.fa.string_belongs_to_language(valid_string),
    #                         f"FA did not accept a valid string: {valid_string}")

    def test_invalid_string_rejection(self):
        """Test if the FA correctly rejects invalid strings."""
        invalid_strings = ["xyz", "abc123", "aaaa", "bbb", "ccccc"]
        for invalid_string in invalid_strings:
            self.assertFalse(self.fa.string_belongs_to_language(invalid_string),
                             f"FA incorrectly accepted an invalid string: {invalid_string}")

if __name__ == "__main__":
    unittest.main()

        