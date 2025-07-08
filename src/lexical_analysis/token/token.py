from lexical_analysis.token.token_kind import TokenKind


class Token:
    def __init__(self, line: int, column: int, kind: TokenKind, lexeme: str):
        self.line: int = line
        self.column: int = column
        self.kind: TokenKind = kind
        self.lexeme: str = lexeme

    def __repr__(self):
        return f"<{self.line}:{self.column}, {self.kind.name}, '{self.lexeme}'>"
