from syntatic_analysis.nodes import BaseNode

class VariableNode(BaseNode):
    def __init__(self, name):
        self.name = name

    def display(self, identation: int = 0):
        print((" " * identation) + f"Variable: {self.name}")
        
    def generate_code(self):
        return f"    # TODO: context-aware variable access for {self.name}\n    mov {self.name}, %rax\n"