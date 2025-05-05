import random

def generate_string_from_pattern(pattern):
    """
    Generate a string that matches the given regex pattern.
    Handles a variety of regex operations without third-party libraries.
    """
    def parse_pattern(pattern, start=0):
        """Recursively parse the pattern and generate a string."""
        result = []
        i = start
        
        while i < len(pattern):
            char = pattern[i]
            
            if char == '\\' and i + 1 < len(pattern):
                i += 1
                char = pattern[i]
                if char == 'd':  
                    result.append(str(random.randint(0, 9)))
                elif char == 'w': 
                    result.append(random.choice('abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789_'))
                elif char == 's':  
                    result.append(random.choice(' \t\n\r\f\v'))
                else:  
                    result.append(char)
                i += 1
                continue
            
            
            if char == '[':
                end = pattern.find(']', i)
                if end != -1:
                    char_class = pattern[i+1:end]
                    negated = char_class.startswith('^')
                    if negated:
                        char_class = char_class[1:]
                    
                    chars_to_choose = []
                    j = 0
                    while j < len(char_class):
                        if j + 2 < len(char_class) and char_class[j+1] == '-':
                            chars_to_choose.extend(chr(c) for c in range(ord(char_class[j]), ord(char_class[j+2]) + 1))
                            j += 3
                        else:
                            chars_to_choose.append(char_class[j])
                            j += 1
                    
                    if negated:
                        all_chars = [chr(c) for c in range(32, 127)]
                        chars_to_choose = [c for c in all_chars if c not in chars_to_choose]
                    
                    result.append(random.choice(chars_to_choose))
                    i = end + 1
                    continue
            
            if char == '(':
                group_start = i + 1
                count = 1
                group_end = group_start
                while group_end < len(pattern) and count > 0:
                    if pattern[group_end] == '(':
                        count += 1
                    elif pattern[group_end] == ')':
                        count -= 1
                    group_end += 1
                
                if count == 0:
                    group_end -= 1
                    group_content = pattern[group_start:group_end]
                    if '|' in group_content:
                        alternatives = group_content.split('|')
                        chosen_alt = random.choice(alternatives)
                        group_result, _ = parse_pattern(chosen_alt, 0)
                        result.append(group_result)
                    else:
                        group_result, _ = parse_pattern(group_content, 0)
                        result.append(group_result)
                    
                    i = group_end + 1
                    continue
            
            if char in '*+?{' and result:
                last_result = result.pop()
                count = 1
                if char == '*':
                    count = random.randint(0, 5)
                elif char == '+':
                    count = random.randint(1, 5)
                elif char == '?':
                    count = random.randint(0, 1)
                elif char == '{':
                    end_brace = pattern.find('}', i)
                    if end_brace != -1:
                        count_spec = pattern[i+1:end_brace]
                        if ',' in count_spec:
                            min_count, max_count = count_spec.split(',')
                            min_count = int(min_count) if min_count else 0
                            max_count = int(max_count) if max_count else 10
                            count = random.randint(min_count, max_count)
                        else:
                            count = int(count_spec)
                        i = end_brace
                result.append(last_result * count)
                i += 1
                continue
            
            if char == '.':
                result.append(random.choice('abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789'))
                i += 1
                continue
            
            result.append(char)
            i += 1
        
        return ''.join(result), i
    
    return parse_pattern(pattern)[0]

def match_pattern(pattern, text):
    if '|' in pattern:
        # Handle alternation
        for option in pattern.split('|'):
            result = match_pattern(option, text)
            if result:
                return result
        return None

    if pattern == 'sequence':
        return text.startswith('sequence') and 'sequence'

    if pattern in ['actor', 'object', 'boundary', 'control', 'entity', 'database']:
        return text.startswith(pattern) and pattern

    if pattern in ['for', 'while', 'alt', 'opt', 'par', 'new', 'delete', 'activate', 'deactivate', 'note', 'case', 'if', 'else']:
        return text.startswith(pattern) and pattern

    if pattern in ['<<call>>', '<<create>>']:
        return text.startswith(pattern) and pattern

    if pattern in ['==', '!=', '<=', '>=', '->', '=>', '-->', '-x>', '<->', '-o>', '|<', '=', '<', '>']:
        return text.startswith(pattern) and pattern

    if pattern == '[{}();:]':
        if text and text[0] in '{}();:':
            return text[0]

    if pattern == '"[^"]*"':
        if text.startswith('"'):
            end = 1
            while end < len(text) and text[end] != '"':
                end += 1
            if end < len(text):
                return text[:end+1]
        return None

    if pattern == '//.*':
        if text.startswith('//'):
            end = text.find('\n')
            return text if end == -1 else text[:end]

    if pattern == '/\\*.*\\*/':
        if text.startswith('/*'):
            end = text.find('*/')
            return text[:end+2] if end != -1 else None

    if pattern == '\\d+':
        i = 0
        while i < len(text) and text[i].isdigit():
            i += 1
        return text[:i] if i > 0 else None

    if pattern == '[a-zA-Z_][a-zA-Z0-9_]*':
        if not text or (not text[0].isalpha() and text[0] != '_'):
            return None
        i = 1
        while i < len(text) and (text[i].isalnum() or text[i] == '_'):
            i += 1
        return text[:i]

    if pattern == '[ \t\n\r]+':
        i = 0
        while i < len(text) and text[i] in ' \t\n\r':
            i += 1
        return text[:i] if i > 0 else None

    return None


def generate_multiple_strings(pattern, count=10):
    """
    Generate multiple valid strings from a given regex pattern.
    """
    return [generate_string_from_pattern(pattern) for _ in range(count)]


def explain_pattern(pattern):
    """
    Explain how a string can be constructed from a given regex pattern.
    """
    explanation = f"Pattern: {pattern}\n"
    explanation += "This pattern consists of the following components:\n"
    
    if '?' in pattern:
        explanation += "- `?` makes the preceding character or group optional.\n"
    if '*' in pattern:
        explanation += "- `*` allows zero or more occurrences of the preceding character or group.\n"
    if '+' in pattern:
        explanation += "- `+` requires at least one occurrence of the preceding character or group.\n"
    if '{' in pattern:
        explanation += "- `{n,m}` specifies a minimum and maximum number of repetitions.\n"
    if '|' in pattern:
        explanation += "- `|` provides alternatives between different characters or groups.\n"
    if '(' in pattern and ')' in pattern:
        explanation += "- `()` is used for grouping subpatterns.\n"
    if '[' in pattern and ']' in pattern:
        explanation += "- `[]` defines a character class, selecting one character from the given options.\n"
    
    explanation += "\nA valid string that can be generated from this pattern:\n"
    example_string = generate_string_from_pattern(pattern)
    explanation += f"Example: {example_string}\n"
    
    return explanation


# patterns = [
#     r"M?N{2}(O|P){3}Q*R+",
#     r"(X|Y|Z){3}8+(9|0){2}",
#     r"(H|i)(J|K)L*N?"
# ]

# for pattern in patterns:
#     print(f"Pattern: {pattern}")
#     generated_strings = generate_multiple_strings(pattern)
#     for string in generated_strings:
#         print(f"Generated String: {string}")
#     print("===============================")

# print(explain_pattern(patterns[2]))