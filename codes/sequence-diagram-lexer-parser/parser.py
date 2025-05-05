from enumToken import TokenType
from astNodes import Diagram, Participant, Message, Note, IfBlock, WhileBlock, OptBlock, AltBlock, print_ast
from lexer import Lexer

class Parser:
    def __init__(self, tokens):
        self.tokens = tokens
        self.pos = 0

    def current(self):
        return self.tokens[self.pos] if self.pos < len(self.tokens) else None

    def match(self, type_):
        if self.current() and self.current().type == type_:
            tok = self.current()
            self.pos += 1
            return tok
        return None

    def parse(self):
        elements = []
        if not self.match(TokenType.DIAGRAM_KEYWORD):
            raise SyntaxError("Expected 'sequence' keyword at the beginning")

        while self.current():
            if self.current().type == TokenType.PARTICIPANT_TYPE:
                elements.append(self.parse_participant())
            elif self.current().type == TokenType.STEREOTYPE:
                elements.append(self.parse_message())
            elif self.current().type == TokenType.KEYWORD and self.current().value == 'if':
                elements.append(self.parse_if())
            elif self.current().type == TokenType.KEYWORD and self.current().value == 'note':
                elements.append(self.parse_note())
            elif self.current().type == TokenType.KEYWORD and self.current().value == 'while':
                elements.append(self.parse_while())
            elif self.current().type == TokenType.KEYWORD and self.current().value == 'opt':
                elements.append(self.parse_opt())
            elif self.current().type == TokenType.KEYWORD and self.current().value == 'alt':
                elements.append(self.parse_alt())
            else:
                self.pos += 1

        return Diagram(elements)

    def parse_participant(self):
        p_type = self.match(TokenType.PARTICIPANT_TYPE).value
        name = self.match(TokenType.IDENTIFIER).value
        return Participant(p_type, name)

    def parse_message(self):
        stereotype = self.match(TokenType.STEREOTYPE).value
        direction = self.match(TokenType.OPERATOR).value
        return Message(stereotype, direction)

    def parse_note(self):
        self.match(TokenType.KEYWORD)  # 'note'
        content = self.match(TokenType.STRING).value.strip('"')
        return Note(content)

    def parse_if(self):
        self.match(TokenType.KEYWORD)  # 'if'
        self.match(TokenType.PUNCTUATION)  # '('
        condition = []
        while self.current() and self.current().type != TokenType.PUNCTUATION:
            condition.append(self.current().value)
            self.pos += 1
        self.match(TokenType.PUNCTUATION)  # ')'
        self.match(TokenType.PUNCTUATION)  # '{'

        body = self.parse_block_body()
        self.match(TokenType.PUNCTUATION)  # '}'

        return IfBlock(' '.join(condition), body)

    def parse_while(self):
        self.match(TokenType.KEYWORD)  # 'while'
        self.match(TokenType.PUNCTUATION)  # '('
        condition = []
        while self.current() and self.current().type != TokenType.PUNCTUATION:
            condition.append(self.current().value)
            self.pos += 1
        self.match(TokenType.PUNCTUATION)  # ')'
        self.match(TokenType.PUNCTUATION)  # '{'

        body = self.parse_block_body()
        self.match(TokenType.PUNCTUATION)  # '}'

        return WhileBlock(' '.join(condition), body)

    def parse_opt(self):
        self.match(TokenType.KEYWORD)  # 'opt'
        self.match(TokenType.PUNCTUATION)  # '('
        condition = []
        while self.current() and self.current().type != TokenType.PUNCTUATION:
            condition.append(self.current().value)
            self.pos += 1
        self.match(TokenType.PUNCTUATION)  # ')'
        self.match(TokenType.PUNCTUATION)  # '{'

        body = self.parse_block_body()
        self.match(TokenType.PUNCTUATION)  # '}'

        return OptBlock(' '.join(condition), body)

    def parse_alt(self):
        self.match(TokenType.KEYWORD)  # 'alt'
    
        self.match(TokenType.PUNCTUATION)  # '('
        condition = []
        while self.current() and self.current().type != TokenType.PUNCTUATION:
            condition.append(self.current().value)
            self.pos += 1
        condition_str = ' '.join(condition)
        self.match(TokenType.PUNCTUATION)  # ')'
    
        self.match(TokenType.PUNCTUATION)  # '{'
        true_body = self.parse_block_body()
        self.match(TokenType.PUNCTUATION)  # '}'
    
    # Parse the false branch (else part)
        false_body = []
        if self.current() and self.current().type == TokenType.KEYWORD and self.current().value == 'else':
            self.match(TokenType.KEYWORD)  # 'else'
            self.match(TokenType.PUNCTUATION)  # '{'
            false_body = self.parse_block_body()
            self.match(TokenType.PUNCTUATION)  # '}'
    
        return AltBlock(condition_str, true_body, false_body)


    def parse_block_body(self):
        body = []
        while self.current() and self.current().value != '}':
            if self.current().type == TokenType.KEYWORD:
                keyword = self.current().value
                if keyword == 'note':
                    body.append(self.parse_note())
                elif keyword == 'if':
                    body.append(self.parse_if())
                elif keyword == 'while':
                    body.append(self.parse_while())
                elif keyword == 'opt':
                    body.append(self.parse_opt())
                elif keyword == 'alt':
                    body.append(self.parse_alt())
                else:
                    self.pos += 1
            elif self.current().type == TokenType.STEREOTYPE:
                body.append(self.parse_message())
            elif self.current().type == TokenType.PARTICIPANT_TYPE:
                body.append(self.parse_participant())
            else:
                self.pos += 1
        return body

# === Example Usage ===
if __name__ == "__main__":
    code = """sequence
    actor John
    <<call>> ->
    if (x == 10) {
        note "Hi"
        while (y < 5) {
            note "Looping"
        }
    }
    opt (z > 0) {
        note "Optional path"
    }
    alt (a == b) {
        note "A equals B"
    } else {
        note "A not equals B"
    }
    """
    
    lexer = Lexer(code)
    tokens = lexer.tokenize()
    
    print("TOKENS:")
    for t in tokens:
        print(t)
    
    print("\nPARSED AST:")
    parser = Parser(tokens)
    ast = parser.parse()
    print_ast(ast)
