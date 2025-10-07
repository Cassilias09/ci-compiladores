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
        
        # --- PADRÃO UNIFICADO DE AVALIAÇÃO ---
        code = (
            f"{left_code}\n"          # 1. Avalia esquerda -> %rax
            + "    push %rax\n"         # 2. Guarda na pilha
            + f"{right_code}\n"         # 3. Avalia direita -> %rax
            + "    mov %rax, %rbx\n"    # 4. Move resultado da direita para %rbx
            + "    pop %rax\n"          # 5. Recupera resultado da esquerda para %rax
            + self._operator_to_code()  # Agora: %rax=A, %rbx=B
        )
        return code

    def _operator_to_code(self):
        match self.operator:
            case "==":
                return (
                    "    cmp %rbx, %rax\n"
                    "    xor %rax, %rax\n"  # limpa o registrador inteiro
                    "    sete %al\n"
                    "    movzx %al, %rax\n"
                )
            case "!=":
                return (
                    "    cmp %rbx, %rax\n"
                    "    xor %rax, %rax\n"
                    "    setne %al\n"
                    "    movzx %al, %rax\n"
                )
            case ">":
                return (
                    "    cmp %rbx, %rax\n"
                    "    xor %rax, %rax\n"
                    "    setg %al\n"
                    "    movzx %al, %rax\n"
                )
            case "<":
                return (
                    "    cmp %rbx, %rax\n"
                    "    xor %rax, %rax\n"
                    "    setl %al\n"
                    "    movzx %al, %rax\n"
                )
            case ">=":
                return (
                    "    cmp %rbx, %rax\n"
                    "    xor %rax, %rax\n"
                    "    setge %al\n"
                    "    movzx %al, %rax\n"
                )
            case "<=":
                return (
                    "    cmp %rbx, %rax\n"
                    "    xor %rax, %rax\n"
                    "    setle %al\n"
                    "    movzx %al, %rax\n"
                )
            case _:
                raise ValueError(f"Comparison operator '{self.operator}' not supported.")
