import re
from enum import Enum, auto
from typing import Dict, List, Set, Tuple, Optional, Any
from dataclasses import dataclass, field

# Token definition
class TokenType(Enum):
    DIAGRAM_KEYWORD = auto()
    PARTICIPANT_TYPE = auto()
    CONTROL_KEYWORD = auto()
    LIFECYCLE_KEYWORD = auto()
    NOTE_KEYWORD = auto()
    SYNC_OPERATOR = auto()
    ASYNC_OPERATOR = auto()
    RETURN_OPERATOR = auto()
    XSYNC_OPERATOR = auto()
    TWO_WAY_OPERATOR = auto()
    TIMEOUT_OPERATOR = auto()
    BULKING_OPERATOR = auto()
    STEREOTYPE_CALL = auto()
    STEREOTYPE_SEND = auto()
    STEREOTYPE_CREATE = auto()
    STEREOTYPE_DESTROY = auto()
    STEREOTYPE_RETURN = auto()
    IDENTIFIER = auto()
    STRING = auto()
    COLON = auto()
    SEMICOLON = auto()
    LEFT_BRACE = auto()
    RIGHT_BRACE = auto()
    LEFT_PAREN = auto()
    RIGHT_PAREN = auto()
    SCOPE_OPERATOR = auto()
    COMMENT = auto()
    WHITESPACE = auto()


@dataclass
class Token:
    type: TokenType
    value: str
    line: int
    column: int


@dataclass
class DiagnosticMessage:
    message: str
    line: int
    column: int
    severity: str = "error"  # "error" or "warning"


@dataclass
class ParticipantInfo:
    type: str
    state: str  # 'declared', 'active', 'inactive', 'deleted'
    class_name: Optional[str] = None
    package: Optional[str] = None


@dataclass
class SyncMessageInfo:
    line: int
    column: int
    returned: bool = False


class TokenDefinitions:
    """Class responsible for token pattern definitions"""
    
    @staticmethod
    def get_token_patterns() -> Dict[TokenType, str]:
        return {
            TokenType.DIAGRAM_KEYWORD: r'\b(sequence)\b',
            TokenType.PARTICIPANT_TYPE: r'\b(actor|object|boundary|control|entity|database)\b',
            TokenType.CONTROL_KEYWORD: r'\b(for|while|alt|opt|par|case)\b',
            TokenType.LIFECYCLE_KEYWORD: r'\b(new|delete|activate|deactivate)\b',
            TokenType.NOTE_KEYWORD: r'\b(note)\b',
            TokenType.SYNC_OPERATOR: r'->',
            TokenType.ASYNC_OPERATOR: r'=>',
            TokenType.RETURN_OPERATOR: r'-->',
            TokenType.XSYNC_OPERATOR: r'-x>',
            TokenType.TWO_WAY_OPERATOR: r'<->',
            TokenType.TIMEOUT_OPERATOR: r'-o>',
            TokenType.BULKING_OPERATOR: r'\|<',
            TokenType.STEREOTYPE_CALL: r'<<\s*call\s*>>',
            TokenType.STEREOTYPE_SEND: r'<<\s*send\s*>>',
            TokenType.STEREOTYPE_CREATE: r'<<\s*create\s*>>',
            TokenType.STEREOTYPE_DESTROY: r'<<\s*destroy\s*>>',
            TokenType.STEREOTYPE_RETURN: r'<<\s*return\s*>>',
            TokenType.IDENTIFIER: r'[a-zA-Z_][a-zA-Z0-9_]*',
            TokenType.STRING: r'"[^"]*"',
            TokenType.COLON: r':',
            TokenType.SEMICOLON: r';',
            TokenType.LEFT_BRACE: r'{',
            TokenType.RIGHT_BRACE: r'}',
            TokenType.LEFT_PAREN: r'\(',
            TokenType.RIGHT_PAREN: r'\)',
            TokenType.SCOPE_OPERATOR: r'::',
            TokenType.COMMENT: r'//.*|/\*.*?\*/',
            TokenType.WHITESPACE: r'\s+'
        }


