from syntatic_analysis.nodes import BaseNode
from syntatic_analysis.utils.label_generator import LabelGenerator


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
        
        # --- PADRÃO UNIFICADO DE AVALIAÇÃO ---
        code = (
            f"{left_code}\n"
            + "    push %rax\n"
            + f"{right_code}\n"
            + "    mov %rax, %rbx\n"
            + "    pop %rax\n"
            + self._operator_to_code()
        )
        return code

    def _operator_to_code(self):
        # Agora as operações estão na ordem correta: %rax (A) op %rbx (B)
        match self.operator:
            case "*":
                return "    imul %rbx, %rax\n" # Usa imul para multiplicação segura
            case "/":
                return "    xor %rdx, %rdx\n" + "    div %rbx\n" # A em %rax / B em %rbx
            case "+":
                return "    add %rbx, %rax\n" # A + B
            case "-":
                return "    sub %rbx, %rax\n" # A - B
            case _:
                raise ValueError(f"Operator '{self.operator}' not supported.")
