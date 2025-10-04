from exceptions.exception_list import ExceptionList
from exceptions.lexical_exception import LexicalException
from lexical_analysis.token.token import Token
from lexical_analysis.token.token_mapping import single_char_tokens, multi_char_tokens, keywords
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

    def add_token(self, token: Token):
        """Add a token to the list of tokens."""
        self._tokens.append(token)

    def is_identifier_start(self, char: str) -> bool:
        return char.isalpha()

    def is_identifier_part(self, char: str) -> bool:
        return char.isalnum()

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
        elif self.is_identifier_start(lexeme[0]):
            if all(self.is_identifier_part(c) for c in lexeme):
                if lexeme in keywords:
                    token_kind = keywords[lexeme]
                    token = Token(
                        line=self._line,
                        column=self._column - len(lexeme) + 1,
                        kind=token_kind,
                        lexeme=lexeme,
                    )
                else:
                    token = Token(
                        line=self._line,
                        column=self._column - len(lexeme) + 1,
                        kind=TokenKind.IDENTIFIER,
                        lexeme=lexeme,
                    )
            else:
                exception = LexicalException(
                    f"Identificador inválido '{lexeme}'.",
                    line=self._line,
                    column=self._column,
                )
                self._exceptions.append(exception)
                self.reset_buffer()
                return
        elif lexeme in multi_char_tokens:
            token = Token(
                line=self._line,
                column=self._column - len(lexeme) + 1,
                kind=multi_char_tokens[lexeme],
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

    def analyze(self, source_code: str):
        """Analyze the source code and generate tokens."""
        self.reset_buffer()
        i = 0
        length = len(source_code)
        while i < length:
            char = source_code[i]
            if char == "\n":
                self._line += 1
                self._column = 0
                i += 1
                continue

            if char.isspace():
                self._column += 1
                i += 1
                continue

            if self.is_identifier_start(char):
                ident = char
                i += 1
                self._column += 1
                
                while i < length and self.is_identifier_part(source_code[i]):
                    ident += source_code[i]
                    i += 1
                    self._column += 1
                
                self._buffer = ident
                self.generate_token()
                continue

            if char.isdigit():
                num = char
                i += 1
                self._column += 1
                
                while i < length and source_code[i].isdigit():
                    num += source_code[i]
                    i += 1
                    self._column += 1
                
                if i < length and source_code[i].isalpha():
                    while i < length and (source_code[i].isalpha() or source_code[i].isdigit()):
                        num += source_code[i]
                        i += 1
                        self._column += 1
                    
                    self._buffer = num
                    exception = LexicalException(
                        f"Sequência inválida '{num}' (números não podem ser seguidos de letras).",
                        line=self._line,
                        column=self._column,
                    )
                    self._exceptions.append(exception)
                    self.reset_buffer()
                else:
                    self._buffer = num
                    self.generate_token()
                continue

            if char in single_char_tokens:
                if i + 1 < length and (char + source_code[i + 1]) in multi_char_tokens:
                    self._buffer = char + source_code[i + 1]
                    self.generate_token()
                    self._column += 2
                    i += 2
                    continue
                self._buffer = char
                self.generate_token()
                self._column += 1
                i += 1
                continue

            self._buffer = char
            exception = LexicalException(
                f"Caractere inválido '{char}'.",
                line=self._line,
                column=self._column,
            )
            self._exceptions.append(exception)
            self.reset_buffer()
            self._column += 1
            i += 1

        if len(self._exceptions) != 0:
            raise ExceptionList(process="Lexical Analysis", exceptions=self._exceptions)
        return self.get_tokens()
