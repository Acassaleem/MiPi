from Token import Token, TokenType
from ast import (
    Binary, Unary, Literal, Grouping,
    Variable, Assign, Var, PrintStmt, ExpressionStmt,
    Block, If, While, InputExpr,
    ListLiteral, Index, Call, Function,
    Expr, Stmt
)


class Parser:
    def __init__(self, tokens: list[Token]):
        self.tokens = tokens
        self.current = 0

    def parse(self) -> list[Stmt]:
        statements = []
        while not self.is_at_end():
            try:
                statements.append(self.declaration())
            except RuntimeError as e:
                print(f"Parsing error: {e}")
                self.synchronize()
        return statements

    def declaration(self) -> Stmt:
        if self.match(TokenType.FUN):
            return self.fun_declaration()
        if self.match(TokenType.VAR):
            return self.var_declaration()

        return self.statement()

    def fun_declaration(self) -> Function:
        name = self.consume(TokenType.IDENTIFIER, "Expect function name.")
        self.consume(TokenType.LEFT_PAREN, "Expect '(' after function name.")

        params = []
        if not self.check(TokenType.RIGHT_PAREN):
            params.append(self.consume(TokenType.IDENTIFIER, "Expect parameter name."))
            while self.match(TokenType.COMMA):
                if len(params) >= 255:  # Arbitrary limit for parameters
                    self.error(self.peek(), "Cannot have more than 255 parameters.")
                params.append(self.consume(TokenType.IDENTIFIER, "Expect parameter name."))

        self.consume(TokenType.RIGHT_PAREN, "Expect ')' after parameters.")
        self.consume(TokenType.LEFT_BRACE, "Expect '{' before function body.")

        body = Block(self.block())
        return Function(name, params, body)

    def statement(self) -> Stmt:
        if self.match(TokenType.PRINT):
            return self.print_statement()
        if self.match(TokenType.IF):
            return self.if_statement()
        if self.match(TokenType.WHILE):
            return self.while_statement()
        if self.match(TokenType.LEFT_BRACE):  # For standalone blocks { ... }
            return Block(self.block())

        return self.expression_statement()

    def print_statement(self) -> PrintStmt:
        value = self.expression()
        self.consume(TokenType.SEMICOLON, "Expect ';' after value.")
        return PrintStmt(value)

    def var_declaration(self) -> Var:
        name = self.consume(TokenType.IDENTIFIER, "Expect variable name.")

        initializer = None
        if self.match(TokenType.EQUAL):
            initializer = self.expression()

        self.consume(TokenType.SEMICOLON, "Expect ';' after variable declaration.")
        return Var(name, initializer)

    def expression_statement(self) -> ExpressionStmt:
        expr = self.expression()
        self.consume(TokenType.SEMICOLON, "Expect ';' after expression.")
        return ExpressionStmt(expr)

    def block(self) -> list[Stmt]:
        statements = []
        while not self.check(TokenType.RIGHT_BRACE) and not self.is_at_end():
            statements.append(self.declaration())

        self.consume(TokenType.RIGHT_BRACE, "Expect '}' after block.")
        return statements

    def if_statement(self) -> If:
        self.consume(TokenType.LEFT_PAREN, "Expect '(' after 'if'.")
        condition = self.expression()
        self.consume(TokenType.RIGHT_PAREN, "Expect ')' after if condition.")

        then_branch = self.statement()

        else_branch = None
        if self.match(TokenType.ELSE):
            else_branch = self.statement()

        return If(condition, then_branch, else_branch)

    def while_statement(self) -> While:
        self.consume(TokenType.LEFT_PAREN, "Expect '(' after 'while'.")
        condition = self.expression()
        self.consume(TokenType.RIGHT_PAREN, "Expect ')' after while condition.")

        body = self.statement()

        return While(condition, body)

    def expression(self) -> Expr:
        return self.assignment()

    def assignment(self) -> Expr:
        expr = self.or_expr()

        if self.match(TokenType.EQUAL):
            equals_token = self.previous()
            value = self.assignment()

            if isinstance(expr, Variable):
                return Assign(expr, value)
            elif isinstance(expr, Index):
                return Assign(expr, value)

            raise self.error(equals_token, "Invalid assignment target.")

        return expr

    def or_expr(self) -> Expr:
        expr = self.and_expr()
        while self.match(TokenType.OR):
            operator = self.previous()
            right = self.and_expr()
            expr = Binary(expr, operator, right)
        return expr

    def and_expr(self) -> Expr:
        expr = self.equality()
        while self.match(TokenType.AND):
            operator = self.previous()
            right = self.equality()
            expr = Binary(expr, operator, right)
        return expr

    def equality(self) -> Expr:
        expr = self.comparison()
        while self.match(TokenType.BANG_EQUAL, TokenType.EQUAL_EQUAL):
            operator = self.previous()
            right = self.comparison()
            expr = Binary(expr, operator, right)
        return expr

    def comparison(self) -> Expr:
        expr = self.term()
        while self.match(TokenType.GREATER, TokenType.GREATER_EQUAL, TokenType.LESS, TokenType.LESS_EQUAL):
            operator = self.previous()
            right = self.term()
            expr = Binary(expr, operator, right)
        return expr

    def term(self) -> Expr:
        expr = self.factor()
        while self.match(TokenType.PLUS, TokenType.MINUS):
            operator = self.previous()
            right = self.factor()
            expr = Binary(expr, operator, right)
        return expr

    def factor(self) -> Expr:
        expr = self.unary()
        while self.match(TokenType.STAR, TokenType.SLASH):
            operator = self.previous()
            right = self.unary()
            expr = Binary(expr, operator, right)
        return expr

    def unary(self) -> Expr:
        if self.match(TokenType.BANG, TokenType.MINUS):
            operator = self.previous()
            right = self.unary()
            return Unary(operator, right)
        return self.call_expression()

    def call_expression(self) -> Expr:
        expr = self.primary()

        while True:
            if self.match(TokenType.LEFT_PAREN):
                expr = self.finish_call(expr)
            elif self.match(TokenType.LEFT_BRACKET):
                expr = self.finish_index(expr)
            else:
                break
        return expr

    def finish_call(self, callee: Expr) -> Expr:
        arguments = []
        if not self.check(TokenType.RIGHT_PAREN):
            arguments.append(self.expression())
            while self.match(TokenType.COMMA):
                arguments.append(self.expression())

        self.consume(TokenType.RIGHT_PAREN, "Expect ')' after arguments.")

        # Special handling for 'input' as a distinct AST node
        if isinstance(callee, Variable) and callee.name.type == TokenType.INPUT:
            if len(arguments) > 1:
                self.error(callee.name, "Built-in 'input' expects 0 or 1 argument.")
            return InputExpr(arguments[0] if arguments else None)

        # Handle built-in list functions like list_append and list_remove_at
        # These are identified as specific TokenTypes by Lexer and must be
        # correctly wrapped in a Call node that can be evaluated.
        elif isinstance(callee, Variable) and (
                callee.name.type == TokenType.LIST_APPEND or
                callee.name.type == TokenType.LIST_REMOVE_AT
        ):
            return Call(callee, arguments)  # Still a Call node, its callee is a Variable

        # For all other function calls (user-defined functions or unrecognized built-ins), use the general Call AST node
        return Call(callee, arguments)

    def finish_index(self, obj: Expr) -> Index:
        index_expr = self.expression()
        self.consume(TokenType.RIGHT_BRACKET, "Expect ']' after index.")
        return Index(obj, index_expr)

    def primary(self) -> Expr:
        if self.match(TokenType.FALSE):
            return Literal(False)
        if self.match(TokenType.TRUE):
            return Literal(True)
        if self.match(TokenType.NIL):
            return Literal(None)
        if self.match(TokenType.NUMBER):
            return Literal(self.previous().literal)
        if self.match(TokenType.STRING):
            return Literal(self.previous().literal)

        # Handle specific built-in keywords as primary elements
        if self.match(TokenType.INPUT):  # input is a special keyword
            # Parser expects `input` as a special keyword that leads to InputExpr,
            # so it needs to be handled here.
            self.consume(TokenType.LEFT_PAREN, "Expect '(' after 'input'.")
            prompt_expr = None
            if not self.check(TokenType.RIGHT_PAREN):
                prompt_expr = self.expression()
            self.consume(TokenType.RIGHT_PAREN, "Expect ')' after input prompt.")
            return InputExpr(prompt_expr)

        # Handle list_append and list_remove_at if they were tokenized as their specific types
        # This will create a Variable node that gets passed to call_expression and then finish_call
        if self.match(TokenType.LIST_APPEND):
            return Variable(self.previous())  # Treat built-in call name as a variable for now
        if self.match(TokenType.LIST_REMOVE_AT):
            return Variable(self.previous())  # Treat built-in call name as a variable for now

        if self.match(TokenType.IDENTIFIER):  # Any other identifier (regular variable name or user-defined func name)
            return Variable(self.previous())

        if self.match(TokenType.LEFT_PAREN):
            expr = self.expression()
            self.consume(TokenType.RIGHT_PAREN, "Expect ')' after expression.")
            return Grouping(expr)

        if self.match(TokenType.LEFT_BRACKET):
            elements = []
            if not self.check(TokenType.RIGHT_BRACKET):
                elements.append(self.expression())
                while self.match(TokenType.COMMA):
                    elements.append(self.expression())

            self.consume(TokenType.RIGHT_BRACKET, "Expect ']' after list literal.")
            return ListLiteral(elements)

        raise self.error(self.peek(), "Expect expression.")

    def match(self, *types: TokenType) -> bool:
        for type in types:
            if self.check(type):
                self.advance()
                return True
        return False

    def check(self, type: TokenType) -> bool:
        if self.is_at_end():
            return False
        return self.peek().type == type

    def advance(self) -> Token:
        if not self.is_at_end():
            self.current += 1
        return self.previous()

    def is_at_end(self) -> bool:
        return self.peek().type == TokenType.EOF

    def peek(self) -> Token:
        return self.tokens[self.current]

    def previous(self) -> Token:
        return self.tokens[self.current - 1]

    def consume(self, type: TokenType, message: str) -> Token:
        if self.check(type):
            return self.advance()
        raise self.error(self.peek(), message)

    def error(self, token: Token, message: str) -> RuntimeError:
        if token.type == TokenType.EOF:
            error_message = f"[line {token.line}] Error at end: {message}"
        else:
            error_message = f"[line {token.line}] Error at '{token.lexeme}': {message}"
        return RuntimeError(error_message)

    def synchronize(self):
        self.advance()
        while not self.is_at_end():
            if self.previous().type == TokenType.SEMICOLON:
                return
            if self.previous().type == TokenType.RIGHT_BRACE:
                return
            self.advance()

