class SemanticException(Exception):
    """Exception raised for errors in the semantic analysis of the input."""

    def __init__(self, message: str, line: int = -1, column: int = -1):
        """
        Initialize the SemanticException with a message, line number, and column number.

        :param message: Error message describing the issue.
        :param line: Line number where the error occurred (default: -1 if unknown).
        :param column: Column number where the error occurred (default: -1 if unknown).
        """
        if line >= 0 and column >= 0:
            super().__init__(
                f"Erro semântico na linha {line + 1}, coluna {column + 1}: {message}"
            )
        else:
            super().__init__(f"Erro semântico: {message}")

        self.line = line
        self.column = column
