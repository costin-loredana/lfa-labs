import unittest
from FiniteAutomation import FiniteAutomation

class TestVariant10(unittest.TestCase):
    def setUp(self):
        self.states = {'q0', 'q1', 'q2', 'q3'}
        self.alphabet = {'a', 'b', 'c'}
        self.transitions = {
            'q0': {'a': 'q1', 'b': 'q2', 'c': None},
            'q1': {'a': None, 'b': 'q1', 'c': None},  # Note: q1 has self-loop with 'b'
            'q2': {'a': None, 'b': None, 'c': 'q3'},
            'q3': {'a': 'q1', 'b': None, 'c': None}
    }
        self.start_state = 'q0'
        self.final_states = {'q3'}
        self.fa = FiniteAutomation(
        self.states,
        self.alphabet,
        self.transitions,
        self.start_state,
        self.final_states
    )


    def test_valid_transitions(self):
        # Test q0 -> q1 transition with 'a'
        self.assertEqual(self.fa.transitions['q0']['a'], 'q1')
        # Test q1 -> q2 transition with 'b'
        self.assertEqual(self.fa.transitions['q1']['b'], 'q2')
        # Test q2 -> q3 transition with 'c'
        self.assertEqual(self.fa.transitions['q2']['c'], 'q3')
        # Test q3 -> q1 transition with 'a'
        self.assertEqual(self.fa.transitions['q3']['a'], 'q1')
        # Test q1 self-loop with 'b'
        self.assertEqual(self.fa.transitions['q1']['b'], 'q1')
        # Test q0 -> q2 transition with 'b'
        self.assertEqual(self.fa.transitions['q0']['b'], 'q2')

    def test_valid_strings(self):
        valid_strings = ['abc', 'abbc', 'bca', 'abbbc']
        for string in valid_strings:
            self.assertTrue(self.fa.string_belongs_to_language(string))

    def test_invalid_strings(self):
        invalid_strings = ['ab', 'aa', 'bbb', 'cba', 'abcc']
        for string in invalid_strings:
            self.assertFalse(self.fa.string_belongs_to_language(string))

    def test_final_state(self):
        self.assertEqual(self.fa.final_states, {'q3'})
    
    def test_is_dfa(self):
        """Verify that the automaton is indeed a DFA"""
        self.assertEqual(self.fa.check_type(), "DFA")
    
        # Verify deterministic properties
        for state in self.states:
            if state in self.transitions:
                # Each state should have exactly one transition for each input symbol
                symbols_from_state = set(self.transitions[state].keys())
                self.assertEqual(symbols_from_state, self.alphabet)
            
            # Each transition should lead to exactly one state
                for symbol in self.alphabet:
                    if symbol in self.transitions[state]:
                        next_state = self.transitions[state][symbol]
                        self.assertIsInstance(next_state, str)
                        self.assertIn(next_state, self.states)

    def test_transition_diagram(self):
        """Test the complete transition diagram"""
        transitions_to_test = [
            ('q0', 'a', 'q1'),  # δ(q0,a) = q1
            ('q1', 'b', 'q2'),  # δ(q1,b) = q2
            ('q2', 'c', 'q3'),  # δ(q2,c) = q3
            ('q3', 'a', 'q1'),  # δ(q3,a) = q1
            ('q1', 'b', 'q1'),  # δ(q1,b) = q1
            ('q0', 'b', 'q2'),  # δ(q0,b) = q2
            ]
    
        for current_state, symbol, expected_next_state in transitions_to_test:
            self.assertIn(current_state, self.transitions)
            self.assertIn(symbol, self.transitions[current_state])
            actual_next_state = self.transitions[current_state][symbol]
            self.assertEqual(actual_next_state, expected_next_state)

if __name__ == '__main__':
    unittest.main()
