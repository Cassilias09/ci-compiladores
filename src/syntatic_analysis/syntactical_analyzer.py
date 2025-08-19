from lexical_analysis.token.token import Token
from lexical_analysis.token.token_kind import TokenKind
from syntatic_analysis.nodes.binary_operation_node import BinaryOperationNode
from syntatic_analysis.nodes.code_start_node import CodeStartNode
from syntatic_analysis.nodes.literal_node import LiteralNode
from exceptions.syntactical_exception import SyntacticalException
from exceptions.exception_list import ExceptionList


class SyntacticalAnalyzer:
    def __init__(self, tokens):
        self.tokens = tokens
        self.current_token_index = 0

        self.code_start: CodeStartNode = CodeStartNode()
        self._exceptions = []

    def parse(self) -> CodeStartNode:
        while self._check_token():
            try:
                self.code_start.add_child(self._parse_exp_a())
            except Exception as e:
                self._exceptions.append(e)
                self.advance()
        if len(self._exceptions) != 0:
            raise ExceptionList(
                process="Syntactical Analysis", exceptions=self._exceptions
            )
        return self.code_start

    def _parse_exp_a(self):
        left = self._parse_exp_m()
        while self._check_token() and self._check_token().kind in [TokenKind.PLUS, TokenKind.MINUS]:
            operator = self._read_token()
            right = self._parse_exp_m()
            left = BinaryOperationNode(left, operator.lexeme, right)
        return left

    def _parse_exp_m(self):
        left = self._parse_prim()
        while self._check_token() and self._check_token().kind in [TokenKind.ASTERISK, TokenKind.SLASH]:
            operator = self._read_token()
            right = self._parse_prim()
            left = BinaryOperationNode(left, operator.lexeme, right)
        return left

    def _parse_prim(self):
        token = self._read_token()
        if not token:
            self._except(token)
            return None

        if token.kind == TokenKind.PARENTHESIS_OPEN:
            exp = self._parse_exp_a()
            if not self._check_token() or self._check_token().kind != TokenKind.PARENTHESIS_CLOSE:
                self._except(self._check_token())
                return None
            self._read_token()  # Consume the closing parenthesis
            return exp

        elif token.kind == TokenKind.LITERAL:
            return LiteralNode(token.lexeme)

        else:
            self._except(token)
            return None

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
        exception = SyntacticalException(
            f"Token '{token.lexeme}' não esperado.",
            line=token.line,
            column=token.column,
        )
        self._exceptions.append(exception)
