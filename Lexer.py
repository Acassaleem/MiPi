from Token import Token, TokenType


class Lexer:
    def __init__(self, source: str):
        self.source = source
        self.tokens = []
        self.start = 0
        self.current = 0
        self.line = 1

        self.keywords = {
            "and": TokenType.AND,
            "false": TokenType.FALSE,
            "or": TokenType.OR,
            "true": TokenType.TRUE,
            "nil": TokenType.NIL,
            "var": TokenType.VAR,
            "print": TokenType.PRINT,
            "if": TokenType.IF,
            "else": TokenType.ELSE,
            "while": TokenType.WHILE,
            "fun": TokenType.FUN,
            "input": TokenType.INPUT, # Keep input as a keyword, as it's a special AST node
            # REMOVED: list_remove_at and list_append from keywords.
            # Handled within the identifier() method's specific checks.
        }

    def scan_tokens(self) -> list[Token]:
        while not self.is_at_end():
            self.start = self.current
            self.scan_token()

        self.tokens.append(Token(TokenType.EOF, "", None, self.line))
        return self.tokens

    def scan_token(self):
        c = self.advance()
        if c == '(':
            self.add_token(TokenType.LEFT_PAREN)
        elif c == ')':
            self.add_token(TokenType.RIGHT_PAREN)
        elif c == '{':
            self.add_token(TokenType.LEFT_BRACE)
        elif c == '}':
            self.add_token(TokenType.RIGHT_BRACE)
        elif c == '[':
            self.add_token(TokenType.LEFT_BRACKET)
        elif c == ']':
            self.add_token(TokenType.RIGHT_BRACKET)
        elif c == ',':
            self.add_token(TokenType.COMMA)
        elif c == '-':
            self.add_token(TokenType.MINUS)
        elif c == '+':
            self.add_token(TokenType.PLUS)
        elif c == '*':
            self.add_token(TokenType.STAR)
        elif c == ';':
            self.add_token(TokenType.SEMICOLON)
        elif c == '!':
            self.add_token(TokenType.BANG_EQUAL if self.match_char('=') else TokenType.BANG)
        elif c == '=':
            self.add_token(TokenType.EQUAL_EQUAL if self.match_char('=') else TokenType.EQUAL)
        elif c == '<':
            self.add_token(TokenType.LESS_EQUAL if self.match_char('=') else TokenType.LESS)
        elif c == '>':
            self.add_token(TokenType.GREATER_EQUAL if self.match_char('=') else TokenType.GREATER)
        elif c == '"':
            self.string()
        elif c == '/':
            if self.match_char('/'):
                while self.peek() != '\n' and not self.is_at_end():
                    self.advance()
            else:
                self.add_token(TokenType.SLASH)
        elif c.isspace():
            if c == '\n':
                self.line += 1
            pass
        elif c.isdigit():
            self.number()
        elif c.isalpha() or c == '_':
            self.identifier()
        else:
            raise RuntimeError(f"Unexpected character '{c}' on line {self.line}")

    def string(self):
        while self.peek() != '"' and not self.is_at_end():
            if self.peek() == '\n':
                self.line += 1
            if self.peek() == '\\':
                self.advance()
                escape_char = self.advance()
                if escape_char not in ['n', 't', '"', '\\', 'r', '0']:
                    raise RuntimeError(f"Invalid escape sequence '\\{escape_char}' in string on line {self.line}.")
            else:
                self.advance()

        if self.is_at_end():
            raise RuntimeError(f"Unterminated string on line {self.line}.")

        self.advance()

        value_raw = self.source[self.start + 1: self.current - 1]

        value_processed = ""
        i = 0
        while i < len(value_raw):
            if value_raw[i] == '\\':
                i += 1
                if i < len(value_raw):
                    escape_char = value_raw[i]
                    if escape_char == 'n':
                        value_processed += '\n'
                    elif escape_char == 't':
                        value_processed += '\t'
                    elif escape_char == '"':
                        value_processed += '\"'
                    elif escape_char == '\\':
                        value_processed += '\\'
                    elif escape_char == 'r':
                        value_processed += '\r'
                    elif escape_char == '0':
                        value_processed += '\x00'
                    else:
                        raise RuntimeError(f"Invalid escape sequence '\\{escape_char}' in string on line {self.line}.")
                else:
                    raise RuntimeError(f"Incomplete escape sequence in string on line {self.line}.")
            else:
                value_processed += value_raw[i]
            i += 1

        self.add_token(TokenType.STRING, value_processed)

    def number(self):
        while self.peek().isdigit():
            self.advance()

        if self.peek() == '.' and self.peek_next().isdigit():
            self.advance()
            while self.peek().isdigit():
                self.advance()

        value = float(self.source[self.start:self.current])
        self.add_token(TokenType.NUMBER, value)

    def identifier(self):
        while self.peek().isalnum() or self.peek() == '_':
            self.advance()

        text = self.source[self.start:self.current]
        type = self.keywords.get(text)
        if type is None:
            if text == "list_remove_at":
                type = TokenType.LIST_REMOVE_AT
            elif text == "list_append":
                type = TokenType.LIST_APPEND
            else:
                type = TokenType.IDENTIFIER

        self.add_token(type)

    def match_char(self, expected: str) -> bool:
        if self.is_at_end() or self.source[self.current] != expected:
            return False
        self.current += 1
        return True

    def is_at_end(self) -> bool:
        return self.current >= len(self.source)

    def advance(self) -> str:
        char = self.source[self.current]
        self.current += 1
        return char

    def peek(self) -> str:
        if self.is_at_end():
            return '\0'
        return self.source[self.current]

    def peek_next(self) -> str:
        if self.current + 1 >= len(self.source):
            return '\0'
        return self.source[self.current + 1]

    def add_token(self, type: TokenType, literal: object = None):
        lexeme = self.source[self.start:self.current]
        self.tokens.append(Token(type, lexeme, literal, self.line))

