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
    ',': TokenKind.COMMA
}

multi_char_tokens = {
    '==': TokenKind.EQUAL_EQUAL
}

keywords = {
    'if': TokenKind.IF,
    'else': TokenKind.ELSE,
    'while': TokenKind.WHILE,
    'return': TokenKind.RETURN,
    'fun': TokenKind.FUN,
    'var': TokenKind.VAR,
    'main': TokenKind.MAIN
}

