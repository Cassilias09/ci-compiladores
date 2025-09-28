from syntatic_analysis.nodes import BaseNode

class ProgramNode(BaseNode):
    def __init__(self, declarations, result_expression):
        self.declarations = declarations  # lista de DeclarationNode (declarações globais e funções)
        self.result_expression = result_expression  # nó da expressão final (o corpo do bloco 'main')

    def display(self, identation: int = 0):
        print("Program")
        for decl in self.declarations:
            decl.display(identation + 1)
        print("Result Expression:")
        self.result_expression.display(identation + 1)
        
    def generate_code(self):
        code = ""
        # 1. Geração de código para todas as declarações (variáveis globais e funções)
        for decl in self.declarations:
            code += decl.generate_code() + "\n"
            
        # 2. Início do bloco principal 'main'
        code += ".globl main\nmain:\n"
        # Prólogo simples para a função main (embora não tenha variáveis locais neste exemplo)
        code += "    push %rbp\n    mov %rsp, %rbp\n"
        
        # 3. Geração de código para o corpo do 'main' (comandos e expressão de retorno)
        code += self.result_expression.generate_code()
        
        # 4. Saída do programa usando syscall Linux
        # O resultado da expressão final já está em %rax
        # Move o status de saída (%rax) para o primeiro argumento (%rdi)
        code += "    mov %rax, %rdi\n"
        # Move o número da syscall 'exit' (60) para %rax
        code += "    mov $60, %rax\n"
        # Executa a chamada de sistema
        code += "    syscall\n"
        return code