
from syntatic_analysis.nodes.declaration_node import DeclarationNode, FunDeclNode, LocalVarDeclNode, GlobalVarDeclNode, FunCallNode
from syntatic_analysis.nodes.variable_node import VariableNode
from syntatic_analysis.nodes.binary_operation_node import BinaryOperationNode
from syntatic_analysis.nodes.assignment_node import AssignmentNode
from syntatic_analysis.nodes.program_node import ProgramNode
from syntatic_analysis.nodes.block_node import BlockNode
from syntatic_analysis.nodes.return_node import ReturnNode
from semantic_analysis.symbol_table import SymbolTable



class SemanticAnalyzer:
    def __init__(self, ast):
        self.ast = ast
        self.errors = []
        self.global_table = SymbolTable()

    def analyze(self):
        self._visit(self.ast, self.global_table)
        if self.errors:
            raise Exception("Erros semânticos:\n" + "\n".join(self.errors))

    def _visit(self, node, table):
        if isinstance(node, ProgramNode):
            # Visit all global declarations (vars and functions)
            for decl in node.declarations:
                self._visit(decl, table)
            self._visit(node.result_expression, table)
        elif isinstance(node, GlobalVarDeclNode):
            if table.lookup(node.name):
                self.errors.append(f"Variável global '{node.name}' já declarada.")
            else:
                table.declare(node.name, 'global')
            self._visit(node.expression, table)
        elif isinstance(node, FunDeclNode):
            if table.lookup(node.name):
                self.errors.append(f"Função '{node.name}' já declarada.")
            else:
                table.declare(node.name, 'function', params=node.params)
            # New scope for function
            fun_table = table.push_scope()
            # Parameters: assign positive offsets (RBP+24, RBP+32, ...)
            param_offset = 24
            for param in node.params:
                fun_table.declare(param, 'param', offset=param_offset)
                param_offset += 8
            # Local variables: assign negative offsets (RBP-8, RBP-16, ...)
            local_offset = -8
            for local in node.local_vars:
                if fun_table.lookup(local.name):
                    self.errors.append(f"Variável local '{local.name}' já declarada na função '{node.name}'.")
                else:
                    fun_table.declare(local.name, 'local', offset=local_offset)
                    local_offset -= 8
                self._visit(local.expression, fun_table)
            # Visit commands and return
            for cmd in node.commands:
                self._visit(cmd, fun_table)
            self._visit(node.return_node, fun_table)
        elif isinstance(node, LocalVarDeclNode):
            # Already handled in FunDeclNode
            pass
        elif isinstance(node, DeclarationNode):
            # Legacy: treat as global var
            if table.lookup(node.name):
                self.errors.append(f"Variável '{node.name}' já declarada.")
            else:
                table.declare(node.name, 'global')
            self._visit(node.expression, table)
        elif isinstance(node, AssignmentNode):
            var_entry = table.lookup(node.variable.name)
            if not var_entry:
                self.errors.append(f"Variável '{node.variable.name}' não declarada antes da atribuição.")
            self._visit(node.expression, table)
        elif isinstance(node, VariableNode):
            var_entry = table.lookup(node.name)
            if not var_entry:
                self.errors.append(f"Variável '{node.name}' usada sem declaração.")
        elif isinstance(node, FunCallNode):
            fun_entry = table.lookup(node.name)
            if not fun_entry or fun_entry.kind != 'function':
                self.errors.append(f"Função '{node.name}' não declarada.")
            else:
                expected = len(fun_entry.params) if fun_entry.params else 0
                actual = len(node.args)
                if expected != actual:
                    self.errors.append(f"Função '{node.name}' chamada com {actual} argumento(s), mas espera {expected}.")
            for arg in node.args:
                self._visit(arg, table)
        elif isinstance(node, BinaryOperationNode):
            self._visit(node.left, table)
            self._visit(node.right, table)
        elif isinstance(node, BlockNode):
            # New scope for block
            block_table = table.push_scope()
            for cmd in getattr(node, 'commands', []):
                self._visit(cmd, block_table)
        elif isinstance(node, ReturnNode):
            self._visit(node.expression, table)
        else:
            for child in getattr(node, "children", []):
                self._visit(child, table)
