from typing import List
from lexical_analysis.token.token import Token
from lexical_analysis.token.token_kind import TokenKind
from syntatic_analysis.nodes import BaseNode
from syntatic_analysis.nodes.binary_operation_node import BinaryOperationNode
from syntatic_analysis.nodes.literal_node import LiteralNode
from exceptions.syntactical_exception import SyntacticalException


class SyntacticalAnalyzer:
    def __init__(self, tokens):
        self.tokens = tokens
        self.current_token_index = 0

        self.syntactic_tree_nodes = []

    def parse(self) -> List[BaseNode]:
        while self._check_token():
            self.syntactic_tree_nodes.append(self._parse_line())
        return self.syntactic_tree_nodes

    def _parse_line(self):
        while True:
            token = self._read_token()
            if not token:
                break

            if token.kind == TokenKind.PARENTHESIS_OPEN:
                operation_node = BinaryOperationNode(
                    left=self._parse_line(),
                    operator=self._read_token().lexeme,
                    right=self._parse_line(),
                )
                self._read_token()  # Lê o PARENTHESIS_CLOSE
                return operation_node

            if token.kind == TokenKind.LITERAL:
                return LiteralNode(value=token.lexeme)

            raise SyntacticalException(
                f"Token '{token.lexeme}' não reconhecido.",
                line=token.line,
                column=token.column,
            )

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
