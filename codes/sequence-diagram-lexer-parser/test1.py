from lexer import Lexer
from test import Parser, ParserError

# Complex sequence diagram with intentional errors
complex_code = """sequence
    actor User
    participant "Authentication Service" as Auth
    participant Database
    
    # Missing arrow direction
    <<request>> 
    
    if (isLoggedIn == false) {
        User <<request>> -> Auth
        Auth <<validate>> -> Database
        
        # Missing closing parenthesis
        while (connection_active {
            Database <<query>> -> Database
            note "Checking credentials"
        }
        
        alt (credentials_valid) {
            Auth <<success>> -> User
            # Participant doesn't exist
            Auth <<log>> -> Logger
        } else {
            Auth <<failure>> -> User
            # Missing opening brace
            if (retry_count < 3) 
                note "Retry authentication"
            }
        }
    }
    
    # Unmatched closing brace
    }
    
    opt (user_preferences) {
        User <<request>> -> Database
        # Incorrect keyword
        iff (preferences_exist) {
            Database <<response>> -> User
        }
    }
"""

def test_parser_with_errors():
    try:
        lexer = Lexer(complex_code)
        tokens = lexer.tokenize()
        
        print("TOKENS:")
        for t in tokens:
            print(t)
        
        print("\nPARSING:")
        parser = Parser(tokens)
        ast = parser.parse()
        
    except ParserError as e:
        print(f"\n PARSER ERROR: {e.message}")
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
        print(f"\n⚠️ UNEXPECTED ERROR: {str(e)}")

if __name__ == "__main__":
    test_parser_with_errors()
