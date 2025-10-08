from syntatic_analysis.nodes import BaseNode 
from syntatic_analysis.utils.label_generator import LabelGenerator

class LogicalOperationNode(BaseNode):
    """Classe base para nós lógicos, para compartilhar o construtor."""
    def __init__(self, left: BaseNode, operator: str, right: BaseNode):
        self.left = left
        self.operator = operator
        self.right = right

    def display(self, identation: int = 0):
        print((" " * identation) + self.operator)
        self.left.display(identation + 1)
        self.right.display(identation + 1)

class LogicalAndNode(LogicalOperationNode):
    """
    Nó para o operador lógico '&&' com avaliação de curto-circuito.
    """
    def generate_code(self):
        end_label = LabelGenerator.new("AndEnd")
        
        # 1. Avalia o lado esquerdo
        code = self.left.generate_code()
        
        # 2. Se for falso, pula direto para o fim (curto-circuito)
        code += "\n    # Short-circuit check for AND\n"
        code += "    cmp $0, %rax\n"
        code += f"    je {end_label}\n"
        
        # 3. Salva o resultado do lado esquerdo e avalia o direito
        code += "    push %rax\n"
        code += self.right.generate_code()
        
        # 4. Combina os dois resultados com 'and' lógico
        code += "    mov %rax, %rbx\n"
        code += "    pop %rax\n"
        code += "    and %rbx, %rax\n"
        code += "    cmp $0, %rax\n"
        code += "    setne %al\n"
        code += "    movzx %al, %rax\n"
        
        # 5. Label de fim
        code += f"\n{end_label}:\n"
        return code

class LogicalOrNode(LogicalOperationNode):
    """
    Nó para o operador lógico '||' com avaliação de curto-circuito.
    """
    def generate_code(self):
        true_label = LabelGenerator.new("OrTrue")
        end_label = LabelGenerator.new("OrEnd")
        
        # 1. Avalia o lado esquerdo
        code = self.left.generate_code()
        
        # 2. Se o lado esquerdo for verdadeiro, curto-circuita
        code += "\n    # Short-circuit check for OR\n"
        code += "    cmp $0, %rax\n"
        code += f"    jne {true_label}\n"
        
        # 3. Caso contrário, salva o resultado e avalia o lado direito
        code += "    push %rax\n"
        code += self.right.generate_code()
        
        # 4. Combina com OR lógico
        code += "    mov %rax, %rbx\n"
        code += "    pop %rax\n"
        code += "    or %rbx, %rax\n"
        code += "    cmp $0, %rax\n"
        code += "    setne %al\n"
        code += "    movzx %al, %rax\n"
        code += f"    jmp {end_label}\n"
        
        # 5. Curto-circuito (resultado verdadeiro)
        code += f"\n{true_label}:\n"
        code += "    cmp $0, %rax\n"       # normaliza o valor já existente
        code += "    setne %al\n"
        code += "    movzx %al, %rax\n"
        
        # 6. Label de fim
        code += f"\n{end_label}:\n"
        return code
