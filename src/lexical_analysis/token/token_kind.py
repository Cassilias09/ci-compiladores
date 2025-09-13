import enum


class TokenKind(enum.Enum):

    PARENTHESIS_OPEN = 0
    PARENTHESIS_CLOSE = 1

    LITERAL = 2

    PLUS = 3
    MINUS = 4
    ASTERISK = 5
    SLASH = 6

    UNKNOWN = 7
    
    EQUALS = 8
    SEMICOLON = 9
    IDENTIFIER = 10