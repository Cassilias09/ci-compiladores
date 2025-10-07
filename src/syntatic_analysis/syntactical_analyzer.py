from lexical_analysis.token.token import Token
from lexical_analysis.token.token_kind import TokenKind
from syntatic_analysis.nodes.binary_operation_node import BinaryOperationNode
from syntatic_analysis.nodes.code_start_node import CodeStartNode
from syntatic_analysis.nodes.declaration_node import DeclarationNode, FunCallNode, FunDeclNode, GlobalVarDeclNode, LocalVarDeclNode
from syntatic_analysis.nodes.literal_node import LiteralNode
from syntatic_analysis.nodes.program_node import ProgramNode
from syntatic_analysis.nodes.variable_node import VariableNode
from syntatic_analysis.nodes.comparison_node import ComparisonNode
from syntatic_analysis.nodes.if_node import IfNode
from syntatic_analysis.nodes.while_node import WhileNode
from syntatic_analysis.nodes.assignment_node import AssignmentNode
from syntatic_analysis.nodes.return_node import ReturnNode
from syntatic_analysis.nodes.block_node import BlockNode
from syntatic_analysis.nodes.logical_operation_node import LogicalAndNode, LogicalOrNode
from syntatic_analysis.nodes.unary_operation_node import UnaryOperationNode 
from exceptions.syntactical_exception import SyntacticalException
from exceptions.exception_list import ExceptionList

