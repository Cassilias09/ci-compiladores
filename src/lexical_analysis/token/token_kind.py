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

    IF = 11
    ELSE = 12

    WHILE = 13

    RETURN = 14

    BRACE_OPEN = 15
    BRACE_CLOSE = 16

    GREATER = 17
    LESS = 18
    EQUAL_EQUAL = 19
    NOT_EQUAL = 20
    GREATER_EQUAL = 21
    LESS_EQUAL = 22

    FUN = 23
    VAR = 24
    MAIN = 25
    COMMA = 26

    AND = 27
    OR = 28
    NOT = 29
