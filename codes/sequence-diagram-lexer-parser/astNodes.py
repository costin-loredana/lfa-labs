class ASTNode:
    pass

# === AST Node Classes ===
class Diagram:
    def __init__(self, elements):
        self.elements = elements

class Participant:
    def __init__(self, p_type, name):
        self.p_type = p_type
        self.name = name

class Message:
    def __init__(self, stereotype, arrow):
        self.stereotype = stereotype
        self.arrow = arrow

class Note:
    def __init__(self, content):
        self.content = content

class IfBlock:
    def __init__(self, condition, body):
        self.condition = condition
        self.body = body

class WhileBlock:
    def __init__(self, condition, body):
        self.condition = condition
        self.body = body

class OptBlock:
    def __init__(self, condition, body):
        self.condition = condition
        self.body = body

class AltBlock:
    def __init__(self, condition, true_body, false_body):
        self.condition = condition
        self.true_body = true_body
        self.false_body = false_body

# === Tree Printer ===
def print_ast(node, indent=0):
    prefix = ' ' * indent + '├── '

    if isinstance(node, Diagram):
        print('Diagram')
        for elem in node.elements:
            print_ast(elem, indent + 4)

    elif isinstance(node, Participant):
        print(f"{prefix}Participant(type='{node.p_type}', name='{node.name}')")

    elif isinstance(node, Message):
        print(f"{prefix}Message(stereotype='{node.stereotype}', arrow='{node.arrow}')")

    elif isinstance(node, Note):
        print(f"{prefix}Note: {node.content}")

    elif isinstance(node, IfBlock):
        print(f"{prefix}If(condition='{node.condition}')")
        for stmt in node.body:
            print_ast(stmt, indent + 4)

    elif isinstance(node, WhileBlock):
        print(f"{prefix}While(condition='{node.condition}')")
        for stmt in node.body:
            print_ast(stmt, indent + 4)

    elif isinstance(node, OptBlock):
        print(f"{prefix}Opt(condition='{node.condition}')")
        for stmt in node.body:
            print_ast(stmt, indent + 4)

    elif isinstance(node, AltBlock):
        print(f"{prefix}Alt(condition='{node.condition}')")
        print(' ' * (indent + 4) + '├── True branch:')
        for stmt in node.true_body:
            print_ast(stmt, indent + 8)
        print(' ' * (indent + 4) + '├── False branch:')
        for stmt in node.false_body:
            print_ast(stmt, indent + 8)

    else:
        print(f"{prefix}{type(node).__name__}")

# === Example Usage ===
if __name__ == "__main__":
    ast = Diagram([
        Participant('actor', 'John'),
        Message('<<call>>', '->'),
        IfBlock('x == 10', [
            Note('Hi'),
            WhileBlock('y < 5', [
                Note('Looping')
            ])
        ]),
        OptBlock('z > 0', [
            Note('Optional path')
        ]),
        AltBlock('a == b', [
            Note('A equals B')
        ], [
            Note('A not equals B')
        ])
    ])

    print_ast(ast)