class Tokenizer:
    """Class responsible for tokenizing input text"""
    
    def __init__(self):
        self.token_patterns = TokenDefinitions.get_token_patterns()
        self.compiled_patterns = {
            token_type: re.compile(pattern) 
            for token_type, pattern in self.token_patterns.items()
        }
        
    def tokenize(self, input_text: str) -> Tuple[List[Token], List[DiagnosticMessage]]:
        tokens = []
        diagnostics = []
        
        position = 0
        line = 1
        column = 1
        
        while position < len(input_text):
            # Handle whitespace separately for line/column tracking
            if input_text[position].isspace():
                if input_text[position] == '\n':
                    line += 1
                    column = 1
                else:
                    column += 1
                position += 1
                continue
            
            # Try to match a token
            match = None
            for token_type, pattern in self.compiled_patterns.items():
                match_obj = pattern.match(input_text[position:])
                if match_obj:
                    match = (token_type, match_obj.group(0))
                    break
            
            if not match:
                # Handle invalid token
                invalid_end = position
                while (invalid_end < len(input_text) and 
                       not input_text[invalid_end].isspace() and 
                       input_text[invalid_end] not in '{}();:'):
                    invalid_end += 1
                
                invalid_token = input_text[position:invalid_end]
                diagnostics.append(DiagnosticMessage(
                    message=f"Invalid token: '{invalid_token}'",
                    line=line,
                    column=column
                ))
                
                column += invalid_end - position
                position = invalid_end
                continue
            
            token_type, value = match
            
            # Skip comments and whitespace
            if token_type in [TokenType.COMMENT, TokenType.WHITESPACE]:
                for char in value:
                    if char == '\n':
                        line += 1
                        column = 1
                    else:
                        column += 1
                position += len(value)
                continue
            
            # Add token to the list
            tokens.append(Token(
                type=token_type,
                value=value,
                line=line,
                column=column
            ))
            
            column += len(value)
            position += len(value)
        
        return tokens, diagnostics


class ParticipantTracker:
    """Class responsible for tracking participant state"""
    
    def __init__(self):
        self.participants: Dict[str, ParticipantInfo] = {}
        self.active_participants: Set[str] = set()
        self.object_instances: Set[str] = set()
        self.classes: Set[str] = set()
        self.packages: Set[str] = set()
    
    def declare_participant(self, name: str, participant_type: str, 
                           class_name: Optional[str] = None, 
                           package: Optional[str] = None) -> bool:
        """Declare a new participant. Returns True if successful, False if already exists."""
        if name in self.participants:
            return False
        
        self.participants[name] = ParticipantInfo(
            type=participant_type,
            state='inactive',
            class_name=class_name,
            package=package
        )
        
        if name:
            self.object_instances.add(name)
        
        if class_name:
            self.classes.add(class_name)
        
        if package:
            self.packages.add(package)
            
        return True
    
    def activate_participant(self, name: str) -> bool:
        """Activate a participant. Returns True if successful."""
        if name not in self.participants:
            return False
        
        if self.participants[name].state == 'deleted':
            return False
        
        self.participants[name].state = 'active'
        self.active_participants.add(name)
        return True
    
    def deactivate_participant(self, name: str) -> bool:
        """Deactivate a participant. Returns True if successful."""
        if name not in self.participants:
            return False
        
        if self.participants[name].state == 'deleted':
            return False
        
        self.participants[name].state = 'inactive'
        if name in self.active_participants:
            self.active_participants.remove(name)
        return True
    
    def delete_participant(self, name: str) -> bool:
        """Delete a participant. Returns True if successful."""
        if name not in self.participants:
            return False
        
        if self.participants[name].state == 'deleted':
            return False
        
        self.participants[name].state = 'deleted'
        if name in self.active_participants:
            self.active_participants.remove(name)
        return True
    
    def create_participant(self, name: str) -> bool:
        """Create a new participant (for 'new' keyword). Returns True if successful."""
        if name in self.participants and self.participants[name].state != 'deleted':
            return False
        
        self.participants[name] = ParticipantInfo(
            type='object',  # Default type for new objects
            state='active'
        )
        self.active_participants.add(name)
        return True
    
    def is_participant_valid(self, name: str) -> bool:
        """Check if a participant exists and is not deleted."""
        return name in self.participants and self.participants[name].state != 'deleted'
    
    def is_participant_active(self, name: str) -> bool:
        """Check if a participant is active."""
        return name in self.participants and self.participants[name].state == 'active'


