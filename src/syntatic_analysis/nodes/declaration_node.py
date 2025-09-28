from syntatic_analysis.nodes import BaseNode

class FunDeclNode(BaseNode):
    def __init__(self, name, params, local_vars, commands, return_node):
        self.name = name
        self.params = params  # Lista de nomes dos parâmetros
        self.local_vars = local_vars  # Lista de LocalVarDeclNode
        self.commands = commands  # Lista de nós de comando
        self.return_node = return_node  # ReturnNode (nó da expressão de retorno)

    def display(self, identation: int = 0):
        print((" " * identation) + f"Function: {self.name}({', '.join(self.params)})")
        for var in self.local_vars:
            var.display(identation + 1)
        for cmd in self.commands:
            cmd.display(identation + 1)
        self.return_node.display(identation + 1)

    def generate_code(self):
        code = f"{self.name}:\n"
        # Prólogo da Função
        code += "    push %rbp\n"
        code += "    mov %rsp, %rbp\n"
        if self.local_vars:
            # Aloca espaço para variáveis locais (L * 8 bytes)
            code += f"    sub ${len(self.local_vars) * 8}, %rsp\n"
        # Inicialização das variáveis locais
        for idx, var in enumerate(self.local_vars):
            # Offset: -8, -16, ... (abaixo do RBP)
            offset = -8 * (idx + 1)
            code += var.generate_code(offset)
        # Geração de código para comandos
        for cmd in self.commands:
            code += cmd.generate_code()
        # Geração de código para a expressão de retorno (o resultado deve estar em %rax)
        code += self.return_node.generate_code()
        # Epílogo da Função
        code += "    mov %rbp, %rsp\n"  # Desaloca variáveis locais (movimenta RSP para RBP)
        code += "    pop %rbp\n"  # Restaura o RBP do chamador
        code += "    ret\n"  # Retorna ao chamador
        return code

class LocalVarDeclNode(BaseNode):
    def __init__(self, name, expression):
        self.name = name
        self.expression = expression

    def display(self, identation: int = 0):
        print((" " * identation) + f"LocalVar: {self.name}")
        self.expression.display(identation + 1)

    def generate_code(self, offset):
        # Gera o código para calcular a expressão de inicialização (resultado em %rax)
        code = self.expression.generate_code()
        # Move o valor de %rax para o offset da variável local no frame de pilha
        code += f"    mov %rax, {offset}(%rbp)\n"
        return code

class GlobalVarDeclNode(BaseNode):
    def __init__(self, name, expression):
        self.name = name
        self.expression = expression

    def display(self, identation: int = 0):
        print((" " * identation) + f"GlobalVar: {self.name}")
        self.expression.display(identation + 1)

    def generate_code(self):
        # Gera o código para calcular a expressão de inicialização (resultado em %rax)
        code = self.expression.generate_code()
        # Move o valor de %rax para o rótulo da variável global
        code += f"    mov %rax, {self.name}\n"
        return code

class FunCallNode(BaseNode):
    def __init__(self, name, args):
        self.name = name
        self.args = args  # Lista de nós de expressão (argumentos)

    def display(self, identation: int = 0):
        # Converte a lista de argumentos para string para exibição
        print((" " * identation) + f"FunCall: {self.name}({', '.join(str(a) for a in self.args)})")
        for arg in self.args:
            arg.display(identation + 1)

    def generate_code(self):
        code = ""
        # Avalia argumentos em ordem reversa e os empilha
        for arg in reversed(self.args):
            code += arg.generate_code()  # Resultado da expressão vai para %rax
            code += "    push %rax\n"  # Empilha o argumento
        code += f"    call {self.name}\n"  # Chama a função
        if self.args:
            # Limpa os argumentos da pilha (N * 8 bytes)
            code += f"    add ${len(self.args) * 8}, %rsp\n"
        # O resultado da chamada fica em %rax
        return code
        
class DeclarationNode(BaseNode):
    def __init__(self, name, expression):
        self.name = name
        self.expression = expression

    def display(self, identation: int = 0):
        print((" " * identation) + f"Declaration: {self.name}")
        self.expression.display(identation + 1)
        
    def generate_code(self):
        # Gera o código para calcular a expressão de inicialização (resultado em %rax)
        code = self.expression.generate_code()
        # Move o valor de %rax para o rótulo (uso genérico para variáveis, geralmente globais neste contexto)
        code += f"\nmov %rax, {self.name}\n"
        return code