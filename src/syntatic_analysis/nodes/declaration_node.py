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

        code += "push %rbp\n"
        code += "mov %rsp, %rbp\n"
        if self.local_vars:
            # aloca espaço para variáveis locais (L * 8 bytes)
            code += f"sub ${len(self.local_vars) * 8}, %rsp\n"

        for idx, var in enumerate(self.local_vars):
            # offset: -8, -16, ... (abaixo do RBP)
            offset = getattr(var, "offset", -8 * (idx + 1))
            code += var.generate_code(offset)

        for cmd in self.commands:
            code += cmd.generate_code()

        code += self.return_node.generate_code()

        code += "\nmov %rbp, %rsp\n"  # Desaloca variáveis locais (movimenta RSP para RBP)
        code += "pop %rbp\n"  # Restaura o RBP do chamador
        code += "ret\n"  # Retorna ao chamador
        return code

class LocalVarDeclNode(BaseNode):
    def __init__(self, name, expression):
        self.name = name
        self.expression = expression
        self.offset = None

    def display(self, identation: int = 0):
        print((" " * identation) + f"LocalVar: {self.name}")
        self.expression.display(identation + 1)

    def generate_code(self, offset=None):
        off = offset if offset is not None else self.offset
        if off is None:
            print(f"Warning: offset for local variable '{self.name}' is not set.")
            code = self.expression.generate_code()
            code += f"\nmov %rax, {self.name}\n"
            return code

        code = self.expression.generate_code()
        code += f"\nmov %rax, {off}(%rbp)\n"
        
        return code

class GlobalVarDeclNode(BaseNode):
    def __init__(self, name, expression):
        self.name = name
        self.expression = expression

    def display(self, identation: int = 0):
        print((" " * identation) + f"GlobalVar: {self.name}")
        self.expression.display(identation + 1)

    def generate_code(self):
        code = self.expression.generate_code()
        code += f"\nmov %rax, {self.name}\n"
        return code

class FunCallNode(BaseNode):
    def __init__(self, name, args):
        self.name = name
        self.args = args  # Lista de nós de expressão (argumentos)

    def display(self, identation: int = 0):
        print((" " * identation) + f"FunCall: {self.name}({', '.join(str(a) for a in self.args)})")
        for arg in self.args:
            arg.display(identation + 1)

    def generate_code(self):
        code = ""

        for arg in reversed(self.args):
            code += arg.generate_code()
            code += "\npush %rax\n"
        code += f"call {self.name}\n"
        
        if self.args:
            # limpa os argumentos da pilha (N * 8 bytes)
            code += f"add ${len(self.args) * 8}, %rsp\n"

        return code
        
class DeclarationNode(BaseNode):
    def __init__(self, name, expression):
        self.name = name
        self.expression = expression

    def display(self, identation: int = 0):
        print((" " * identation) + f"Declaration: {self.name}")
        self.expression.display(identation + 1)
        
    def generate_code(self):
        code = self.expression.generate_code()
        code += f"\nmov %rax, {self.name}\n"
        return code