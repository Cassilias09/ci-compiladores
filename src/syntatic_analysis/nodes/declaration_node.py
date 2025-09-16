from syntatic_analysis.nodes import BaseNode

class DeclarationNode(BaseNode):
    def __init__(self, name, expression):
        self.name = name
        self.expression = expression

    def display(self, identation: int = 0):
        print((" " * identation) + f"Declaration: {self.name}")
        self.expression.display(identation + 1)
        
    def generate_code(self):
        code = self.expression.generate_code()
        code += f"\nmov %rax, {self.name}\n"
        return code