class SyntacticalAnalyzer:
    def __init__(self, tokens):
        self.tokens = tokens
        self.current_token_index = 0

        self.code_start: CodeStartNode = CodeStartNode()
        self._exceptions = []

    # ---------------- PARSE PRINCIPAL ----------------
    def parse(self):
        """
        <Programa> ::= (<Decl>)* 'main' '{' (<Cmd>)* 'return' <Exp> ';' '}'
        <Decl> ::= <VarDecl> | <FunDecl>
        """
        function_declarations = []
        global_variable_declarations = []

        while self._check_token() and self._check_token().kind in (TokenKind.FUN, TokenKind.VAR):
            if self._check_token().kind == TokenKind.FUN:
                decl = self._parse_function_declaration()
                if decl:
                    function_declarations.append(decl)
            elif self._check_token().kind == TokenKind.VAR:
                decl = self._parse_global_var_declaration()
                if decl:
                    global_variable_declarations.append(decl)
            else:
                self.advance()

        # Espera a palavra-chave 'main'
        if not self._check_token() or self._check_token().kind != TokenKind.MAIN:
            self._except(self._check_token())
            if len(self._exceptions) != 0:
                raise ExceptionList(process="Syntactical Analysis", exceptions=self._exceptions)
            return self.code_start
        self._read_token()
        if not self._check_token() or self._read_token().kind != TokenKind.BRACE_OPEN:
            self._except(self._check_token())
            if len(self._exceptions) != 0:
                raise ExceptionList(process="Syntactical Analysis", exceptions=self._exceptions)
            return self.code_start

        commands = []
        while self._check_token() and self._check_token().kind != TokenKind.RETURN:
            cmd = self._parse_cmd()
            if cmd:
                commands.append(cmd)
            else:
                if self._check_token():
                    self.advance()
                else:
                    break

        if not self._check_token() or self._check_token().kind != TokenKind.RETURN:
            self._except(self._check_token())
        else:
            return_node = self._parse_return()
            if not self._check_token() or self._check_token().kind != TokenKind.BRACE_CLOSE:
                self._except(self._check_token())
            else:
                self._read_token()

            block = BlockNode(commands + [return_node])
            program = ProgramNode(global_variable_declarations, function_declarations, block)
            self.code_start._variables = [getattr(d, 'name', None) for d in global_variable_declarations if hasattr(d, 'name')]
            self.code_start.add_child(program)

            if len(self._exceptions) != 0:
                raise ExceptionList(process="Syntactical Analysis", exceptions=self._exceptions)
            return self.code_start

        if len(self._exceptions) != 0:
            raise ExceptionList(process="Syntactical Analysis", exceptions=self._exceptions)
        return self.code_start

    def _parse_function_declaration(self):
        # 'fun' <ident> '(' <ParamSeq>? ')' '{' (<LocalVarDecl>)* (<Cmd>)* 'return' <Exp> ';' '}'
        if not self._check_token() or self._read_token().kind != TokenKind.FUN:
            self._except(self._check_token())
            return None
        name_token = self._read_token()
        if not name_token or name_token.kind != TokenKind.IDENTIFIER:
            self._except(name_token)
            return None
        if not self._check_token() or self._read_token().kind != TokenKind.PARENTHESIS_OPEN:
            self._except(self._check_token())
            return None
        params = []
        if self._check_token() and self._check_token().kind == TokenKind.IDENTIFIER:
            params.append(self._read_token().lexeme)
            while self._check_token() and self._check_token().kind == TokenKind.COMMA:
                self._read_token()
                if self._check_token() and self._check_token().kind == TokenKind.IDENTIFIER:
                    params.append(self._read_token().lexeme)
                else:
                    self._except(self._check_token())
                    break
        if not self._check_token() or self._read_token().kind != TokenKind.PARENTHESIS_CLOSE:
            self._except(self._check_token())
            return None
        if not self._check_token() or self._read_token().kind != TokenKind.BRACE_OPEN:
            self._except(self._check_token())
            return None
        local_vars = []
        while self._check_token() and self._check_token().kind == TokenKind.VAR:
            local_var = self._parse_local_var_declaration()
            if local_var:
                local_vars.append(local_var)
            else:
                self.advance()
        commands = []
        while self._check_token() and self._check_token().kind not in (TokenKind.RETURN, TokenKind.BRACE_CLOSE):
            cmd = self._parse_cmd()
            if cmd:
                commands.append(cmd)
            else:
                if self._check_token():
                    self.advance()
                else:
                    break
        if not self._check_token() or self._check_token().kind != TokenKind.RETURN:
            self._except(self._check_token())
            return None
        return_node = self._parse_return()
        if not self._check_token() or self._check_token().kind != TokenKind.BRACE_CLOSE:
            self._except(self._check_token())
            return None
        self._read_token()
        return FunDeclNode(name_token.lexeme, params, local_vars, commands, return_node)

    def _parse_local_var_declaration(self):
        # 'var' <ident> '=' <exp> ';'
        if not self._check_token() or self._read_token().kind != TokenKind.VAR:
            self._except(self._check_token())
            return None
        ident_token = self._read_token()
        if not ident_token or ident_token.kind != TokenKind.IDENTIFIER:
            self._except(ident_token)
            return None
        if not self._check_token() or self._read_token().kind != TokenKind.EQUALS:
            self._except(self._check_token())
            return None
        expr = self._parse_expression()
        if not self._check_token() or self._read_token().kind != TokenKind.SEMICOLON:
            self._except(self._check_token())
            return None
        return LocalVarDeclNode(ident_token.lexeme, expr)

    def _parse_global_var_declaration(self):
        # 'var' <ident> '=' <exp> ';'
        if not self._check_token() or self._read_token().kind != TokenKind.VAR:
            self._except(self._check_token())
            return None
        ident_token = self._read_token()
        if not ident_token or ident_token.kind != TokenKind.IDENTIFIER:
            self._except(ident_token)
            return None
        if not self._check_token() or self._read_token().kind != TokenKind.EQUALS:
            self._except(self._check_token())
            return None
        expr = self._parse_expression()
        if not self._check_token() or self._read_token().kind != TokenKind.SEMICOLON:
            self._except(self._check_token())
            return None
        return GlobalVarDeclNode(ident_token.lexeme, expr)

    # -- Commands --
    def _parse_cmd(self):
        token = self._check_token()
        if not token:
            return None

        if token.kind == TokenKind.IF:
            return self._parse_if()
        elif token.kind == TokenKind.WHILE:
            return self._parse_while()
        elif token.kind == TokenKind.IDENTIFIER:
            return self._parse_assignment()
        elif token.kind == TokenKind.BRACE_OPEN:
            return self._parse_block()
        elif token.kind == TokenKind.VAR:
            return self._parse_local_var_declaration()
        else:
            self._except(token)
            self.advance()
            return None

    # 'if' '(' <exp> ')' '{' <cmd>* '}' ('else' '{' <cmd>* '}')?
    def _parse_if(self):
        if self._read_token().kind != TokenKind.IF:
            self._except(self._check_token())
            return None

        if not self._check_token() or self._read_token().kind != TokenKind.PARENTHESIS_OPEN:
            self._except(self._check_token())
            return None

        condition = self._parse_expression()

        if not self._check_token() or self._read_token().kind != TokenKind.PARENTHESIS_CLOSE:
            self._except(self._check_token())
            return None

        if not self._check_token() or self._read_token().kind != TokenKind.BRACE_OPEN:
            self._except(self._check_token())
            return None

        then_cmds = []
        while self._check_token() and self._check_token().kind != TokenKind.BRACE_CLOSE:
            cmd = self._parse_cmd()
            if cmd:
                then_cmds.append(cmd)
            else:
                if self._check_token():
                    self.advance()
                else:
                    break

        if not self._check_token() or self._read_token().kind != TokenKind.BRACE_CLOSE:
            self._except(self._check_token())
            return None

        else_cmds = []
        if self._check_token() and self._check_token().kind == TokenKind.ELSE:
            self._read_token()
            if not self._check_token() or self._read_token().kind != TokenKind.BRACE_OPEN:
                self._except(self._check_token())
                return None
            while self._check_token() and self._check_token().kind != TokenKind.BRACE_CLOSE:
                cmd = self._parse_cmd()
                if cmd:
                    else_cmds.append(cmd)
                else:
                    if self._check_token():
                        self.advance()
                    else:
                        break
            if not self._check_token() or self._read_token().kind != TokenKind.BRACE_CLOSE:
                self._except(self._check_token())
                return None

        then_block = BlockNode(then_cmds)
        else_block = BlockNode(else_cmds) if else_cmds else None
        return IfNode(condition, then_block, else_block)

    # 'while' '(' <exp> ')' '{' <cmd>* '}'
    def _parse_while(self):
        if self._read_token().kind != TokenKind.WHILE:
            self._except(self._check_token())
            return None

        if not self._check_token() or self._read_token().kind != TokenKind.PARENTHESIS_OPEN:
            self._except(self._check_token())
            return None

        condition = self._parse_expression()

        if not self._check_token() or self._read_token().kind != TokenKind.PARENTHESIS_CLOSE:
            self._except(self._check_token())
            return None

        if not self._check_token() or self._read_token().kind != TokenKind.BRACE_OPEN:
            self._except(self._check_token())
            return None

        body_cmds = []
        while self._check_token() and self._check_token().kind != TokenKind.BRACE_CLOSE:
            cmd = self._parse_cmd()
            if cmd:
                body_cmds.append(cmd)
            else:
                if self._check_token():
                    self.advance()
                else:
                    break

        if not self._check_token() or self._read_token().kind != TokenKind.BRACE_CLOSE:
            self._except(self._check_token())
            return None

        body_block = BlockNode(body_cmds)
        return WhileNode(condition, body_block)

    # <atrib> ::= <var> '=' <exp> ';'
    def _parse_assignment(self):
        ident = self._read_token()
        if not ident or ident.kind != TokenKind.IDENTIFIER:
            self._except(ident)
            return None

        if not self._check_token() or self._read_token().kind != TokenKind.EQUALS:
            self._except(self._check_token())
            return None

        expr = self._parse_expression()

        if not self._check_token() or self._read_token().kind != TokenKind.SEMICOLON:
            self._except(self._check_token())
            return None

        return AssignmentNode(VariableNode(ident.lexeme), expr)

    # 'return' <exp> ';'
    def _parse_return(self):
        if not self._check_token() or self._read_token().kind != TokenKind.RETURN:
            self._except(self._check_token())
            return None

        expr = self._parse_expression()

        if not self._check_token() or self._read_token().kind != TokenKind.SEMICOLON:
            self._except(self._check_token())
            return None

        return ReturnNode(expr)

    # '{' <cmd>* '}'
    def _parse_block(self):
        if not self._check_token() or self._read_token().kind != TokenKind.BRACE_OPEN:
            self._except(self._check_token())
            return None

        stmts = []
        while self._check_token() and self._check_token().kind != TokenKind.BRACE_CLOSE:
            cmd = self._parse_cmd()
            if cmd:
                stmts.append(cmd)
            else:
                if self._check_token():
                    self.advance()
                else:
                    break

        if not self._check_token() or self._read_token().kind != TokenKind.BRACE_CLOSE:
            self._except(self._check_token())
            return None

        return BlockNode(stmts)

    # -- Declarations --
    # <decl> ::= <var> '=' <exp> ';'
    def _parse_declaration(self):
        # <decl> ::= <ident> '=' <exp> ';'
        ident_token = self._read_token()
        if ident_token.kind != TokenKind.IDENTIFIER:
            self._except(ident_token)
            return
        if self._read_token().kind != TokenKind.EQUALS:
            self._except(ident_token)
            return
        expr = self._parse_expression()
        if self._read_token().kind != TokenKind.SEMICOLON:
            self._except(ident_token)
            return
        return DeclarationNode(ident_token.lexeme, expr)

    # -- Expressions --
    # Entry point for all expressions
    def _parse_expression(self):
        # Inicia com o operador de menor precedência: ||
        return self._parse_or()

    # Precedência: || (menor)
    def _parse_or(self):
        node = self._parse_and() # Pega o operando do próximo nível (&&)
        while self._check_token() and self._check_token().kind == TokenKind.OR:
            op = self._read_token()
            right = self._parse_and() # O lado direito também é do próximo nível
            node = LogicalOrNode(node, op.lexeme, right)
        return node

    # Precedência: &&
    def _parse_and(self):
        node = self._parse_comparison() # Pega o operando do próximo nível (==, <, >)
        while self._check_token() and self._check_token().kind == TokenKind.AND:
            op = self._read_token()
            right = self._parse_comparison()
            node = LogicalAndNode(node, op.lexeme, right)
        return node

    # Precedência: ==, !=, <, <=, >, >=
    def _parse_comparison(self):
        node = self._parse_add_sub() # Pega o operando do próximo nível (+, -)
        comp_tokens = (
            TokenKind.EQUAL_EQUAL, TokenKind.NOT_EQUAL,
            TokenKind.LESS, TokenKind.LESS_EQUAL,
            TokenKind.GREATER, TokenKind.GREATER_EQUAL
        )
        while self._check_token() and self._check_token().kind in comp_tokens:
            op = self._read_token()
            right = self._parse_add_sub()
            node = ComparisonNode(node, op.lexeme, right)
        return node

    # Precedência: +, -
    def _parse_add_sub(self): 
        node = self._parse_mul_div() # Pega o operando do próximo nível (*, /)
        while self._check_token() and self._check_token().kind in (TokenKind.PLUS, TokenKind.MINUS):
            op = self._read_token()
            right = self._parse_mul_div()
            node = BinaryOperationNode(node, op.lexeme, right)
        return node

    # Precedência: *, /
    def _parse_mul_div(self):
        node = self._parse_unary() # Pega o operando do próximo nível (!)
        while self._check_token() and self._check_token().kind in (TokenKind.ASTERISK, TokenKind.SLASH):
            op = self._read_token()
            right = self._parse_unary()
            node = BinaryOperationNode(node, op.lexeme, right)
        return node
    
    # Precedência: ! (operador unário)
    def _parse_unary(self):
        token = self._check_token()
        if token and token.kind == TokenKind.NOT:
            op = self._read_token()
            operand = self._parse_unary() 
            return UnaryOperationNode(op.lexeme, operand)
        return self._parse_primary()

    def _parse_primary(self):
        # REMOVIDO: token = self._check_token()

        # Consome o próximo token e decide o que fazer com ele.
        token = self._read_token()

        if not token:
            self._except(None)
            return None

        # CASO 1: É um parêntese de abertura
        if token.kind == TokenKind.PARENTHESIS_OPEN:
            expr_node = self._parse_expression() # Recomeça a cadeia para a expressão interna
            
            # Verifica se o próximo token fecha o parêntese
            closing_token = self._read_token()
            if not closing_token or closing_token.kind != TokenKind.PARENTHESIS_CLOSE:
                self._except(closing_token) # Erro se não encontrar ')'
                return None
                
            return expr_node
        
        # CASO 2: É um número literal
        elif token.kind == TokenKind.LITERAL:
            return LiteralNode(token.lexeme)

        # CASO 3: É um identificador (variável ou chamada de função)
        elif token.kind == TokenKind.IDENTIFIER:
            # Verifica se o PRÓXIMO token é '(', indicando uma chamada de função
            if self._check_token() and self._check_token().kind == TokenKind.PARENTHESIS_OPEN:
                self._read_token()  # Consome '('
                
                args = []
                if self._check_token() and self._check_token().kind != TokenKind.PARENTHESIS_CLOSE:
                    # Loop para analisar múltiplos argumentos separados por vírgula
                    while True:
                        args.append(self._parse_expression())
                        if self._check_token() and self._check_token().kind == TokenKind.COMMA:
                            self._read_token() # Consome ',' e continua
                        else:
                            break # Sai do loop se não houver mais vírgulas
                
                # Verifica o ')' de fechamento da chamada de função
                if not self._check_token() or self._read_token().kind != TokenKind.PARENTHESIS_CLOSE:
                    self._except(self._check_token())
                    return None
                
                return FunCallNode(token.lexeme, args)
            else:
                # Se não for seguido por '(', é apenas uma variável
                return VariableNode(token.lexeme)
                
        # CASO 4: Token inesperado
        else:
            self._except(token)
            return None

    # -- Auxiliary methods --
    def _check_token(self) -> Token:
        if self.current_token_index < len(self.tokens):
            return self.tokens[self.current_token_index]
        return None

    def _read_token(self) -> Token:
        if self.current_token_index < len(self.tokens):
            token = self.tokens[self.current_token_index]
            self.advance()
            return token
        return None

    def advance(self):
        self.current_token_index += 1

    def _except(self, token: Token):
        if token is None:
            exception = SyntacticalException(
                "Token EOF não esperado.",
                line=-1,
                column=-1,
            )
        else:
            exception = SyntacticalException(
                f"Token '{getattr(token, 'lexeme', str(token))}' não esperado.",
                line=getattr(token, "line", -1),
                column=getattr(token, "column", -1),
            )
        self._exceptions.append(exception)
