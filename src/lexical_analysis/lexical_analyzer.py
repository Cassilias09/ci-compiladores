from exceptions.exception_list import ExceptionList
from exceptions.lexical_exception import LexicalException
from lexical_analysis.token.token import Token
from lexical_analysis.token.token_mapping import single_char_tokens
from lexical_analysis.token.token_kind import TokenKind


class LexicalAnalyzer:
    def __init__(self):
        self._buffer: str = ""
        self._line: int = 0
        self._column: int = -1
        self._tokens: list[Token] = []
        self._exceptions: list[Exception] = []

    def add_to_buffer(self, char: str):
        """Add a character to the buffer."""
        self._buffer += char
        self._column += 1

    def reset_buffer(self):
        """Reset the buffer."""
        self._buffer = ""

    def get_buffer(self) -> str:
        """Get the current buffer content."""
        return self._buffer

    def get_tokens(self) -> list[Token]:
        """Get the list of tokens."""
        return self._tokens

    def generate_token(self):
        """Generate a token from the current buffer."""
        lexeme = self.get_buffer()
        if lexeme == "":
            return

        if lexeme.isdigit():
            token = Token(
                line=self._line,
                column=self._column - len(lexeme) + 1,
                kind=TokenKind.LITERAL,
                lexeme=lexeme,
            )
        elif lexeme in single_char_tokens:
            token_kind = single_char_tokens[lexeme]
            token = Token(
                line=self._line, column=self._column, kind=token_kind, lexeme=lexeme
            )
        else:
            exception = LexicalException(
                f"Lexema '{lexeme}' não reconhecido.",
                line=self._line,
                column=self._column,
            )
            self._exceptions.append(exception)
            self.reset_buffer()
            return

        self.add_token(token)
        self.reset_buffer()

    def add_token(self, token: Token):
        """Add a token to the list of tokens."""
        self._tokens.append(token)

    def analyze(self, source_code: str):
        """Analyze the source code and generate tokens."""
        self.reset_buffer()
        for char in source_code:
            if char == "\n":
                self._line += 1
                self._column = 0
                continue

            if char.isspace():
                self._column += 1
                continue

            if char.isdigit():
                self.add_to_buffer(char)
                continue

            if self.get_buffer():
                self.generate_token()
            self.add_to_buffer(char)
            self.generate_token()
        self.generate_token()

        if len(self._exceptions) != 0:
            raise ExceptionList(process="Lexical Analysis", exceptions=self._exceptions)
        return self.get_tokens()
