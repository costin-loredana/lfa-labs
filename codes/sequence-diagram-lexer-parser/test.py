from enumToken import TokenType
from astNodes import Diagram, Participant, Message, Note, IfBlock, WhileBlock, OptBlock, AltBlock, print_ast
from lexer import Lexer

class ParserError(Exception):
    """Custom exception for parser errors with line/position information"""
    def __init__(self, message, token=None):
        self.message = message
        self.token = token
        super().__init__(self.message)

class Parser:
    def __init__(self, tokens):
        self.tokens = tokens
        self.pos = 0

    def current(self):
        return self.tokens[self.pos] if self.pos < len(self.tokens) else None

    def peek(self, offset=1):
        """Look ahead at upcoming tokens without consuming them"""
        pos = self.pos + offset
        return self.tokens[pos] if pos < len(self.tokens) else None

    def match(self, type_):
        if self.current() and self.current().type == type_:
            tok = self.current()
            self.pos += 1
            return tok
        return None

    def expect(self, type_, error_message=None):
        """Match a token type or raise an error if not found"""
        token = self.match(type_)
        if not token:
            if not error_message:
                error_message = f"Expected token of type {type_}"
                if self.current():
                    error_message += f", but found {self.current().type} ({self.current().value})"
                else:
                    error_message += ", but reached end of input"
            raise ParserError(error_message, self.current())
        return token

    def parse(self):
        try:
            elements = []
            if not self.match(TokenType.DIAGRAM_KEYWORD):
                raise ParserError("Expected 'sequence' keyword at the beginning")

            while self.current():
                if self.current().type == TokenType.PARTICIPANT_TYPE:
                    elements.append(self.parse_participant())
                elif self.current().type == TokenType.STEREOTYPE:
                    elements.append(self.parse_message())
                elif self.current().type == TokenType.KEYWORD:
                    keyword = self.current().value
                    if keyword == 'if':
                        elements.append(self.parse_if())
                    elif keyword == 'note':
                        elements.append(self.parse_note())
                    elif keyword == 'while':
                        elements.append(self.parse_while())
                    elif keyword == 'opt':
                        elements.append(self.parse_opt())
                    elif keyword == 'alt':
                        elements.append(self.parse_alt())
                    else:
                        raise ParserError(f"Unexpected keyword: {keyword}", self.current())
                else:
                    self.pos += 1

            return Diagram(elements)
        except ParserError:
            # Re-raise the custom error
            raise
        except Exception as e:
            # Convert unexpected errors to ParserErrors with context
            raise ParserError(f"Unexpected error: {str(e)}", self.current()) from e

    def parse_participant(self):
        try:
            p_type = self.expect(TokenType.PARTICIPANT_TYPE, "Expected participant type").value
            name = self.expect(TokenType.IDENTIFIER, "Expected participant name").value
            return Participant(p_type, name)
        except ParserError:
            # Re-raise parser errors
            raise
        except Exception as e:
            raise ParserError(f"Error parsing participant: {str(e)}", self.current()) from e

    def parse_message(self):
        try:
            stereotype = self.expect(TokenType.STEREOTYPE, "Expected message stereotype").value
            direction = self.expect(TokenType.OPERATOR, "Expected message direction operator").value
            return Message(stereotype, direction)
        except ParserError:
            raise
        except Exception as e:
            raise ParserError(f"Error parsing message: {str(e)}", self.current()) from e

    def parse_note(self):
        try:
            self.expect(TokenType.KEYWORD, "Expected 'note' keyword")  # 'note'
            content = self.expect(TokenType.STRING, "Expected string content for note").value.strip('"')
            return Note(content)
        except ParserError:
            raise
        except Exception as e:
            raise ParserError(f"Error parsing note: {str(e)}", self.current()) from e

    def parse_if(self):
        try:
            self.expect(TokenType.KEYWORD, "Expected 'if' keyword")  # 'if'
            self.expect(TokenType.PUNCTUATION, "Expected opening parenthesis '('")  # '('
            condition = []
            while self.current() and self.current().type != TokenType.PUNCTUATION:
                condition.append(self.current().value)
                self.pos += 1
            
            if not condition:
                raise ParserError("Empty condition is not allowed", self.current())
                
            self.expect(TokenType.PUNCTUATION, "Expected closing parenthesis ')'")  # ')'
            self.expect(TokenType.PUNCTUATION, "Expected opening brace '{'")  # '{'

            body = self.parse_block_body()
            self.expect(TokenType.PUNCTUATION, "Expected closing brace '}'")  # '}'

            return IfBlock(' '.join(condition), body)
        except ParserError:
            raise
        except Exception as e:
            raise ParserError(f"Error parsing if block: {str(e)}", self.current()) from e

    def parse_while(self):
        try:
            self.expect(TokenType.KEYWORD, "Expected 'while' keyword")  # 'while'
            self.expect(TokenType.PUNCTUATION, "Expected opening parenthesis '('")  # '('
            condition = []
            while self.current() and self.current().type != TokenType.PUNCTUATION:
                condition.append(self.current().value)
                self.pos += 1
            
            if not condition:
                raise ParserError("Empty condition is not allowed", self.current())
                
            self.expect(TokenType.PUNCTUATION, "Expected closing parenthesis ')'")  # ')'
            self.expect(TokenType.PUNCTUATION, "Expected opening brace '{'")  # '{'

            body = self.parse_block_body()
            self.expect(TokenType.PUNCTUATION, "Expected closing brace '}'")  # '}'

            return WhileBlock(' '.join(condition), body)
        except ParserError:
            raise
        except Exception as e:
            raise ParserError(f"Error parsing while block: {str(e)}", self.current()) from e

    def parse_opt(self):
        try:
            self.expect(TokenType.KEYWORD, "Expected 'opt' keyword")  # 'opt'
            self.expect(TokenType.PUNCTUATION, "Expected opening parenthesis '('")  # '('
            condition = []
            while self.current() and self.current().type != TokenType.PUNCTUATION:
                condition.append(self.current().value)
                self.pos += 1
            
            if not condition:
                raise ParserError("Empty condition is not allowed", self.current())
                
            self.expect(TokenType.PUNCTUATION, "Expected closing parenthesis ')'")  # ')'
            self.expect(TokenType.PUNCTUATION, "Expected opening brace '{'")  # '{'

            body = self.parse_block_body()
            self.expect(TokenType.PUNCTUATION, "Expected closing brace '}'")  # '}'

            return OptBlock(' '.join(condition), body)
        except ParserError:
            raise
        except Exception as e:
            raise ParserError(f"Error parsing opt block: {str(e)}", self.current()) from e

    def parse_alt(self):
        try:
            self.expect(TokenType.KEYWORD, "Expected 'alt' keyword")  # 'alt'
        
            self.expect(TokenType.PUNCTUATION, "Expected opening parenthesis '('")  # '('
            condition = []
            while self.current() and self.current().type != TokenType.PUNCTUATION:
                condition.append(self.current().value)
                self.pos += 1
            
            if not condition:
                raise ParserError("Empty condition is not allowed", self.current())
                
            condition_str = ' '.join(condition)
            self.expect(TokenType.PUNCTUATION, "Expected closing parenthesis ')'")  # ')'
        
            self.expect(TokenType.PUNCTUATION, "Expected opening brace '{'")  # '{'
            true_body = self.parse_block_body()
            self.expect(TokenType.PUNCTUATION, "Expected closing brace '}'")  # '}'
        
            # Parse the false branch (else part)
            false_body = []
            if self.current() and self.current().type == TokenType.KEYWORD and self.current().value == 'else':
                self.match(TokenType.KEYWORD)  # 'else'
                self.expect(TokenType.PUNCTUATION, "Expected opening brace '{'")  # '{'
                false_body = self.parse_block_body()
                self.expect(TokenType.PUNCTUATION, "Expected closing brace '}'")  # '}'
        
            return AltBlock(condition_str, true_body, false_body)
        except ParserError:
            raise
        except Exception as e:
            raise ParserError(f"Error parsing alt block: {str(e)}", self.current()) from e

    def parse_block_body(self):
        try:
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
                    elif keyword == 'else':
                        # 'else' should be handled by parse_alt, not here
                        raise ParserError("Unexpected 'else' without matching 'alt'", self.current())
                    else:
                        raise ParserError(f"Unexpected keyword in block: {keyword}", self.current())
                elif self.current().type == TokenType.STEREOTYPE:
                    body.append(self.parse_message())
                elif self.current().type == TokenType.PARTICIPANT_TYPE:
                    body.append(self.parse_participant())
                else:
                    self.pos += 1
            return body
        except ParserError:
            raise
        except Exception as e:
            raise ParserError(f"Error parsing block body: {str(e)}", self.current()) from e

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
    
    try:
        lexer = Lexer(code)
        tokens = lexer.tokenize()
        
        print("TOKENS:")
        for t in tokens:
            print(t)
        
        print("\nPARSED AST:")
        parser = Parser(tokens)
        ast = parser.parse()
        print_ast(ast)
    except ParserError as e:
        print(f"Parser Error: {e.message}")
        if e.token:
            print(f"At token: {e.token}")
        
        # Show context of the error (5 tokens before and after)
        if parser.tokens and parser.pos < len(parser.tokens):
            start = max(0, parser.pos - 5)
            end = min(len(parser.tokens), parser.pos + 5)
            
            print("\nError context:")
            for i in range(start, end):
                prefix = "→ " if i == parser.pos else "  "
                print(f"{prefix}{i}: {parser.tokens[i]}")
    except Exception as e:
        print(f"Unexpected error: {str(e)}")