class MessageTracker:
    """Class responsible for tracking message state"""
    
    def __init__(self):
        self.sync_messages: Dict[Tuple[str, str], SyncMessageInfo] = {}
        self.message_stack: List[Any] = []
    
    def add_sync_message(self, sender: str, receiver: str, line: int, column: int) -> None:
        """Add a synchronous message to track for return validation."""
        self.sync_messages[(sender, receiver)] = SyncMessageInfo(line=line, column=column)
    
    def add_return_message(self, sender: str, receiver: str) -> bool:
        """Add a return message. Returns True if it matches a previous sync message."""
        # Swap sender and receiver for return message validation
        if (receiver, sender) in self.sync_messages:
            self.sync_messages[(receiver, sender)].returned = True
            return True
        return False
    
    def get_unreturned_messages(self) -> List[Tuple[Tuple[str, str], SyncMessageInfo]]:
        """Get all synchronous messages that haven't been returned."""
        return [(pair, info) for pair, info in self.sync_messages.items() 
                if not info.returned]


class ControlFlowTracker:
    """Class responsible for tracking control flow structures"""
    
    def __init__(self):
        self.control_stack: List[Tuple[str, int, int]] = []  # (type, line, column)
    
    def push_control(self, control_type: str, line: int, column: int) -> None:
        """Push a control structure onto the stack."""
        self.control_stack.append((control_type, line, column))
    
    def pop_control(self) -> Optional[Tuple[str, int, int]]:
        """Pop a control structure from the stack. Returns None if stack is empty."""
        if not self.control_stack:
            return None
        return self.control_stack.pop()
    
    def peek_control(self) -> Optional[Tuple[str, int, int]]:
        """Peek at the top control structure. Returns None if stack is empty."""
        if not self.control_stack:
            return None
        return self.control_stack[-1]


