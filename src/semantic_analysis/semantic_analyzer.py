from syntatic_analysis.nodes.declaration_node import DeclarationNode
from syntatic_analysis.nodes.variable_node import VariableNode
from syntatic_analysis.nodes.binary_operation_node import BinaryOperationNode
from syntatic_analysis.nodes.assignment_node import AssignmentNode


class SemanticAnalyzer:
    def __init__(self, ast):
        self.ast = ast
        self.symbols = set()  # tabela de símbolos (nomes declarados)
        self.errors = []

    def analyze(self):
        self._visit(self.ast)
        if self.errors:
            raise Exception("Erros semânticos:\n" + "\n".join(self.errors))

    def _visit(self, node):
        if isinstance(node, DeclarationNode):
            # adiciona na tabela
            self.symbols.add(node.name)
            self._visit(node.expression)

        elif isinstance(node, VariableNode):
            if node.name not in self.symbols:
                self.errors.append(
                    f"Variável '{node.name}' usada sem declaração."
                )

        elif isinstance(node, BinaryOperationNode):
            self._visit(node.left)
            self._visit(node.right)

        elif isinstance(node, AssignmentNode):  # se existir
            if node.var_name not in self.symbols:
                self.errors.append(
                    f"Variável '{node.var_name}' não declarada antes da atribuição."
                )
            self._visit(node.expression)

        else:
            for child in getattr(node, "children", []):
                self._visit(child)
