from syntatic_analysis.nodes import BaseNode

class AssignmentNode(BaseNode):
    """Node representing an assignment operation in the syntactic analysis tree."""
    def __init__(self, variable, expression):
        self.variable = variable  
        self.expression = expression  
        self.offset = None  # será definido pelo SemanticAnalyzer depois

    def display(self, identation: int = 0):
        print((" " * identation) + f"Assignment: {self.variable.name}")
        self.expression.display(identation + 1)

    def generate_code(self, offset=None):
        # Se offset foi passado explicitamente, usa ele; senão tenta usar self.offset
        off = offset if offset is not None else self.offset
        if off is None:
            code = self.expression.generate_code()
            code += f"\nmov %rax, {self.variable.name}\n"
            return code
        # Gera o código para calcular a expressão de inicialização (resultado em %rax)
        code = self.expression.generate_code()
        # Move o valor de %rax para o offset da variável local no frame de pilha
        code += f"\nmov %rax, {off}(%rbp)\n"
        return code
