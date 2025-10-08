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
    def generate_code(self):
        end_label = LabelGenerator.new("AndEnd")
        
        code = self.left.generate_code()
        code += "cmp $0, %rax\n"
        code += "setne %al\n"
        code += "movzx %al, %rax\n"
        code += f"cmp $0, %rax\n"
        code += f"je {end_label}\n"
        code += self.right.generate_code()
        code += "cmp $0, %rax\n"
        code += "setne %al\n"
        code += "movzx %al, %rax\n"
        code += f"{end_label}:\n"
        return code

class LogicalOrNode(LogicalOperationNode):
    def generate_code(self):
        true_label = LabelGenerator.new("OrTrue")
        end_label = LabelGenerator.new("OrEnd")
        
        code = self.left.generate_code()
        code += "cmp $0, %rax\n"
        code += "setne %al\n"
        code += "movzx %al, %rax\n"
        code += f"jne {true_label}\n"
        code += self.right.generate_code()
        code += "cmp $0, %rax\n"
        code += "setne %al\n"
        code += "movzx %al, %rax\n"
        code += f"jmp {end_label}\n"
        code += f"{true_label}:\n"
        code += "mov $1, %rax\n"
        code += f"{end_label}:\n"
        return code

