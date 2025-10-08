from syntatic_analysis.nodes import BaseNode

class UnaryOperationNode(BaseNode):
    def __init__(self, operator: str, operand: BaseNode):
        self.operator = operator
        self.operand = operand

    def display(self, identation: int = 0):
        print((" " * identation) + self.operator)
        self.operand.display(identation + 1)

    def generate_code(self):
        code = self.operand.generate_code()
        
        if self.operator == '!':
            code += "\ncmp $0, %rax\n"
            code += "sete %al\n"
            code += "movzx %al, %rax\n"

        else:
            raise ValueError(f"Unary operator '{self.operator}' not supported for code generation.")

        return code