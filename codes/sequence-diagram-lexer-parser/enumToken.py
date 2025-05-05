from enum import Enum

class TokenType(Enum):
    DIAGRAM_KEYWORD = 'DIAGRAM_KEYWORD'
    PARTICIPANT_TYPE = 'PARTICIPANT_TYPE'
    KEYWORD = 'KEYWORD'
    STEREOTYPE = 'STEREOTYPE'
    OPERATOR = 'OPERATOR'
    PUNCTUATION = 'PUNCTUATION'
    STRING = 'STRING'
    COMMENT = 'COMMENT'
    NUMBER = 'NUMBER'
    IDENTIFIER = 'IDENTIFIER'
    WHITESPACE = 'WHITESPACE'

class Token:
    def __init__(self, type_: TokenType, value, line, column):
        self.type = type_
        self.value = value
        self.line = line
        self.column = column
    
    def __repr__(self):
        return f'Token({self.type.name}, {self.value!r}, line={self.line}, column={self.column})'
