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
    def _parse_expression(self):
        #return self._parse_exp_comp()
        return self._parse_exp_l_or()
    
    def _parse_exp_l_or(self):
    # <exp_l_or> ::= <exp_l_and> (’||’ <exp_l_and>)*
        node = self._parse_exp_l_and()
        while self._check_token() and self._check_token().kind == TokenKind.OR: 
            op = self._read_token()
            right = self._parse_exp_l_and()
            node = BinaryOperationNode(node, op.lexeme, right)
        return node

    def _parse_exp_l_and(self):
        # <exp_l_and> ::= <exp_comp> ('&&' <exp_comp>)*
        node = self._parse_exp_comp()
        while self._check_token() and self._check_token().kind == TokenKind.AND:
            op = self._read_token()
            right = self._parse_exp_comp()
            node = BinaryOperationNode(node, op.lexeme, right)
        return node

    # <exp> ::= <exp_a> (('<' | '>' | '==' | '!=' | '>=' | '<=') <exp_a>)*
    def _parse_exp_comp(self):
        node = self._parse_exp_a()
        comp_tokens = (
            TokenKind.LESS, 
            TokenKind.GREATER, 
            TokenKind.EQUAL_EQUAL,
            TokenKind.NOT_EQUAL, 
            TokenKind.GREATER_EQUAL, 
            TokenKind.LESS_EQUAL 
        )
        while self._check_token() and self._check_token().kind in comp_tokens:
            op = self._read_token()
            right = self._parse_exp_a()
            if right is None:
                print(f"DEBUG: Falha ao analisar o operando direito para {op.lexeme}. Próximo token: {self._check_token()}")
            node = ComparisonNode(node, op.lexeme, right)
        return node

    # <exp_a> ::= <exp_m> (('+' | '-') <exp_m>)*
    def _parse_exp_a(self): 
        node = self._parse_exp_m()
        while self._check_token() and self._check_token().kind in (TokenKind.PLUS, TokenKind.MINUS):
            op = self._read_token()
            right = self._parse_exp_m()
            node = BinaryOperationNode(node, op.lexeme, right)
        return node

    # <exp_m> ::= <prim> (('*' | '/') <prim>)*
    def _parse_exp_m(self):
        #node = self._parse_prim()
        node = self._parse_exp_u()
        while self._check_token() and self._check_token().kind in (TokenKind.ASTERISK, TokenKind.SLASH):
            op = self._read_token()
            #right = self._parse_prim()
            right = self._parse_exp_u()
            node = BinaryOperationNode(node, op.lexeme, right)
        return node
    
    # <exp_u> ::= '!' <exp_u> | <prim>
    def _parse_exp_u(self):
        token = self._check_token()
        if token and token.kind == TokenKind.NOT:
            op = self._read_token()
            operand = self._parse_exp_u() 
            return UnaryOperationNode(op.lexeme, operand)
        return self._parse_prim()

    # <prim> ::= <num> | <ident> | '(' <exp> ')' | <FunCall>
    def _parse_prim(self):
        token = self._read_token()
        if not token:
            self._except(token)
            return None

        if token.kind == TokenKind.LITERAL:
            return LiteralNode(token.lexeme)
        elif token.kind == TokenKind.IDENTIFIER:
            # Lookahead for function call
            if self._check_token() and self._check_token().kind == TokenKind.PARENTHESIS_OPEN:
                self._read_token()  # consume '('
                args = []
                if self._check_token() and self._check_token().kind != TokenKind.PARENTHESIS_CLOSE:
                    args.append(self._parse_expression())
                    while self._check_token() and self._check_token().kind == TokenKind.COMMA:
                        self._read_token()
                        args.append(self._parse_expression())
                if not self._check_token() or self._read_token().kind != TokenKind.PARENTHESIS_CLOSE:
                    self._except(self._check_token())
                    return None
                return FunCallNode(token.lexeme, args)
            else:
                return VariableNode(token.lexeme)
        elif token.kind == TokenKind.PARENTHESIS_OPEN:
            expr = self._parse_expression()
            if not self._check_token() or self._read_token().kind != TokenKind.PARENTHESIS_CLOSE:
                self._except(self._check_token())
                return None
            return expr
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
