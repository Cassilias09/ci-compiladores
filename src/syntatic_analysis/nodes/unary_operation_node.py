from syntatic_analysis.nodes import BaseNode

class UnaryOperationNode(BaseNode):
    def __init__(self, operator: str, operand: BaseNode):
        self.operator = operator
        self.operand = operand

    def generate_code(self):
        operand_code = self.operand.generate_code()
        match self.operator:
            case "!":
                return operand_code + "cmp $0, %rax\nsete %al\nmovzx %al, %rax\n"
            case _:
                raise ValueError(f"Unary operator {self.operator} not supported")