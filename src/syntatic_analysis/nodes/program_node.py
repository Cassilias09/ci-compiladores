from syntatic_analysis.nodes import BaseNode

class ProgramNode(BaseNode):
    def __init__(self, global_vars, functions, result_expression):
        self.global_vars = global_vars
        self.functions = functions
        self.result_expression = result_expression

    def display(self, identation: int = 0):
        print("Program")
        print(" Global Variables:")
        for var in self.global_vars:
            var.display(identation + 1)
        print(" Functions:")
        for func in self.functions:
            func.display(identation + 1)
        print("Result Expression (main):")
        self.result_expression.display(identation + 1)
        
    def generate_code(self):
        # 1. Definição das seções
        code = ".section .bss\n"
        
        code += "\n.section .text\n"
        code += ".globl _start\n\n"
        
        # 2. Criação do ponto de entrada _start
        code += "_start:\n"
        code += "    call main\n\n"
        
        # 3. Geração de código para as funções definidas pelo usuário
        for func in self.functions:
            code += func.generate_code() + "\n"
            
        # 4. Início do bloco principal 'main'
        code += ".globl main\nmain:\n"
        code += "push %rbp\n"
        code += "mov %rsp, %rbp\n"
        
        frame_size = getattr(self.result_expression, "frame_size", 0)
        
        if frame_size > 0:
            code += f"sub ${frame_size}, %rsp\n"
        
        # 5. Geração de código para o corpo do 'main'
        code += self.result_expression.generate_code()
        return code
    