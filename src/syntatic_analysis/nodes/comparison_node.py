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
            f"{left_code}\n"
            + "push %rax\n"
            + f"{right_code}\n"
            + "pop %rbx\n"
            + self._operator_to_code()
        )
        return code

    def _operator_to_code(self):
        match self.operator:
            case "==":
                return "cmp %rax, %rbx\nsete %al\nmovzx %al, %rax\n"
            case "<":
                return "cmp %rax, %rbx\nsetl %al\nmovzx %al, %rax\n"
            case ">":
                return "cmp %rax, %rbx\nsetg %al\nmovzx %al, %rax\n"
            case _:
                raise ValueError(f"Comparison operator '{self.operator}' not supported.")
