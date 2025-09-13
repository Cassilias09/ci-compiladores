from syntatic_analysis.nodes import BaseNode

class ProgramNode(BaseNode):
    def __init__(self, declarations, result_expression):
        self.declarations = declarations  # lista de DeclarationNode
        self.result_expression = result_expression  # nó da expressão final

    def display(self, identation: int = 0):
        print("Program")
        for decl in self.declarations:
            decl.display(identation + 1)
        print("Result Expression:")
        self.result_expression.display(identation + 1)
        
    def generate_code(self):
        code = ""
        for decl in self.declarations:
            code += decl.generate_code() + "\n"
        code += self.result_expression.generate_code() + "\n"
        return code