class SemanticValidator:
    """Class responsible for semantic validation of tokens"""
    
    def __init__(self):
        self.participant_tracker = ParticipantTracker()
        self.message_tracker = MessageTracker()
        self.control_flow_tracker = ControlFlowTracker()
        self.diagnostics: List[DiagnosticMessage] = []
    
    def validate(self, tokens: List[Token]) -> List[DiagnosticMessage]:
        """Validate the tokens for semantic correctness."""
        self.diagnostics = []
        
        # Check if we have a sequence diagram
        if not tokens or tokens[0].type != TokenType.DIAGRAM_KEYWORD:
            self.diagnostics.append(DiagnosticMessage(
                message="Diagram must start with 'sequence' keyword",
                line=1,
                column=1
            ))
            return self.diagnostics
        
        # Process tokens
        i = 0
        in_diagram = False
        in_participant_section = True  # Initially assume we're in the participant section
        
        while i < len(tokens):
            token = tokens[i]
            
            # Handle diagram start
            if token.type == TokenType.DIAGRAM_KEYWORD:
                if in_diagram:
                    self.diagnostics.append(DiagnosticMessage(
                        message="Nested sequence diagrams are not allowed",
                        line=token.line,
                        column=token.column
                    ))
                in_diagram = True
                i += 1
                continue
            
            # Handle diagram name (optional)
            if in_diagram and (token.type == TokenType.STRING or token.type == TokenType.IDENTIFIER):
                i += 1
                continue
            
            # Handle diagram opening brace
            if in_diagram and token.type == TokenType.LEFT_BRACE:
                i += 1
                continue
            
            # Handle diagram closing brace
            if in_diagram and token.type == TokenType.RIGHT_BRACE:
                in_diagram = False
                i += 1
                continue
            
            # Handle participant declarations
            if in_diagram and token.type == TokenType.PARTICIPANT_TYPE:
                i = self._validate_participant_declaration(tokens, i)
                continue
            
            # After first interaction, we're no longer in participant section
            if in_diagram and token.type in [
                TokenType.SYNC_OPERATOR, TokenType.ASYNC_OPERATOR, 
                TokenType.RETURN_OPERATOR, TokenType.XSYNC_OPERATOR, 
                TokenType.TWO_WAY_OPERATOR, TokenType.TIMEOUT_OPERATOR, 
                TokenType.BULKING_OPERATOR, TokenType.CONTROL_KEYWORD, 
                TokenType.LIFECYCLE_KEYWORD
            ]:
                in_participant_section = False
            
            # Handle messages
            if in_diagram and not in_participant_section and token.type == TokenType.IDENTIFIER:
                i = self._validate_message(tokens, i)
                continue
            
            # Handle control flow
            if in_diagram and not in_participant_section and token.type == TokenType.CONTROL_KEYWORD:
                i = self._validate_control_flow(tokens, i)
                continue
            
            i += 1
        
        # Check for unreturned synchronous messages
        for (sender, receiver), info in self.message_tracker.get_unreturned_messages():
            self.diagnostics.append(DiagnosticMessage(
                message=f"Synchronous message from '{sender}' to '{receiver}' has no matching return",
                line=info.line,
                column=info.column,
                severity="warning"
            ))
        
        return self.diagnostics
    
    def _validate_participant_declaration(self, tokens: List[Token], index: int) -> int:
        """Validate a participant declaration. Returns the new index."""
        token = tokens[index]
        participant_type = token.value
        
        # Look for participant name
        j = index + 1
        while j < len(tokens) and tokens[j].type in [TokenType.WHITESPACE, TokenType.COMMENT]:
            j += 1
        
        if j < len(tokens):
            participant_name = None
            class_name = None
            package = None
            
            # Handle different object naming patterns
            if tokens[j].type == TokenType.IDENTIFIER:
                participant_name = tokens[j].value
                
                # Check for object:class pattern
                if j + 1 < len(tokens) and tokens[j+1].type == TokenType.COLON:
                    j += 1  # Skip colon
                    
                    # Get class name
                    if j + 1 < len(tokens) and tokens[j+1].type == TokenType.IDENTIFIER:
                        j += 1
                        class_name = tokens[j].value
                        
                        # Check for class::package pattern
                        if j + 1 < len(tokens) and tokens[j+1].type == TokenType.SCOPE_OPERATOR:
                            j += 1  # Skip ::
                            
                            # Get package name
                            if j + 1 < len(tokens) and tokens[j+1].type == TokenType.IDENTIFIER:
                                j += 1
                                package = tokens[j].value
            
            elif tokens[j].type == TokenType.STRING:
                participant_name = tokens[j].value.strip('"')
            
            elif tokens[j].type == TokenType.COLON:
                # Handle :class pattern (class without instance)
                j += 1
                if j < len(tokens) and tokens[j].type == TokenType.IDENTIFIER:
                    class_name = tokens[j].value
                    
                    # Check for class::package pattern
                    if j + 1 < len(tokens) and tokens[j+1].type == TokenType.SCOPE_OPERATOR:
                        j += 1  # Skip ::
                        
                        # Get package name
                        if j + 1 < len(tokens) and tokens[j+1].type == TokenType.IDENTIFIER:
                            j += 1
                            package = tokens[j].value
            
            # Validate participant
            if participant_name:
                # Check for duplicate participant names
                if not self.participant_tracker.declare_participant(
                    participant_name, participant_type, class_name, package
                ):
                    self.diagnostics.append(DiagnosticMessage(
                        message=f"Duplicate participant name: '{participant_name}'",
                        line=token.line,
                        column=token.column
                    ))
            
            # Skip to semicolon
            while j < len(tokens) and tokens[j].type != TokenType.SEMICOLON:
                j += 1
            
            return j + 1  # Move past semic
        return index + 1
    def _validate_message(self, tokens: List[Token], index: int) -> int:
        """Validate a message. Returns the new index."""
        token = tokens[index]
        sender = token.value
        
        # Validate sender exists
        if not self.participant_tracker.is_participant_valid(sender):
            self.diagnostics.append(DiagnosticMessage(
                message=f"Undeclared participant: '{sender}'",
                line=token.line,
                column=token.column
            ))
        
        # Look for message operator
        j = index + 1
        while j < len(tokens) and tokens[j].type not in [
            TokenType.SYNC_OPERATOR, TokenType.ASYNC_OPERATOR, 
            TokenType.RETURN_OPERATOR, TokenType.XSYNC_OPERATOR, 
            TokenType.TWO_WAY_OPERATOR, TokenType.TIMEOUT_OPERATOR, 
            TokenType.BULKING_OPERATOR, TokenType.LIFECYCLE_KEYWORD
        ]:
            j += 1
        
        if j < len(tokens):
            operator_token = tokens[j]
            
            # Handle lifecycle events
            if operator_token.type == TokenType.LIFECYCLE_KEYWORD:
                return self._handle_lifecycle_event(tokens, j, sender)
            
            # Handle message operators
            if operator_token.type in [
                TokenType.SYNC_OPERATOR, TokenType.ASYNC_OPERATOR, 
                TokenType.RETURN_OPERATOR, TokenType.XSYNC_OPERATOR, 
                TokenType.TWO_WAY_OPERATOR, TokenType.TIMEOUT_OPERATOR, 
                TokenType.BULKING_OPERATOR
            ]:
                return self._handle_message_operator(tokens, j, sender)
        
        return index + 1
    
    def _handle_lifecycle_event(self, tokens: List[Token], index: int, participant: str) -> int:
        """Handle a lifecycle event. Returns the new index."""
        token = tokens[index]
        lifecycle_event = token.value
        
        # Use a dictionary to map lifecycle events to handler methods
        lifecycle_handlers = {
            'new': self._handle_new_event,
            'delete': self._handle_delete_event,
            'activate': self._handle_activate_event,
            'deactivate': self._handle_deactivate_event
        }
        
        # Call the appropriate handler
        if lifecycle_event in lifecycle_handlers:
            lifecycle_handlers[lifecycle_event](participant, token)
        
        # Skip to semicolon
        j = index + 1
        while j < len(tokens) and tokens[j].type != TokenType.SEMICOLON:
            j += 1
        
        return j + 1  # Move past semicolon
    
    def _handle_new_event(self, participant: str, token: Token) -> None:
        """Handle a 'new' lifecycle event."""
        if not self.participant_tracker.create_participant(participant):
            self.diagnostics.append(DiagnosticMessage(
                message=f"Participant '{participant}' already exists and cannot be created again",
                line=token.line,
                column=token.column
            ))
    
    def _handle_delete_event(self, participant: str, token: Token) -> None:
        """Handle a 'delete' lifecycle event."""
        if not self.participant_tracker.is_participant_valid(participant):
            self.diagnostics.append(DiagnosticMessage(
                message=f"Cannot delete undeclared participant: '{participant}'",
                line=token.line,
                column=token.column
            ))
        elif not self.participant_tracker.delete_participant(participant):
            self.diagnostics.append(DiagnosticMessage(
                message=f"Participant '{participant}' is already deleted",
                line=token.line,
                column=token.column
            ))
    
    def _handle_activate_event(self, participant: str, token: Token) -> None:
        """Handle an 'activate' lifecycle event."""
        if not self.participant_tracker.is_participant_valid(participant):
            self.diagnostics.append(DiagnosticMessage(
                message=f"Cannot activate undeclared participant: '{participant}'",
                line=token.line,
                column=token.column
            ))
        elif not self.participant_tracker.activate_participant(participant):
            self.diagnostics.append(DiagnosticMessage(
                message=f"Cannot activate deleted participant: '{participant}'",
                line=token.line,
                column=token.column
            ))
    
    def _handle_deactivate_event(self, participant: str, token: Token) -> None:
        """Handle a 'deactivate' lifecycle event."""
        if not self.participant_tracker.is_participant_valid(participant):
            self.diagnostics.append(DiagnosticMessage(
                message=f"Cannot deactivate undeclared participant: '{participant}'",
                line=token.line,
                column=token.column
            ))
        elif not self.participant_tracker.deactivate_participant(participant):
            self.diagnostics.append(DiagnosticMessage(
                message=f"Cannot deactivate deleted participant: '{participant}'",
                line=token.line,
                column=token.column
            ))
    
    def _handle_message_operator(self, tokens: List[Token], index: int, sender: str) -> int:
        """Handle a message operator. Returns the new index."""
        operator_token = tokens[index]
        
        # Look for receiver
        j = index + 1
        while j < len(tokens) and tokens[j].type not in [TokenType.IDENTIFIER, TokenType.STRING]:
            j += 1
        
        if j < len(tokens):
            receiver_token = tokens[j]
            receiver = receiver_token.value
            if receiver_token.type == TokenType.STRING:
                receiver = receiver.strip('"')
            
            # Validate receiver exists
            if not self.participant_tracker.is_participant_valid(receiver):
                self.diagnostics.append(DiagnosticMessage(
                    message=f"Undeclared participant: '{receiver}'",
                    line=receiver_token.line,
                    column=receiver_token.column
                ))
            
            # Implicitly activate receiver if inactive
            elif not self.participant_tracker.is_participant_active(receiver):
                self.participant_tracker.activate_participant(receiver)
            
            # Use a strategy pattern to handle different message types
            message_handlers = {
                TokenType.SYNC_OPERATOR: self._handle_sync_message,
                TokenType.ASYNC_OPERATOR: self._handle_async_message,
                TokenType.RETURN_OPERATOR: self._handle_return_message,
                TokenType.XSYNC_OPERATOR: self._handle_xsync_message,
                TokenType.TWO_WAY_OPERATOR: self._handle_two_way_message,
                TokenType.TIMEOUT_OPERATOR: self._handle_timeout_message,
                TokenType.BULKING_OPERATOR: self._handle_bulking_message
            }
            
            # Call the appropriate handler
            if operator_token.type in message_handlers:
                message_handlers[operator_token.type](sender, receiver, operator_token)
            
            # Skip to semicolon
            while j < len(tokens) and tokens[j].type != TokenType.SEMICOLON:
                j += 1
            
            return j + 1  # Move past semicolon
        
        return index + 1
    
    def _handle_sync_message(self, sender: str, receiver: str, token: Token) -> None:
        """Handle a synchronous message."""
        self.message_tracker.add_sync_message(sender, receiver, token.line, token.column)
    
    def _handle_async_message(self, sender: str, receiver: str, token: Token) -> None:
        """Handle an asynchronous message."""
        # Asynchronous messages don't require returns
        pass
    
    def _handle_return_message(self, sender: str, receiver: str, token: Token) -> None:
        """Handle a return message."""
        if not self.message_tracker.add_return_message(sender, receiver):
            self.diagnostics.append(DiagnosticMessage(
                message=f"Return message from '{sender}' to '{receiver}' has no matching synchronous call",
                line=token.line,
                column=token.column
            ))
    
    def _handle_xsync_message(self, sender: str, receiver: str, token: Token) -> None:
        """Handle an extended synchronous message."""
        self.message_tracker.add_sync_message(sender, receiver, token.line, token.column)
    
    def _handle_two_way_message(self, sender: str, receiver: str, token: Token) -> None:
        """Handle a two-way message."""
        # Two-way messages don't require returns
        pass
    
    def _handle_timeout_message(self, sender: str, receiver: str, token: Token) -> None:
        """Handle a timeout message."""
        # Timeout messages don't require returns
        pass
    
    def _handle_bulking_message(self, sender: str, receiver: str, token: Token) -> None:
        """Handle a bulking message."""
        # Bulking messages don't require returns
        pass
    
    def _validate_control_flow(self, tokens: List[Token], index: int) -> int:
        """Validate a control flow structure. Returns the new index."""
        token = tokens[index]
        keyword = token.value
        
        # Push control structure onto stack
        self.control_flow_tracker.push_control(keyword, token.line, token.column)
        
        # Find the opening brace
        brace_index = index + 1
        while brace_index < len(tokens) and tokens[brace_index].type != TokenType.LEFT_BRACE:
            brace_index += 1
            
        if brace_index >= len(tokens):
            self.diagnostics.append(DiagnosticMessage(
                message=f"Missing opening brace for {keyword} block",
                line=token.line,
                column=token.column
            ))
            return index + 1
            
        # Find the closing brace
        closing_index = brace_index + 1
        brace_count = 1
        while closing_index < len(tokens) and brace_count > 0:
            if tokens[closing_index].type == TokenType.LEFT_BRACE:
                brace_count += 1
            elif tokens[closing_index].type == TokenType.RIGHT_BRACE:
                brace_count -= 1
            closing_index += 1
            
        if brace_count > 0:
            self.diagnostics.append(DiagnosticMessage(
                message=f"Missing closing brace for {keyword} block",
                line=token.line,
                column=token.column
            ))
            return index + 1
            
        # Check for interactions inside the block
        has_interactions = False
        for i in range(brace_index + 1, closing_index - 1):
            if tokens[i].type in [
                TokenType.SYNC_OPERATOR, TokenType.ASYNC_OPERATOR, 
                TokenType.RETURN_OPERATOR, TokenType.XSYNC_OPERATOR, 
                TokenType.TWO_WAY_OPERATOR, TokenType.TIMEOUT_OPERATOR, 
                TokenType.BULKING_OPERATOR
            ]:
                has_interactions = True
                break
                
        if not has_interactions and keyword == 'loop':
            self.diagnostics.append(DiagnosticMessage(
                message="Loop block must contain at least one interaction",
                line=token.line,
                column=token.column
            ))
            
        # For loops, check for potential infinite loops
        if keyword == 'loop':
            # Simple heuristic: if there's no condition or exit mechanism visible
            has_condition = False
            for i in range(index + 1, brace_index):
                if tokens[i].type == TokenType.LEFT_PAREN:
                    has_condition = True
                    break
                    
            if not has_condition:
                self.diagnostics.append(DiagnosticMessage(
                    message="Potential infinite loop detected",
                    line=token.line,
                    column=token.column,
                    severity="warning"
                ))
        
        # Pop control structure from stack
        self.control_flow_tracker.pop_control()
                
        return closing_index
    
