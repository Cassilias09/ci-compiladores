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
        
        # Evaluate right first, then left (to match comparison semantics)
        # After this: %rax=left, %rbx=right
        code = (
            f"{right_code}\n"         # 1. Avalia direita -> %rax
            + "    push %rax\n"        # 2. Guarda na pilha
            + f"{left_code}\n"         # 3. Avalia esquerda -> %rax
            + "    pop %rbx\n"         # 4. Recupera direita para %rbx
            + self._operator_to_code() # Agora: %rax=left, %rbx=right
        )
        return code

    def _operator_to_code(self):
        match self.operator:
            case "==":
                return (
                    "    cmp %rbx, %rax\n"
                    "    sete %al\n"
                    "    movzx %al, %rax\n"
                )
            case "!=":
                return (
                    "    cmp %rbx, %rax\n"
                    "    setne %al\n"
                    "    movzx %al, %rax\n"
                )
            case ">":
                return (
                    "    cmp %rbx, %rax\n"
                    "    setg %al\n"
                    "    movzx %al, %rax\n"
                )
            case "<":
                return (
                    "    cmp %rbx, %rax\n"
                    "    setl %al\n"
                    "    movzx %al, %rax\n"
                )
            case ">=":
                return (
                    "    cmp %rbx, %rax\n"
                    "    setge %al\n"
                    "    movzx %al, %rax\n"
                )
            case "<=":
                return (
                    "    cmp %rbx, %rax\n"
                    "    setle %al\n"
                    "    movzx %al, %rax\n"
                )
            case _:
                raise ValueError(f"Comparison operator '{self.operator}' not supported.")
