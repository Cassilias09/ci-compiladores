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
        # Prólogo simples para a função main
        code += "push %rbp\nmov %rsp, %rbp\n"
        
        # 3. Geração de código para o corpo do 'main' (comandos e expressão de retorno)
        code += self.result_expression.generate_code()
        return code
    