class Lexer:
    """Main lexer class that orchestrates the tokenization and validation process"""
    
    def __init__(self):
        self.tokenizer = Tokenizer()
        self.validator = SemanticValidator()
        
    def process(self, input_text: str) -> Dict[str, Any]:
        """
        Process the input text: tokenize and validate.
        Returns a dictionary with tokens, errors, and warnings.
        """
        # Tokenize the input
        tokens, tokenization_diagnostics = self.tokenizer.tokenize(input_text)
        
        # Validate the tokens
        validation_diagnostics = self.validator.validate(tokens)
        
        # Separate errors and warnings
        errors = [d for d in tokenization_diagnostics + validation_diagnostics if d.severity == "error"]
        warnings = [d for d in validation_diagnostics if d.severity == "warning"]
        
        return {
            "tokens": tokens,
            "errors": errors,
            "warnings": warnings,
            "success": len(errors) == 0
        }


# Example usage
if __name__ == "__main__":
    sample_input = """
    sequence "Sample Diagram" {
        actor User;
        boundary UI;
        control System;
        entity Database;
        
        User -> UI: "Login";
        UI -> System: "Validate credentials";
        System -> Database: "Query user";
        Database --> System: "User data";
        System --> UI: "Valid user";
        UI --> User: "Welcome";
        
        loop "Check notifications" {
            User -> UI: "Check notifications";
            UI -> System: "Get notifications";
            System -> Database: "Query notifications";
            Database --> System: "Notification data";
            System --> UI: "Display notifications";
            UI --> User: "Show notifications";
        }
    }
    """
    
    lexer = Lexer()
    result = lexer.process(sample_input)
    
    if result["success"]:
        print(f"Successfully processed {len(result['tokens'])} tokens")
    else:
        print(f"Found {len(result['errors'])} errors:")
        for error in result["errors"]:
            print(f"  Line {error.line}, Column {error.column}: {error.message}")
    
    if result["warnings"]:
        print(f"Found {len(result['warnings'])} warnings:")
        for warning in result["warnings"]:
            print(f"  Line {warning.line}, Column {warning.column}: {warning.message}")
    
