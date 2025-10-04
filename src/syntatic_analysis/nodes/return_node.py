from syntatic_analysis.nodes import BaseNode

class ReturnNode(BaseNode):
    def __init__(self, expression):
        self.expression = expression  # Expression node

    def display(self, identation: int = 0):
        print((" " * identation) + "Return")
        self.expression.display(identation + 1)

    def generate_code(self):
        code = self.expression.generate_code()
        return code
