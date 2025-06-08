# Base class for all expressions
class Expr:
    pass

# Base class for all statements
class Stmt:
    pass

# Represents a binary expression (e.g., a + b, x == y)
class Binary(Expr):
    def __init__(self, left: Expr, operator, right: Expr):
        self.left = left
        self.operator = operator
        self.right = right

# Represents a unary expression (e.g., -a, !b)
class Unary(Expr):
    def __init__(self, operator, right: Expr):
        self.operator = operator
        self.right = right

# Represents a literal value (e.g., number, true, false, string)
class Literal(Expr):
    def __init__(self, value: object):
        self.value = value

# Represents a grouped expression (e.g., (a + b))
class Grouping(Expr):
    def __init__(self, expression: Expr):
        self.expression = expression

# Represents a variable reference (e.g., x)
class Variable(Expr):
    def __init__(self, name): # 'name' here will be a Token (IDENTIFIER)
        self.name = name

# Represents an assignment expression (e.g., x = 10 + y or myList[0] = 5)
class Assign(Expr):
    def __init__(self, target_expr: Expr, value: Expr): # target_expr can be Variable or Index
        self.target_expr = target_expr
        self.value = value

# Represents a variable declaration statement (e.g., var x; or var y = 5;)
class Var(Stmt):
    def __init__(self, name, initializer: Expr = None): # 'name' is a Token (IDENTIFIER)
        self.name = name
        self.initializer = initializer # Optional initial value

# Represents a print statement (e.g., print 1 + 2;)
class PrintStmt(Stmt):
    def __init__(self, expression: Expr):
        self.expression = expression

# Represents an expression treated as a statement (e.g., x = 5;)
class ExpressionStmt(Stmt):
    def __init__(self, expression: Expr):
        self.expression = expression

# Represents a block of statements enclosed in curly braces { ... }
class Block(Stmt):
    def __init__(self, statements: list[Stmt]):
        self.statements = statements

# Represents an if-then-else statement
class If(Stmt):
    def __init__(self, condition: Expr, then_branch: Stmt, else_branch: Stmt = None):
        self.condition = condition
        self.then_branch = then_branch
        self.else_branch = else_branch # Optional else branch

# Represents a while loop statement
class While(Stmt):
    def __init__(self, condition: Expr, body: Stmt):
        self.condition = condition
        self.body = body

# Represents the input() function call expression
class InputExpr(Expr):
    def __init__(self, prompt: Expr = None): # The prompt itself can be an expression (e.g., string literal), optional
        self.prompt = prompt

# New: Represents a list literal (e.g., [1, "two", true])
class ListLiteral(Expr):
    def __init__(self, elements: list[Expr]):
        self.elements = elements

# New: Represents an index access expression (e.g., myList[0])
class Index(Expr):
    def __init__(self, obj: Expr, index_expr: Expr): # obj is the list/string, index_expr is the index
        self.obj = obj
        self.index_expr = index_expr

# New: Represents a function declaration
class Function(Stmt):
    def __init__(self, name, params: list, body: Block): # name is Token, params are Tokens
        self.name = name
        self.params = params
        self.body = body

# New: Represents a function call expression
class Call(Expr):
    def __init__(self, callee: Expr, arguments: list[Expr]): # callee is the expression that produces the callable (e.g., Variable for function name)
        self.callee = callee
        self.arguments = arguments
