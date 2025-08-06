from lexical_analysis.token.token import Token
from lexical_analysis.token.token_kind import TokenKind
from syntatic_analysis.nodes.binary_operation_node import BinaryOperationNode
from syntatic_analysis.nodes.code_start_node import CodeStartNode
from syntatic_analysis.nodes.literal_node import LiteralNode
from exceptions.syntactical_exception import SyntacticalException
from exceptions.exception_list import ExceptionList

OPERAND_TOKENS = [TokenKind.ASTERISK, TokenKind.PLUS, TokenKind.MINUS, TokenKind.SLASH]


class SyntacticalAnalyzer:
    def __init__(self, tokens):
        self.tokens = tokens
        self.current_token_index = 0

        self.code_start: CodeStartNode = CodeStartNode()
        self._exceptions = []

    def parse(self) -> CodeStartNode:
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

    def advance(self):
        self.current_token_index += 1

    def _except(self, token: Token):
        exception = SyntacticalException(
            f"Token '{token.lexeme}' não esperado.",
            line=token.line,
            column=token.column,
        )
        self._exceptions.append(exception)
