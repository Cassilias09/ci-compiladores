from lexical_analysis.token.token_kind import TokenKind

single_char_tokens = {
    '(': TokenKind.PARENTHESIS_OPEN,
    ')': TokenKind.PARENTHESIS_CLOSE,
    '+': TokenKind.PLUS,
    '-': TokenKind.MINUS,
    '*': TokenKind.ASTERISK,
    '/': TokenKind.SLASH,
    '=': TokenKind.EQUALS,
    ';': TokenKind.SEMICOLON,
    '{': TokenKind.BRACE_OPEN,
    '}': TokenKind.BRACE_CLOSE,
    '>': TokenKind.GREATER,
    '<': TokenKind.LESS,
    '!': TokenKind.NOT
}

multi_char_tokens = {
    '==': TokenKind.EQUAL_EQUAL,
    '!=': TokenKind.NOT_EQUAL,
    '>=': TokenKind.GREATER_EQUAL,
    '<=': TokenKind.LESS_EQUAL,
    '&&': TokenKind.AND,
    '||': TokenKind.OR
}

keywords = {
    'if': TokenKind.IF,
    'else': TokenKind.ELSE,
    'while': TokenKind.WHILE,
    'return': TokenKind.RETURN
}

