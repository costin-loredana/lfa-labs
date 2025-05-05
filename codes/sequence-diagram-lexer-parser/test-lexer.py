from lexer import Lexer

# Complex sequence diagram with various features
complex_input = '''
sequence ComplexExample {
    // Define participants with different types
    actor User;
    boundary UI;
    control Controller;
    entity DataModel;
    database DB;
    object Logger;
    
    /* This is a multi-line comment
       that spans multiple lines */
    
    // Test message types with stereotypes
    User -> UI: "Enter credentials";
    UI -> Controller: "Validate" <<call>>;
    Controller => DataModel: "Check user" <<send>>;
    DataModel -> DB: "Query";
    
    // Test loops and conditions
    alt {
        case ("Valid credentials") {
            DB --> DataModel: "User found";
            DataModel --> Controller: "Valid";
            Controller --> UI: "Success";
            UI --> User: "Welcome!";
            
            // Test activation/deactivation
            activate Controller;
            Controller -> Logger: "Log successful login";
            deactivate Controller;
        }
        case ("Invalid credentials") {
            DB -x> DataModel: "No user found";
            DataModel --> Controller: "Invalid";
            Controller --> UI: "Failure";
            UI --> User: "Try again";
            
            // Test loop
            loop (3) {
                User -> UI: "Retry login";
                UI -> Controller: "Revalidate";
            }
        }
    }
    
    // Test participant lifecycle
    User new;
    Logger delete;
    
    // Test bidirectional message
    User <-> UI: "Interactive session";
    
    // Test notes
    note (info): "This diagram shows a login sequence";
    
    // Test other operators
    Controller -o> DB: "Close connection";
    DB |< Controller: "Acknowledge";
    
    // Test numbers
    par (2) {
        UI -> User: "Update UI elements";
    }
}
'''

# Create lexer instance
lexer = Lexer(complex_input)

# Tokenize the input
tokens = lexer.tokenize()

# Print token count
print(f"Total tokens found: {len(tokens)}\n")

# Count tokens by type
token_counts = {}
for token in tokens:
    token_type = token['type']
    if token_type in token_counts:
        token_counts[token_type] += 1
    else:
        token_counts[token_type] = 1

print("Token counts by type:")
for token_type, count in token_counts.items():
    print(f"{token_type}: {count}")
print()

# Test specific token types
diagram_keywords = [token['value'] for token in tokens if token['type'] == 'DIAGRAM_KEYWORD']
participant_types = [token['value'] for token in tokens if token['type'] == 'PARTICIPANT_TYPE']
keywords = [token['value'] for token in tokens if token['type'] == 'KEYWORD']
operators = [token['value'] for token in tokens if token['type'] == 'OPERATOR']
stereotypes = [token['value'] for token in tokens if token['type'] == 'STEREOTYPE']
identifiers = [token['value'] for token in tokens if token['type'] == 'IDENTIFIER']
strings = [token['value'] for token in tokens if token['type'] == 'STRING']
numbers = [token['value'] for token in tokens if token['type'] == 'NUMBER']

print(f"DIAGRAM_KEYWORD: {diagram_keywords}")
print(f"PARTICIPANT_TYPE: {participant_types}")
print(f"KEYWORD: {keywords}")
print(f"OPERATOR: {operators}")
print(f"STEREOTYPE: {stereotypes}")
print(f"IDENTIFIER (first 10): {identifiers[:10]}...")
print(f"STRING: {strings}")
print(f"NUMBER: {numbers}")
print()

# Test validation
try:
    lexer.validate()
    print("Validation successful!")
except ValueError as e:
    print(f"Validation error: {e}")

# Test with invalid tokens
invalid_input = '''
sequence InvalidExample {
    actor User;
    User @#$ System: "This has invalid tokens";
}
'''

invalid_lexer = Lexer(invalid_input)
invalid_tokens = invalid_lexer.tokenize()
print("\nTesting invalid tokens:")
print(f"Errors found: {len(invalid_lexer.get_errors())}")
for error in invalid_lexer.get_errors():
    print(f"Line {error['line']}, Column {error['column']}: {error['message']}")

# Test validation errors
validation_error_input = '''
sequence ValidationErrorExample {
    actor User;
    object System;
    
    User -> System: "Message";
    System delete;
    
    // This should cause a validation error - messaging a deleted participant
    User -> System: "Another message";
    
    // Unclosed control structure
    alt {
        case ("Test") {
            User -> User: "Test";
        // Missing closing brace
}
'''

validation_error_lexer = Lexer(validation_error_input)
validation_error_tokens = validation_error_lexer.tokenize()
print("\nTesting validation errors:")
try:
    validation_error_lexer.validate()
    print("Validation successful (unexpected)!")
except ValueError as e:
    print(f"Validation error (expected): {e}")