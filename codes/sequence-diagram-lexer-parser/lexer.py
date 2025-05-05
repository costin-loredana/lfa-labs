from enumToken import Token, TokenType
from regexpressions import match_pattern

class Lexer:
    TOKEN_TYPES = [
        (TokenType.DIAGRAM_KEYWORD, 'sequence'),
        (TokenType.PARTICIPANT_TYPE, 'actor|object|boundary|control|entity|database'),
        (TokenType.KEYWORD, 'for|while|alt|opt|par|new|delete|activate|deactivate|note|case|if|else'),
        (TokenType.STEREOTYPE, '<<call>>|<<create>>'),
        (TokenType.OPERATOR, '==|!=|<=|>=|->|=>|-->|-x>|<->|-o>|\\|<|=|<|>'),
        (TokenType.PUNCTUATION, '[{}();:]'),
        (TokenType.STRING, '"[^"]*"'),
        (TokenType.COMMENT, '//.*|/\\*.*\\*/'),
        (TokenType.NUMBER, '\\d+'),
        (TokenType.IDENTIFIER, '[a-zA-Z_][a-zA-Z0-9_]*'),
        (TokenType.WHITESPACE, '[ \t\n\r]+'),
    ]

    def __init__(self, text):
        self.text = text
        self.tokens = []

    def tokenize(self):
        pos = 0
        line = 1
        column = 1

        while pos < len(self.text):
            match = None
            for type_, pattern in self.TOKEN_TYPES:
                result = match_pattern(pattern, self.text[pos:])
                if result:
                    value = result
                    if type_ not in [TokenType.WHITESPACE, TokenType.COMMENT]:
                        self.tokens.append(Token(type_, value, line, column))
                    newlines = value.count('\n')
                    if newlines > 0:
                        line += newlines
                        column = len(value) - value.rfind('\n')
                    else:
                        column += len(value)
                    pos += len(value)
                    match = True
                    break

            if not match:
                raise ValueError(f"Unexpected character {self.text[pos]!r} at line {line}, column {column}")

        return self.tokens

if __name__ == '__main__':
    code = '''
    sequence
    actor John
    object Obj
    -> <<call>>
    if (x == 10) {
        note "Hi"
    }
    '''
    lexer = Lexer(code)
    tokens = lexer.tokenize()
    for t in tokens:
        print(t)
