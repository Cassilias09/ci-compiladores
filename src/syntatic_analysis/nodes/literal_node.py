from syntatic_analysis.nodes import BaseNode


class LiteralNode(BaseNode):
    """Node representing a literal value in the syntactic analysis tree."""

    def __init__(self, value: int):
        """
        Initialize a literal node.

        :param token: The token representing the literal value.
        """
        self.value: int = value

    def __repr__(self):
        return f"LiteralNode(value={self.value})"

    def display(self, identation: int = 0):
        print((" " * identation) + self.value)
