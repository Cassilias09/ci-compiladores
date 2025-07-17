class LexicalException(Exception):
    """Exception raised for errors in the lexical analysis of the input."""

    def __init__(self, message: str, line: int, column: int):
        """
        Initialize the LexicalException with a message, line number, and column number.

        :param message: Error message describing the issue.
        :param line: Line number where the error occurred.
        :param column: Column number where the error occurred.
        """
        super().__init__(
            f"Erro léxico na linha {line + 1}, coluna {column + 1}: {message}"
        )
        self.line = line
        self.column = column
