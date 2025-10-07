from syntatic_analysis.nodes import BaseNode

class VariableNode(BaseNode):
    def __init__(self, name):
        self.name = name
        self.entry = None # será preenchido pelo SemanticAnalyzer

    def display(self, identation: int = 0):
        print((" " * identation) + f"Variable: {self.name}")
        
    def generate_code(self):
        # Se a análise semântica anotou a entrada (entry), usamos offset quando for local/param
        entry = self.entry
        if entry and getattr(entry, "kind", None) in ("local", "param"):
            off = entry.offset
            return f"\nmov {off}(%rbp), %rax\n"
        else:
            # variável global (acesso por rótulo)
            return f"\nmov {self.name}, %rax\n"
