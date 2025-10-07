from syntatic_analysis.nodes import BaseNode
from syntatic_analysis.nodes.declaration_node import LocalVarDeclNode

class BlockNode(BaseNode):
    def __init__(self, statements: list):
        self.statements = statements

    def display(self, identation: int = 0):
        print((" " * identation) + "Block")
        for stmt in self.statements:
            stmt.display(identation + 1)

    def generate_code(self):
        code = ""
        for stmt in self.statements:
            if isinstance(stmt, LocalVarDeclNode):
                code += stmt.generate_code(getattr(stmt, "offset", None))
            else:
                code += stmt.generate_code()
        return code
