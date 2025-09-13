from lexical_analysis.token.token import Token
from lexical_analysis.token.token_kind import TokenKind
from syntatic_analysis.nodes.binary_operation_node import BinaryOperationNode
from syntatic_analysis.nodes.code_start_node import CodeStartNode
from syntatic_analysis.nodes.declaration_node import DeclarationNode
from syntatic_analysis.nodes.literal_node import LiteralNode
from syntatic_analysis.nodes.program_node import ProgramNode
from syntatic_analysis.nodes.variable_node import VariableNode
from exceptions.syntactical_exception import SyntacticalException
from exceptions.exception_list import ExceptionList

OPERAND_TOKENS = [TokenKind.ASTERISK, TokenKind.PLUS, TokenKind.MINUS, TokenKind.SLASH]


class SyntacticalAnalyzer:
    def __init__(self, tokens):
        self.tokens = tokens
        self.current_token_index = 0

        self.code_start: CodeStartNode = CodeStartNode()
        self._exceptions = []

    def parse(self):
        # <programa> ::= <decl>* <result>
        if self._check_token() and (
            self._check_token().kind == TokenKind.IDENTIFIER
            or self._check_token().kind == TokenKind.EQUALS
        ):
            declarations = []
            while self._check_token() and self._check_token().kind == TokenKind.IDENTIFIER:
                declarations.append(self._parse_declaration())
            if self._check_token() and self._check_token().kind == TokenKind.EQUALS:
                result_expression = self._parse_result()
                if len(self._exceptions) != 0:
                    raise ExceptionList(process="Syntactical Analysis", exceptions=self._exceptions)
                self.code_start._variables = [decl.name for decl in declarations]
                self.code_start.add_child(ProgramNode(declarations, result_expression))
                return self.code_start

        # Expressão sem declarações (EC2)
        while self._check_token():
            self.code_start.add_child(self._parse_line())
        if len(self._exceptions) != 0:
            raise ExceptionList(
                process="Syntactical Analysis", exceptions=self._exceptions
            )
        return self.code_start

    def _parse_line(self):
        while True:
            token = self._read_token()
            if not token:
                break

            if token.kind == TokenKind.PARENTHESIS_OPEN:
                if self._check_token() is None:
                    self._except(token)
                    return

                if self._check_token().kind in OPERAND_TOKENS:
                    self._except(token)
                    return

                left_node = self._parse_line()
                if left_node is None:
                    self._except(token)
                    return

                operator = self._read_token()
                if operator is None:
                    self._except(token)
                    return

                if operator.kind not in OPERAND_TOKENS:
                    self._except(token)
                    return

                right_node = self._parse_line()
                if right_node is None:
                    self._except(token)
                    return

                operation_node = BinaryOperationNode(
                    left=left_node,
                    operator=operator.lexeme,
                    right=right_node,
                )

                # Lê o fim da expressão
                if self._read_token().kind != TokenKind.PARENTHESIS_CLOSE:
                    self._except(token)
                    return
                return operation_node

            if token.kind == TokenKind.LITERAL:
                return LiteralNode(value=token.lexeme)

            self._except(token)

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

    def _parse_result(self):
        # <result> ::= '=' <exp>
        eq_token = self._read_token()
        if eq_token.kind != TokenKind.EQUALS:
            self._except(eq_token)
            return
        return self._parse_expression()

    def _parse_expression(self):
        # <exp> ::= <exp_m> ((’+’ | ’-’) <exp_m>)*
        node = self._parse_exp_m()
        while self._check_token() and self._check_token().kind in (TokenKind.PLUS, TokenKind.MINUS):
            op = self._read_token()
            right = self._parse_exp_m()
            node = BinaryOperationNode(left=node, operator=op.lexeme, right=right)
        return node

    def _parse_exp_m(self):
        # <exp_m> ::= <prim> ((’*’ | ’/’) <prim>)*
        node = self._parse_prim()
        while self._check_token() and self._check_token().kind in (TokenKind.ASTERISK, TokenKind.SLASH):
            op = self._read_token()
            right = self._parse_prim()
            node = BinaryOperationNode(left=node, operator=op.lexeme, right=right)
        return node

    def _parse_prim(self):
        # <prim> ::= <num> | <ident> | ’(’ <exp> ’)’
        token = self._read_token()
        if token.kind == TokenKind.LITERAL:
            return LiteralNode(token.lexeme)
        elif token.kind == TokenKind.IDENTIFIER:
            return VariableNode(token.lexeme)
        elif token.kind == TokenKind.PARENTHESIS_OPEN:
            expr = self._parse_expression()
            if self._read_token().kind != TokenKind.PARENTHESIS_CLOSE:
                self._except(token)
            return expr
        else:
            self._except(token)

    def advance(self):
        self.current_token_index += 1

    def _except(self, token: Token):
        exception = SyntacticalException(
            f"Token '{token.lexeme}' não esperado.",
            line=token.line,
            column=token.column,
        )
        self._exceptions.append(exception)
