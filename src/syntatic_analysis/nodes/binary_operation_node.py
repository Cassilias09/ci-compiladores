from syntatic_analysis.nodes import BaseNode


class BinaryOperationNode(BaseNode):
    """Node representing a binary operation in the syntactic analysis tree."""

    def __init__(self, left: BaseNode, operator: str, right: BaseNode):
        """
        Initialize a binary operation node.

        :param left: The left operand (another node).
        :param operator: The operator token.
        :param right: The right operand (another node).
        """
        self.left: BaseNode = left
        self.operator: str = operator
        self.right: BaseNode = right

    def __repr__(self):
        return f"BinaryOperationNode(left={self.left}, operator={self.operator}, right={self.right})"

    def display(self, identation: int = 0):
        print((" " * identation) + self.operator)
        self.left.display(identation=identation + 1)
        self.right.display(identation=identation + 1)

    def generate_code(self):
        left_code = self.left.generate_code()
        right_code = self.right.generate_code()
        code = (
            f"{right_code}\n"
            + "push %rax\n"
            + f"{left_code}\n"
            + "pop %rbx\n"
            + f"{self._operator_to_code()} %rbx, %rax\n"
        )
        return code

    def _operator_to_code(self):
        match self.operator:
            case "*":
                return "mul"
            case "/":
                return "div"
            case "+":
                return "add"
            case "-":
                return "sub"
            case _:
                raise ValueError(f"Operator '{self.operator}' not supported.")
