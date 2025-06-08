from ast import (
    Binary, Unary, Literal, Grouping, Variable, Assign, Var, PrintStmt, ExpressionStmt,
    Block, If, While, InputExpr,
    ListLiteral, Index, Call, Function,
    Expr, Stmt
)
from Token import TokenType, Token


# Represents a runtime environment (scope) for variables.
# This allows for nested scopes.
class Environment:
    def __init__(self, enclosing=None):
        """
        Initializes a new environment.
        Args:
            enclosing (Environment, optional): The parent environment, for lexical scoping.
        """
        self.values = {}
        self.enclosing = enclosing  # Reference to the parent environment

    def define(self, name: str, value: object):
        """Declares a new variable in the current environment."""
        if name in self.values:
            raise RuntimeError(
                f"Variable '{name}' already defined in this scope.")  # Prevent re-definition in same scope
        self.values[name] = value

    def get(self, name_token: Token):
        """Retrieves a variable's value, searching in enclosing environments if not found locally."""
        if name_token.lexeme in self.values:
            return self.values.get(name_token.lexeme)

        if self.enclosing:  # If not found locally, check enclosing scope
            return self.enclosing.get(name_token)

        raise RuntimeError(f"Undefined variable '{name_token.lexeme}' on line {name_token.line}.")

    def assign(self, name_token: Token, value: object):
        """Assigns a value to an existing variable, searching in enclosing environments."""
        if name_token.lexeme in self.values:
            self.values[name_token.lexeme] = value
            return

        if self.enclosing:  # If not found locally, try to assign in enclosing scope
            self.enclosing.assign(name_token, value)
            return

        raise RuntimeError(f"Undefined variable '{name_token.lexeme}' on line {name_token.line}.")


# Represents a callable function in the MyPi language (user-defined or built-in).
class LoxCallable:
    def call(self, interpreter, arguments: list) -> object:
        raise NotImplementedError  # Abstract method

    def arity(self) -> int:
        raise NotImplementedError  # Number of arguments it expects


#  user-defined function.
class LoxFunction(LoxCallable):
    def __init__(self, declaration: Function, closure: Environment):
        self.declaration = declaration
        self.closure = closure  # The environment where the function was declared (for closures)

    def call(self, interpreter, arguments: list) -> object:
        # Create a new environment for the function call, linked to its declaration environment (closure)
        environment = Environment(self.closure)
        for i in range(len(self.declaration.params)):
            # Define parameters as local variables in the function's environment
            param_name = self.declaration.params[i].lexeme
            arg_value = arguments[i]
            environment.define(param_name, arg_value)

        # Execute the function body within the new environment
        # Use execute_block to handle environment switching correctly
        interpreter.execute_block(self.declaration.body.statements, environment)

        # Functions implicitly return nil for now (PLANNED: to add return keyword)
        return None

    def arity(self) -> int:
        return len(self.declaration.params)  # Number of parameters


# Built-in function for list element removal.
class BuiltInListRemoveAt(LoxCallable):
    def arity(self) -> int:
        return 2

    def call(self, interpreter, arguments: list) -> object:
        list_obj = arguments[0]
        index = arguments[1]

        if not isinstance(list_obj, list):
            raise RuntimeError("First argument to 'list_remove_at' must be a list.")
        if not isinstance(index, (int, float)) or not index.is_integer():
            raise RuntimeError("Second argument to 'list_remove_at' must be an integer index.")

        index = int(index)
        if not (0 <= index < len(list_obj)):
            raise RuntimeError(f"Index out of bounds: {index} for list of size {len(list_obj)}.")

        list_obj.pop(index)  # Modify list in place
        return None  # Return nil


# Built-in function for list append.
class BuiltInListAppend(LoxCallable):
    def arity(self) -> int:
        return 2

    def call(self, interpreter, arguments: list) -> object:
        list_obj = arguments[0]
        value = arguments[1]

        if not isinstance(list_obj, list):
            raise RuntimeError("First argument to 'list_append' must be a list.")

        list_obj.append(value)  # Modify list in place
        return None  # Return nil


