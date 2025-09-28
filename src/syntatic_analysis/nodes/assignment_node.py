from syntatic_analysis.nodes import BaseNode

class AssignmentNode(BaseNode):
    """Node representing an assignment operation in the syntactic analysis tree."""
    def __init__(self, variable, expression):
        self.variable = variable  
        self.expression = expression  

    def display(self, identation: int = 0):
        print((" " * identation) + f"Assignment: {self.variable.name}")
        self.expression.display(identation + 1)

    def generate_code(self):
        code = self.expression.generate_code()
        code += f"    # TODO: context-aware assignment for {self.variable.name}\n    mov %rax, {self.variable.name}\n"
        return code
