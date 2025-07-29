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
                    exception = SyntacticalException(
                        f"Token '{token.lexeme}' não esperado.",
                        line=token.line,
                        column=token.column,
                    )
                    self._exceptions.append(exception)
                    return

                if self._check_token().kind in OPERAND_TOKENS:
                    exception = SyntacticalException(
                        f"Token '{token.lexeme}' não esperado.",
                        line=token.line,
                        column=token.column,
                    )
                    self._exceptions.append(exception)
                    return

                operation_node = BinaryOperationNode(
                    left=self._parse_line(),
                    operator=self._read_token().lexeme,
                    right=self._parse_line(),
                )

                # Lê o fim da expressão
                if self._read_token().kind != TokenKind.PARENTHESIS_CLOSE:
                    exception = SyntacticalException(
                        f"Token '{token.lexeme}' não esperado.",
                        line=token.line,
                        column=token.column,
                    )
                    self._exceptions.append(exception)
                    return
                return operation_node

            if token.kind == TokenKind.LITERAL:
                return LiteralNode(value=token.lexeme)

            exception = SyntacticalException(
                f"Token '{token.lexeme}' não reconhecido.",
                line=token.line,
                column=token.column,
            )
            self._exceptions.append(exception)

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
