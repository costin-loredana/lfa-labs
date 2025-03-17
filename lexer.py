# lexer.py
import re

TOKEN_TYPES = {
    'DIAGRAM_KEYWORD': r'\b(sequence)\b',
    
    'PARTICIPANT_TYPE': r'\b(actor|object|boundary|control|entity|database)\b',
    
    'KEYWORD': r'\b(for|while|alt|opt|par|new|delete|activate|deactivate|note|case)\b',
    
    'OPERATOR': r'->|=>|-->|-x>|<->|-o>|\|<',
    
    'PUNCTUATION': r'[{}();:]',
    'STEREOTYPE': r'<<\s*(call|send|create|destroy|return)\s*>>',
    'IDENTIFIER': r'[a-zA-Z_][a-zA-Z0-9_]*',
    'STRING': r'"[^"]*"',
    'COMMENT': r'//.*|/\*.*?\*/',
    'NUMBER': r'\d+',
    'WHITESPACE': r'\s+'
}

class Lexer:
    def __init__(self, input_text):
        self.input_text = input_text
        self.tokens = []
        self.current_line = 1
        self.current_column = 1
        self.participants = {} 
        self.errors = [] 

    def tokenize(self):
        """
        Tokenize the input text into a list of tokens.
        Returns the list of tokens.
        """
        self.tokens = []
        self.current_line = 1
        self.current_column = 1
        self.participants = {}
        self.errors = []
        
        position = 0
        while position < len(self.input_text):
            if self.input_text[position].isspace():
                if self.input_text[position] == '\n':
                    self.current_line += 1
                    self.current_column = 1
                else:
                    self.current_column += 1
                position += 1
                continue
            
            match = None
            for token_type, pattern in TOKEN_TYPES.items():
                regex = re.compile(pattern)
                match_obj = regex.match(self.input_text[position:])
                if match_obj:
                    match = (token_type, match_obj.group(0))
                    break
            
            if not match:
                invalid_end = position
                while (invalid_end < len(self.input_text) and 
                       not self.input_text[invalid_end].isspace() and 
                       self.input_text[invalid_end] not in '{}();:'):
                    invalid_end += 1
                
                invalid_token = self.input_text[position:invalid_end]
                self.errors.append({
                    'message': f"Invalid token: '{invalid_token}'",
                    'line': self.current_line,
                    'column': self.current_column
                })
                
                self.current_column += invalid_end - position
                position = invalid_end
                continue
            
            token_type, value = match
            
            if token_type == 'COMMENT':
                for char in value:
                    if char == '\n':
                        self.current_line += 1
                        self.current_column = 1
                    else:
                        self.current_column += 1
                position += len(value)
                continue
            
            if token_type == 'WHITESPACE':
                for char in value:
                    if char == '\n':
                        self.current_line += 1
                        self.current_column = 1
                    else:
                        self.current_column += 1
                position += len(value)
                continue
            
            self.tokens.append({
                'type': token_type,
                'value': value,
                'line': self.current_line,
                'column': self.current_column
            })
            
            self.current_column += len(value)
            position += len(value)
        
        return self.tokens

    def validate(self):
        """
        Validate the tokenized input for semantic correctness.
        Raises ValueError if validation fails.
        """
        participants = {}
        control_stack = []  
        
        i = 0
        while i < len(self.tokens):
            token = self.tokens[i]
            
            if token['type'] == 'PARTICIPANT_TYPE':
                j = i + 1
                while j < len(self.tokens) and self.tokens[j]['type'] in ['WHITESPACE', 'COMMENT']:
                    j += 1
                
                if j < len(self.tokens):
                    if self.tokens[j]['type'] == 'IDENTIFIER':
                        participant_name = self.tokens[j]['value']
                        participants[participant_name] = 'active'
                    elif self.tokens[j]['type'] == 'STRING':
                        participant_name = self.tokens[j]['value'].strip('"')
                        participants[participant_name] = 'active'
            
            elif token['type'] == 'KEYWORD':
                if token['value'] == 'new':
                    if i > 0 and self.tokens[i-1]['type'] == 'IDENTIFIER':
                        participant_name = self.tokens[i-1]['value']
                        participants[participant_name] = 'active'
                
                elif token['value'] == 'delete':
                    if i > 0 and self.tokens[i-1]['type'] == 'IDENTIFIER':
                        participant_name = self.tokens[i-1]['value']
                        participants[participant_name] = 'deleted'
                
                elif token['value'] in ['for', 'while', 'alt', 'opt', 'par']:
                    control_stack.append(token['value'])
            
            elif token['type'] == 'PUNCTUATION' and token['value'] == '}':
                if control_stack:
                    control_stack.pop()
            
            i += 1
        
        if control_stack:
            raise ValueError(f"Unclosed control structures: {', '.join(control_stack)}")
        
        for i, token in enumerate(self.tokens):
            if token['type'] == 'OPERATOR':
                sender = None
                receiver = None
                
                j = i - 1
                while j >= 0:
                    if self.tokens[j]['type'] == 'IDENTIFIER':
                        sender = self.tokens[j]['value']
                        break
                    j -= 1
                
                j = i + 1
                while j < len(self.tokens):
                    if self.tokens[j]['type'] == 'IDENTIFIER':
                        receiver = self.tokens[j]['value']
                        break
                    j += 1
                
                if sender and receiver:
                    if sender not in participants:
                        participants[sender] = 'active'
                    
                    if participants.get(sender) == 'deleted':
                        raise ValueError(f"Message from deleted participant '{sender}' at line {token['line']}, column {token['column']}")
                    
                    if receiver not in participants:
                        participants[receiver] = 'active'
                    
                    if participants.get(receiver) == 'deleted':
                        raise ValueError(f"Message to deleted participant '{receiver}' at line {token['line']}, column {token['column']}")
        
        if self.errors:
            error_messages = "\n".join([f"Line {e['line']}, Column {e['column']}: {e['message']}" for e in self.errors])
            raise ValueError(f"Validation errors:\n{error_messages}")

    def print_tokens(self):
        """
        Print all tokens in a readable format.
        """
        for token in self.tokens:
            print(f"Type: {token['type']}, Value: '{token['value']}', Line: {token['line']}, Column: {token['column']}")

    def get_errors(self):
        """
        Return the list of errors found during tokenization and validation.
        """
        return self.errors
