NEW_LINE = "newline"
SPACE = "space"
LBRACKET = "lbracket"
RBRACKET = "rbracket"
STR = "str"
FIELD_STR = "fieldstr"
POINT = "point"
NUMBER = "number"
BOOL = "bool"
NULL = "null"
ASSIGN = "assign"
EOF = "EOF"

TOKEN_REGEXPS = {
    NEW_LINE: r"\n",
    SPACE: r"\s",
    ASSIGN: "\\=",
    POINT: "\\.",
    NULL: "\\{}",
    LBRACKET: "\\[",
    RBRACKET: "\\]",
    NUMBER: r'([0-9]*[.])?[0-9]+',
    BOOL: r'^(?:true|false)',
    STR: r'"[^"]*"',
    FIELD_STR: r'[A-Za-z0-9\_]*',
    EOF: "EOF"
}