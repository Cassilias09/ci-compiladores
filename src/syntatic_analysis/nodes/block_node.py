from syntatic_analysis.nodes import BaseNode

class BlockNode(BaseNode):
    def __init__(self, statements: list):
        self.statements = statements

    def display(self, identation: int = 0):
        print((" " * identation) + "Block")
        for stmt in self.statements:
            stmt.display(identation + 1)

    def generate_code(self):
        return "\n".join(stmt.generate_code() for stmt in self.statements)
