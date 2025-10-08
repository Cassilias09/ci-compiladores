from syntatic_analysis.nodes import BaseNode

class VariableNode(BaseNode):
    def __init__(self, name):
        self.name = name
        self.entry = None

    def display(self, identation: int = 0):
        print((" " * identation) + f"Variable: {self.name}")
        
    def generate_code(self):
        entry = self.entry
        if entry and getattr(entry, "kind", None) in ("local", "param"):
            off = entry.offset
            return f"\nmov {off}(%rbp), %rax\n"
        else:
            return f"\nmov {self.name}, %rax\n"