class Interpreter:
    def __init__(self):
        # The top-most global environment.
        self.globals = Environment()
        # The current environment.
        self.environment = self.globals

        # Define built-in functions
        self.globals.define("list_remove_at", BuiltInListRemoveAt())
        self.globals.define("list_append", BuiltInListAppend())

    def interpret(self, statements: list[Stmt]):
        for statement in statements:
            try:
                self.execute(statement)
            except RuntimeError as e:
                print(f"Runtime error: {e}")
                # For basic error handling, we stop on the first runtime error.
                break

    def execute(self, stmt: Stmt):
        """Executes a statement."""
        if isinstance(stmt, ExpressionStmt):
            self.evaluate(stmt.expression)
        elif isinstance(stmt, PrintStmt):
            value = self.evaluate(stmt.expression)
            print(self.stringify(value))
        elif isinstance(stmt, Var):
            value = None
            if stmt.initializer:
                value = self.evaluate(stmt.initializer)
            self.environment.define(stmt.name.lexeme, value)  # Define in current environment

        # Execute a block
        elif isinstance(stmt, Block):
            # Pass the block's statements and create a new environment for it.
            self.execute_block(stmt.statements, Environment(self.environment))

        # Execute an if statement
        elif isinstance(stmt, If):
            # Evaluate condition and check its truthiness
            if self._is_truthy(self.evaluate(stmt.condition)):
                self.execute(stmt.then_branch)
            elif stmt.else_branch:  # Only execute else if it exists
                self.execute(stmt.else_branch)

        # Execute a while loop
        elif isinstance(stmt, While):
            # Loop while condition is true
            while self._is_truthy(self.evaluate(stmt.condition)):
                self.execute(stmt.body)

        # Execute a function declaration
        elif isinstance(stmt, Function):
            # Wrap the AST function declaration in a LoxFunction callable object
            # Pass the current environment as the function's closure
            function = LoxFunction(stmt, self.environment)
            self.environment.define(stmt.name.lexeme, function)  # Define the function in the current scope

    def execute_block(self, statements: list[Stmt], environment: Environment):
        """
        Executes a list of statements within a new, temporary environment (scope).
        This method is critical for managing lexical scope (e.g., for blocks or functions).
        """
        previous_environment = self.environment  # Save the current environment
        try:
            self.environment = environment  # Switch to the new environment for the block
            for statement in statements:
                self.execute(statement)
        finally:
            # Restore the previous environment when exiting the block,
            # regardless of whether an error occurred.
            self.environment = previous_environment

    def evaluate(self, expr: Expr) -> object:
        """Evaluates an expression."""
        if isinstance(expr, Binary):
            left = self.evaluate(expr.left)
            right = self.evaluate(expr.right)

            if expr.operator.type == TokenType.PLUS:
                # RELAXED RULE: If one operand is a string, convert the other to string.
                if isinstance(left, str) or isinstance(right, str):
                    return self.stringify(left) + self.stringify(right)
                # Handle number addition
                elif isinstance(left, (int, float)) and isinstance(right, (int, float)):
                    return left + right
                # Handle list concatenation
                elif isinstance(left, list) and isinstance(right, list):
                    return left + right  # Python list concatenation
                else:
                    # This fallback should ideally not be hit
                    # but kept for robustness if types are truly incompatible.
                    raise RuntimeError(
                        f"Operands of '+' must be two numbers, two strings or two lists on line {expr.operator.line}.")
            elif expr.operator.type == TokenType.MINUS:
                self._check_number_operands(expr.operator, left, right)
                return left - right
            elif expr.operator.type == TokenType.STAR:
                self._check_number_operands(expr.operator, left, right)
                return left * right
            elif expr.operator.type == TokenType.SLASH:
                self._check_number_operands(expr.operator, left, right)
                if right == 0:
                    raise RuntimeError(f"Division by zero on line {expr.operator.line}.")
                return left / right

            elif expr.operator.type == TokenType.GREATER:
                self._check_number_operands(expr.operator, left, right)
                return left > right
            elif expr.operator.type == TokenType.GREATER_EQUAL:
                self._check_number_operands(expr.operator, left, right)
                return left >= right
            elif expr.operator.type == TokenType.LESS:
                self._check_number_operands(expr.operator, left, right)
                return left < right
            elif expr.operator.type == TokenType.LESS_EQUAL:
                self._check_number_operands(expr.operator, left, right)
                return left <= right

            elif expr.operator.type == TokenType.BANG_EQUAL:
                return not self._is_equal(left, right)
            elif expr.operator.type == TokenType.EQUAL_EQUAL:
                return self._is_equal(left, right)

            elif expr.operator.type == TokenType.AND:
                # (relying on Python's short-circuiting truthiness)
                return left and right
            elif expr.operator.type == TokenType.OR:
                # (relying on Python's short-circuiting truthiness)
                return left if self._is_truthy(left) else right  # Correct OR operator logic (return operand)

        elif isinstance(expr, Unary):
            right = self.evaluate(expr.right)
            if expr.operator.type == TokenType.MINUS:
                self._check_number_operand(expr.operator, right)
                return -right
            elif expr.operator.type == TokenType.BANG:
                # (negates based on truthiness of any type)
                return not self._is_truthy(right)

        elif isinstance(expr, Literal):
            return expr.value

        elif isinstance(expr, Grouping):
            return self.evaluate(expr.expression)

        elif isinstance(expr, Variable):
            return self.environment.get(expr.name)  # Get from current environment

        elif isinstance(expr, Assign):
            # Assignment now handles Variable or Index targets
            # Evaluate the right-hand side value
            value = self.evaluate(expr.value)

            # If the target is a Variable, simply assign to the environment
            if isinstance(expr.target_expr, Variable):
                self.environment.assign(expr.target_expr.name, value)
            # If the target is an Index (e.g., myList[0] = value)
            elif isinstance(expr.target_expr, Index):
                list_obj = self.evaluate(expr.target_expr.obj)
                index_val = self.evaluate(expr.target_expr.index_expr)

                if not isinstance(list_obj, list):
                    raise RuntimeError(
                        f"Cannot assign to non-list type via index on line {expr.target_expr.obj.name.line if hasattr(expr.target_expr.obj, 'name') else expr.target_expr.obj.line if hasattr(expr.target_expr.obj, 'line') else '?'}.")
                if not isinstance(index_val, (int, float)) or not index_val.is_integer():
                    raise RuntimeError(
                        f"List index must be an integer on line {expr.target_expr.index_expr.line if hasattr(expr.target_expr.index_expr, 'line') else '?'}.")

                index_val = int(index_val)  # Convert to int

                if not (0 <= index_val < len(list_obj)):
                    raise RuntimeError(
                        f"List index out of bounds: {index_val} on line {expr.target_expr.index_expr.line if hasattr(expr.target_expr.index_expr, 'line') else '?'}.")

                list_obj[index_val] = value  # Perform in-place assignment
            else:  # This 'else' belongs to the Assignment target type check
                raise RuntimeError(
                    f"Invalid assignment target on line {expr.target_expr.line if hasattr(expr.target_expr, 'line') else '?'}.")

            return value  # Assignment expressions typically return the assigned value

        elif isinstance(expr, InputExpr):
            prompt_str = ""
            if expr.prompt:
                evaluated_prompt = self.evaluate(expr.prompt)
                if not isinstance(evaluated_prompt, str):
                    raise RuntimeError(
                        f"Input prompt must be a string on line {expr.prompt.line if hasattr(expr.prompt, 'line') else '?'}.")
                prompt_str = evaluated_prompt
            return input(prompt_str)

        elif isinstance(expr, ListLiteral):
            elements = [self.evaluate(el) for el in expr.elements]
            return elements  # Python list used for MyPi list

        elif isinstance(expr, Index):
            obj = self.evaluate(expr.obj)
            index_val = self.evaluate(expr.index_expr)

            if not isinstance(obj, (list, str)):  # Allow indexing on lists and strings
                raise RuntimeError(
                    f"Only lists and strings can be indexed on line {expr.obj.name.line if hasattr(expr.obj, 'name') else expr.obj.line if hasattr(expr.obj, 'line') else '?'}.")
            if not isinstance(index_val, (int, float)) or not index_val.is_integer():
                raise RuntimeError(
                    f"Index must be an integer on line {expr.index_expr.line if hasattr(expr.index_expr, 'line') else '?'}.")

            index_val = int(index_val)  # Convert float index to int

            if not (0 <= index_val < len(obj)):
                raise RuntimeError(
                    f"Index out of bounds: {index_val} on line {expr.index_expr.line if hasattr(expr.index_expr, 'line') else '?'}.")

            return obj[index_val]

        elif isinstance(expr, Call):
            callee = self.evaluate(expr.callee)  # Evaluate the expression that produces the callable object

            arguments = [self.evaluate(arg) for arg in expr.arguments]  # Evaluate all arguments

            if not isinstance(callee, LoxCallable):
                raise RuntimeError(
                    f"Not a callable type on line {expr.callee.name.line if hasattr(expr.callee, 'name') else expr.callee.line if hasattr(expr.callee, 'line') else '?'}.")

            # Check arity (number of arguments)
            if len(arguments) != callee.arity():
                raise RuntimeError(
                    f"Expected {callee.arity()} arguments but got {len(arguments)} on line {expr.callee.name.line if hasattr(expr.callee, 'name') else expr.callee.line if hasattr(expr.callee, 'line') else '?'}.")

            return callee.call(self, arguments)  # Execute the callable

        else:
            raise RuntimeError(f"Unknown expression type: {type(expr).__name__}")

    def _is_truthy(self, obj: object) -> bool:
        """Determines the 'truthiness' of a value for if/while conditions."""
        if obj is None: return False
        if isinstance(obj, bool): return obj
        if isinstance(obj, (int, float)): return obj != 0
        if isinstance(obj, str): return len(obj) > 0
        if isinstance(obj, list): return len(obj) > 0
        return False

    def stringify(self, value: object) -> str:
        """Converts a Python value to its string representation for printing."""
        if value is None: return "nil"
        if isinstance(value, bool): return str(value).lower()
        if isinstance(value, float):
            if value.is_integer():
                return str(int(value))
            return str(value)
        if isinstance(value, str):
            return value
        if isinstance(value, list):
            elements_str = [self.stringify(elem) for elem in value]
            return "[" + ", ".join(elements_str) + "]"
        if isinstance(value, LoxCallable):
            return str(value)
        return str(value)

    def _is_equal(self, a: object, b: object) -> bool:
        """Strict equality check."""
        if type(a) != type(b):
            return False
        if a is None and b is None: return True
        if a is None: return False
        return a == b

    def _check_number_operand(self, operator, operand: object):
        if isinstance(operand, (int, float)):
            return
        raise RuntimeError(f"Operand of '{operator.lexeme}' must be a number on line {operator.line}.")

    def _check_number_operands(self, operator, left: object, right: object):
        if isinstance(left, (int, float)) and isinstance(right, (int, float)):
            return
        raise RuntimeError(f"Operands of '{operator.lexeme}' must be numbers on line {operator.line}.")

    def _check_boolean_operand(self, operator, operand: object):
        if isinstance(operand, bool):
            return
        raise RuntimeError(f"Operand of '{operator.lexeme}' must be a boolean on line {operator.line}.")

    def _check_boolean_operands(self, operator, left: object, right: object):
        if isinstance(left, bool) and isinstance(right, bool):
            return
        raise RuntimeError(f"Operands of '{operator.lexeme}' must be booleans on line {operator.line}.")
