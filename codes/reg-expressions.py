import re
import random

def generate_valid_strings(pattern, count=10):
    results = []

    for _ in range(count):
        if pattern == r"M?N{2}(O|P){3}Q*R+":
            m_part = random.choice(['', 'M'])
            n_part = 'NN'
            op_part = ''.join(random.choices(['O', 'P'], k=3))
            q_part = 'Q' * random.randint(0, 10)
            r_part = 'R' * random.randint(1, 10)
            results.append(m_part + n_part + op_part + q_part + r_part)

        elif pattern == r"(X|Y|Z){3}8+(9|0){2}":
            xzy_part = ''.join(random.choices(['X', 'Y', 'Z'], k=3))
            eight_part = '8' * random.randint(1, 10)
            end_part = ''.join(random.choices(['9', '0'], k=2))
            results.append(xzy_part + eight_part + end_part)

        elif pattern == r"(H|i)(J|K)L*N?":
            first = random.choice(['H', 'i'])
            second = random.choice(['J', 'K'])
            l_part = 'L' * random.randint(0, 10)
            n_part = 'N' if random.choice([True, False]) else ''
            results.append(first + second + l_part + n_part)

    return results

def validate_strings(pattern, strings):
    compiled_pattern = re.compile(f"^{pattern}$")
    return [(string, bool(compiled_pattern.match(string))) for string in strings]

def break_down_pattern(pattern):
    components = re.findall(r'\(.*?\)|\[.*?\]|\{\d+,?\d*\}|\\?.', pattern)
    return components

def explain_component(component):
    explanations = {
        '.': "Any character except a newline",
        '*': "Zero or more repetitions",
        '+': "One or more repetitions",
        '?': "Zero or one repetition",
        '\\d': "A digit (0-9)",
        '\\w': "A word character (alphanumeric + underscore)",
        '{3}': "Exactly 3 repetitions",
        '{2}': "Exactly 2 repetitions",
        '8': "Matches the digit 8",
        '(X|Y|Z)': "Capturing group: matches X, Y, or Z",
        '(9|0)': "Capturing group: matches 9 or 0"
    }
    if component.isnumeric():
        return f"Matches the digit '{component}'"
    return explanations.get(component, f"Unknown component: {component}")

def explain_regex_processing_sequence(pattern):
    components = break_down_pattern(pattern)
    example_string = generate_valid_strings(pattern, count=1)[0]
    print(f"\nProcessing regex pattern: {pattern}")
    print(f"Example string: {example_string}\n")

    print("Step 1: Pattern Analysis")
    for idx, component in enumerate(components, 1):
        explanation = explain_component(component)
        print(f"  {idx}. {component}: {explanation}")

    print("\nStep 2: Matching Process")
    print(f"Breaking down why '{example_string}' matches the pattern:")
    
    if pattern == r"(X|Y|Z){3}8+(9|0){2}":
        first_part = example_string[:3]
        print(f"  '{first_part}' matches (X|Y|Z){{3}} -> Three characters from X, Y, or Z")
        pos = 3
        while pos < len(example_string) and example_string[pos] == '8':
            pos += 1
        
        middle_part = example_string[3:pos]
        print(f"  '{middle_part}' matches 8+ -> One or more occurrences of digit 8")
        
        last_part = example_string[pos:]
        print(f"  '{last_part}' matches (9|0){{2}} -> Two digits that are either 9 or 0")
    
    elif pattern == r"M?N{2}(O|P){3}Q*R+":
        pos = 0
        
        if example_string.startswith('M'):
            print(f"  'M' matches M? -> Optional M character")
            pos = 1
        
        nn_part = example_string[pos:pos+2]
        print(f"  '{nn_part}' matches N{{2}} -> Exactly two N characters")
        pos += 2
        
        op_part = example_string[pos:pos+3]
        print(f"  '{op_part}' matches (O|P){{3}} -> Three characters that are either O or P")
        pos += 3
        
        q_start = pos
        while pos < len(example_string) and example_string[pos] == 'Q':
            pos += 1
        
        if pos > q_start:
            q_part = example_string[q_start:pos]
            print(f"  '{q_part}' matches Q* -> Zero or more Q characters")
        else:
            print(f"  '' matches Q* -> Zero Q characters")
        
        r_part = example_string[pos:]
        print(f"  '{r_part}' matches R+ -> One or more R characters")
    
    elif pattern == r"(H|i)(J|K)L*N?":
        print(f"  '{example_string[0]}' matches (H|i) -> Either H or i")
        print(f"  '{example_string[1]}' matches (J|K) -> Either J or K")

        pos = 2
        while pos < len(example_string) and example_string[pos] == 'L':
            pos += 1
        
        if pos > 2:
            l_part = example_string[2:pos]
            print(f"  '{l_part}' matches L* -> Zero or more L characters")
        else:
            print(f"  '' matches L* -> Zero L characters")

        if pos < len(example_string):
            print(f"  '{example_string[pos]}' matches N? -> Optional N character")
        else:
            print(f"  '' matches N? -> No N character (optional)")
    
    print(f"\nFinal verdict: The example string '{example_string}' fully matches the pattern.")



if __name__ == "__main__":
    patterns = [
        r"M?N{2}(O|P){3}Q*R+",
        r"(X|Y|Z){3}8+(9|0){2}",
        r"(H|i)(J|K)L*N?"
    ]

    for pattern in patterns:
        generated_strings = generate_valid_strings(pattern)
        print(f"\nGenerated valid strings for pattern '{pattern}':")
        for string in generated_strings:
            print(f"  - {string}")
    
        validated_results = validate_strings(pattern, generated_strings)
        print("\nValidation results:")
        for string, is_valid in validated_results:
            status = "✓" if is_valid else "✗"
            print(f"{status} {string}")
    
    explain_regex_processing_sequence(patterns[1])