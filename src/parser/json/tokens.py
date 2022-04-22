LBRACE = "lbrace"
RBRACE = "rbrace"
LBRACKET = "lbracket"
RBRACKET = "rbracket"
STR = "str"
NUMBER = "number"
BOOL = "bool"
COLON = "colon"
COMMA = "comma"
EOF = "EOF"
NULL = "null"

REGEX_TOKENS = {
    LBRACE: r"{",
    RBRACE: r"}",
    LBRACKET: "\\[",
    RBRACKET: "\\]",
    STR: r'"[^"]*"',
    NUMBER: r'([0-9]*[.])?[0-9]+',
    BOOL: r'^(?:true|false)',
    COLON: r":",
    COMMA: r",",
    EOF: "EOF",
    NULL: r"null"
}
