from syntatic_analysis.nodes import BaseNode


class BinaryOperationNode(BaseNode):
    """Node representing a binary operation in the syntactic analysis tree."""

    def __init__(self, left, operator, right):
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
