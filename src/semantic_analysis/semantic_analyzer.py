from syntatic_analysis.nodes.declaration_node import DeclarationNode, FunDeclNode, LocalVarDeclNode, GlobalVarDeclNode, FunCallNode
from syntatic_analysis.nodes.variable_node import VariableNode
from syntatic_analysis.nodes.binary_operation_node import BinaryOperationNode
from syntatic_analysis.nodes.logical_operation_node import LogicalOperationNode, LogicalAndNode, LogicalOrNode
from syntatic_analysis.nodes.unary_operation_node import UnaryOperationNode
from syntatic_analysis.nodes.comparison_node import ComparisonNode
from syntatic_analysis.nodes.assignment_node import AssignmentNode
from syntatic_analysis.nodes.code_start_node import CodeStartNode
from syntatic_analysis.nodes.program_node import ProgramNode
from syntatic_analysis.nodes.block_node import BlockNode
from syntatic_analysis.nodes.if_node import IfNode
from syntatic_analysis.nodes.while_node import WhileNode
from syntatic_analysis.nodes.return_node import ReturnNode
from semantic_analysis.symbol_table import SymbolTable



class SemanticAnalyzer:
    def __init__(self, ast):
        self.ast = ast
        self.errors = []
        self.global_table = SymbolTable()
        self.current_local_offset = None
        self.current_frame_min = None

    def analyze(self):
        self._visit(self.ast, self.global_table)
        if self.errors:
            raise Exception("Erros semânticos:\n" + "\n".join(self.errors))

    def _visit(self, node, table):
        if isinstance(node, CodeStartNode):
            for child in node._children:
                self._visit(child, table)
            return
        
        if isinstance(node, ProgramNode):
            # Processamento de declarações globais (vars e funs)
            for decl in node.global_vars:
                self._visit(decl, table)
            
            for decl in node.functions:
                self._visit(decl, table)

            # Criação do escopo para main
            main_table = table.push_scope()
            self.current_local_offset = -8
            self.current_frame_min = 0

            # bloco principal (node.result_expression é BlockNode)
            self._visit(node.result_expression, main_table)

            # Calculo do frame_size para main
            frame_size = -self.current_frame_min if self.current_frame_min < 0 else 0
            setattr(node.result_expression, "frame_size", frame_size)

            # cleanup
            self.current_local_offset = None
            self.current_frame_min = None
            return

        elif isinstance(node, BlockNode):
            block_table = table.push_scope()

            # Primeira passagem: declaração dos LocalVarDeclNode
            for stmt in node.statements:
                if isinstance(stmt, LocalVarDeclNode):
                    if block_table.lookup(stmt.name):
                        self.errors.append(f"Variável local '{stmt.name}' já declarada neste bloco.")
                    else:
                        # Se não estiver dentro de função/main, current_local_offset deve ser inicializado antes
                        if self.current_local_offset is None:
                            # declaração local fora de função/main -> erro (ou trate como global)
                            self.errors.append(f"Declaração local '{stmt.name}' fora de função/main.")
                            block_table.declare(stmt.name, 'local', offset=None)
                        else:
                            block_table.declare(stmt.name, 'local', offset=self.current_local_offset)
                            stmt.offset = self.current_local_offset
                            # atualizar frame_min
                            if self.current_local_offset < self.current_frame_min:
                                self.current_frame_min = self.current_local_offset
                            self.current_local_offset -= 8

            # Segunda passagem: visite as expressões e comandos com a tabela já populada
            for stmt in node.statements:
                # Para as declarações locais já inicializadas, visite o expression com o block_table
                self._visit(stmt, block_table)
            return
                    
        elif isinstance(node, IfNode):
            self._visit(node.condition, table)
            self._visit(node.then_body, table)
            if node.else_body:
                self._visit(node.else_body, table)
            return
                
        elif isinstance(node, WhileNode):
            self._visit(node.condition, table)
            self._visit(node.block, table)
            return
            
        elif isinstance(node, GlobalVarDeclNode):
            if table.lookup(node.name):
                self.errors.append(f"Variável global '{node.name}' já declarada.")
            else:
                table.declare(node.name, 'global')
            self._visit(node.expression, table)
            return
            
        elif isinstance(node, FunDeclNode):
            if table.lookup(node.name):
                self.errors.append(f"Função '{node.name}' já declarada.")
            else:
                table.declare(node.name, 'function', params=node.params)

            fun_table = table.push_scope()

            # parâmetros (RBP+16, +24, +32, ...)
            param_offset = 16
            for param in node.params:
                fun_table.declare(param, 'param', offset=param_offset)
                param_offset += 8

            # inicializa contadores do frame da função
            self.current_local_offset = -8
            self.current_frame_min = 0

            # 1) declare locais que estão listados em node.local_vars (se existirem)
            for local in getattr(node, "local_vars", []) or []:
                if fun_table.lookup(local.name):
                    self.errors.append(f"Variável local '{local.name}' já declarada na função '{node.name}'.")
                else:
                    fun_table.declare(local.name, 'local', offset=self.current_local_offset)
                    local.offset = self.current_local_offset
                    if self.current_local_offset < self.current_frame_min:
                        self.current_frame_min = self.current_local_offset
                    self.current_local_offset -= 8
                self._visit(local.expression, fun_table)

            # 2) visite comandos e return (eles podem conter blocos que usam o mesmo contador)
            for cmd in node.commands:
                self._visit(cmd, fun_table)
            self._visit(node.return_node, fun_table)

            # compute frame_size e anote
            frame_size = -self.current_frame_min if self.current_frame_min < 0 else 0
            setattr(node, "frame_size", frame_size)

            # limpar controladores
            self.current_local_offset = None
            self.current_frame_min = None
            return

        elif isinstance(node, LocalVarDeclNode):
            self._visit(node.expression, table)
            return
        
        elif isinstance(node, DeclarationNode):
            if table.lookup(node.name):
                self.errors.append(f"Variável '{node.name}' já declarada.")
            else:
                table.declare(node.name, 'global')
            self._visit(node.expression, table)
            return
            
        elif isinstance(node, AssignmentNode):
            var_entry = table.lookup(node.variable.name)
            if not var_entry:
                self.errors.append(f"Variável '{node.variable.name}' não declarada antes da atribuição.")
            else:
                node.variable.entry = var_entry
                # Atribui também o offset diretamente ao AssignmentNode
                if hasattr(var_entry, "offset"):
                    node.offset = var_entry.offset
            self._visit(node.expression, table)
            return
            
        elif isinstance(node, VariableNode):
            var_entry = table.lookup(node.name)
            if not var_entry:
                self.errors.append(f"Variável '{node.name}' usada sem declaração.")
            else:
                node.entry = var_entry
                if hasattr(var_entry, "offset"):
                    node.offset = var_entry.offset
            return
                    
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
            return
                
        elif isinstance(node, (BinaryOperationNode, ComparisonNode, LogicalOperationNode, LogicalAndNode, LogicalOrNode)):
            self._visit(node.left, table)
            self._visit(node.right, table)
            return
        
        elif isinstance(node, UnaryOperationNode):
            self._visit(node.operand, table)
            return
            
        elif isinstance(node, ReturnNode):
            self._visit(node.expression, table)
            return
            
        else:
            for child in getattr(node, "children", []):
                self._visit(child, table)
