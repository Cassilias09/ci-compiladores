from syntatic_analysis.nodes import BaseNode

class ComparisonNode(BaseNode):
    def __init__(self, left: BaseNode, operator: str, right: BaseNode):
        self.left = left
        self.operator = operator
        self.right = right

    def __repr__(self):
        return f"ComparisonNode(left={self.left}, operator={self.operator}, right={self.right})"

    def display(self, identation: int = 0):
        print((" " * identation) + self.operator)
        self.left.display(identation + 1)
        self.right.display(identation + 1)

    def generate_code(self):
        left_code = self.left.generate_code()
        right_code = self.right.generate_code()
        code = (
            f"{right_code}\n"
            + "push %rax\n"
            + f"{left_code}\n"
            + "pop %rbx\n"
            + self._operator_to_code()
        )
        return code

    def _operator_to_code(self):
        match self.operator:
            case "==":
                return "cmp %rbx, %rax\nxor %rcx, %rcx\nsetz %cl\nmov %rcx, %rax\n"
            case "<":
                return "cmp %rbx, %rax\nxor %rcx, %rcx\nsetl %cl\nmov %rcx, %rax\n"
            case ">":
                return "cmp %rbx, %rax\nxor %rcx, %rcx\nsetg %cl\nmov %rcx, %rax\n"
            case _:
                raise ValueError(f"Comparison operator '{self.operator}' not supported.")
