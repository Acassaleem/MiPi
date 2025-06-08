from enum import Enum


class TokenType(Enum):
    # Single-character tokens
    LEFT_PAREN = '('
    RIGHT_PAREN = ')'
    LEFT_BRACE = '{'
    RIGHT_BRACE = '}'
    LEFT_BRACKET = '['
    RIGHT_BRACKET = ']'
    COMMA = ','
    MINUS = '-'
    PLUS = '+'
    SLASH = '/'
    STAR = '*'
    SEMICOLON = ';'

    # One or two character tokens
    BANG = '!'
    BANG_EQUAL = '!='
    EQUAL = '='
    EQUAL_EQUAL = '=='
    GREATER = '>'
    GREATER_EQUAL = '>='
    LESS = '<'
    LESS_EQUAL = '<='

    # Literals
    NUMBER = 'NUMBER'
    STRING = 'STRING'

    # Boolean Literals
    TRUE = 'true'
    FALSE = 'false'
    NIL = 'nil'

    # Keywords
    AND = 'and'
    OR = 'or'
    IDENTIFIER = 'IDENTIFIER'
    VAR = 'var'
    PRINT = 'print'
    IF = 'if'
    ELSE = 'else'
    WHILE = 'while'
    FUN = 'fun'
    INPUT = 'input'

    # Built-in functions that are part of the language keywords for special handling
    LIST_REMOVE_AT = 'list_remove_at'
    LIST_APPEND = 'list_append'

    EOF = 'EOF'


class Token:
    def __init__(self, type: TokenType, lexeme: str, literal: object, line: int):
        self.type = type
        self.lexeme = lexeme
        self.literal = literal
        self.line = line

    def __repr__(self):
        return f"Token(type={self.type.name}, lexeme='{self.lexeme}', literal={self.literal}, line={self.line})"

    def __str__(self):
        return f"{self.type.name} {self.lexeme} {self.literal}"

