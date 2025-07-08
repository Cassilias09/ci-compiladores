from lexical_analysis.token.token_kind import TokenKind

single_char_tokens = {
    '(': TokenKind.PARENTHESIS_OPEN,
    ')': TokenKind.PARENTHESIS_CLOSE,
    '+': TokenKind.PLUS,
    '-': TokenKind.MINUS,
    '*': TokenKind.ASTERISK,
    '/': TokenKind.SLASH,
}
