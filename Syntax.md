# MyPi Language - Syntax Guide

This document provides a comprehensive reference for the syntax and semantics of the MyPi programming language.

---

## 1. Core Concepts

* **Case Sensitivity:** MyPi is case-sensitive (e.g., `myVar` is different from `myvar`).
* **Statements:** All executable lines of code are statements. Every statement **must** end with a semicolon (`;`).
* **Expressions:** Pieces of code that produce a value. Expressions can be part of statements (e.g., `print 1 + 2;`).
* **Code Blocks:** Groups of statements enclosed in curly braces (`{}`). Blocks define their own local scope.
* **Comments:** Single-line comments start with `//`. All text after `//` to the end of the line is ignored.

## 2. Data Types

### 2.1. Numbers
* **Syntax:** Integer literals (e.g., `10`, `42`, `-5`) or floating-point literals (e.g., `3.14`, `0.5`, `-2.0`, `10.0`).
* **Semantics:** Represents real numbers. Operations are standard arithmetic.

### 2.2. Booleans
* **Syntax:** `true`, `false`.
* **Semantics:** Represents truth values. Used in conditional expressions.

### 2.3. Strings (Text Values)
* **Syntax:** Sequences of characters enclosed in double quotes (`"`).
* **Escape Sequences:** Special character sequences within strings:
    * `\n`: Newline
    * `\t`: Tab
    * `\"`: Double quote
    * `\\`: Backslash
    * `\r`: Carriage return
    * `\0`: Null character (null byte)
* **Example:** `"Hello, World!\nTab here:\t"`

### 2.4. Lists
* **Syntax:** Ordered collections of values, enclosed in square brackets (`[]`). Elements are separated by commas (`,`).
* **Example:** `[]` (empty list), `[1, "two", true, nil, [nested_list]]`
* **Semantics:** Lists can contain elements of any MyPi data type.

### 2.5. Nil
* **Syntax:** `nil`.
* **Semantics:** Represents the absence of a value (similar to `null` in other languages). Uninitialized variables default to `nil`.

---

## 3. Variables

* **Declaration:** Use the `var` keyword followed by an identifier (variable name). An initial assignment using `=` is optional.
    ```mipi
    var my_variable;             // Declares my_variable, initialized to nil
    var counter = 0;             // Declares and initializes counter
    var message = "Hello";       // Declares and initializes message
    ```
* **Assignment:** An existing variable can be assigned a new value using the `=` operator.
    ```mipi
    counter = counter + 1;       // Re-assigns counter's value
    message = "New message";     // Re-assigns message
    ```
* **Identifiers:** Variable (and function) names must start with a letter (`a-z`, `A-Z`) or an underscore (`_`), followed by any combination of letters, digits (`0-9`), or underscores.
* **Scope:**
    * **Global:** Declared at the top level of the program. Accessible anywhere.
    * **Local:** Declared inside a code block (`{}`) or a function. Accessible only within that block/function and its nested blocks/functions.
    * **Shadowing:** If a local variable has the same name as an outer-scope variable, the local variable takes precedence within its scope. The outer variable's value remains unchanged.

---

## 4. Operators and Expressions

Operators follow standard precedence rules, from highest to lowest binding. Parentheses `()` can always be used to override precedence.

### 4.1. Operator Precedence (Highest to Lowest)

1.  **Grouping:** `( ... )`
2.  **List Literals:** `[ ... ]`
3.  **Indexing (Access):** `[index]` (e.g., `myList[0]`, `"string"[1]`)
4.  **Unary Operators:**
    * Unary Negation: `-` (e.g., `-5`, `-(x + y)`)
    * Logical NOT: `!` (e.g., `!true`, `!(x == y)`)
5.  **Multiplication/Division:** `*`, `/`
6.  **Addition/Subtraction/Concatenation:** `+`, `-`
7.  **Comparison Operators:** `>`, `>=`, `<`, `<=`
8.  **Equality Operators:** `==`, `!=`
9.  **Logical AND:** `and`
10. **Logical OR:** `or`
11. **Assignment:** `=`

### 4.2. Arithmetic Operations
* **Binary:** `number + number`, `number - number`, `number * number`, `number / number`.
* **Unary:** `-number`.
* **Example:** `5 + 3 * 2 - (10 / 2);`

### 4.3. Boolean & Comparison Operations
* **Comparison:** `number > number`, `number >= number`, `number < number`, `number <= number`. Result is a Boolean.
* **Logical NOT:** `!expression`. Converts `expression` to truthy/falsey and negates it.
* **Logical AND:** `expression1 and expression2`. Returns `expression1` if `expression1` is falsey, otherwise returns `expression2`. (Short-circuiting).
* **Logical OR:** `expression1 or expression2`. Returns `expression1` if `expression1` is truthy, otherwise returns `expression2`. (Short-circuiting).
* **Example:** `(a > b) and (c <= d);`, `!(true or false);`

### 4.4. Equality Operations
* **Strict Type Equality:** `expression1 == expression2`, `expression1 != expression2`.
    * Values are equal only if they have the **same type** and the **same value**.
    * `1 == "1"` evaluates to `false`.
    * `true == "true"` evaluates to `false`.
    * `nil == 0` evaluates to `false`.
* **Example:** `myVar == 10;`, `"hello" != "world";`

### 4.5. String Concatenation
* `string + string`: Concatenates two strings.
* `string + (number | boolean | list | nil)`: Converts the non-string operand to its string representation and then concatenates.
* **Example:** `"Age: " + 30;` (`"Age: 30"`), `"List: " + [1, 2];` (`"List: [1, 2]"`)

### 4.6. List Operations
* **List Concatenation:** `list + list`. Creates a new list by joining two lists.
    * **Example:** `[1, 2] + [3, 4];` (`[1, 2, 3, 4]`)
* **Indexing (Reading):** `list_expression[integer_index_expression]`. Returns the element at the specified index. Indices are 0-based.
    * **Example:** `my_list[0];`
* **Indexing (Assignment):** `list_expression[integer_index_expression] = value_expression;`. Modifies the element at the specified index in place.
    * **Example:** `my_list[1] = "updated";`

---

## 5. Control Flow

### 5.1. If-Then-Else Statements
* Executes a code block based on a condition.
* `condition` will be evaluated for its truthiness.
* The `else` branch is optional.
* Nested `if-then-else` statements create `else if` logic.
    ```mipi
    if (condition) {
        // Statements executed if condition is truthy
    } else { // Optional else block
        // Statements executed if condition is falsey
    }
    // Example of else if:
    if (x > 10) {
        print "Greater than 10";
    } else {
        if (x > 5) {
            print "Greater than 5 but not 10";
        } else {
            print "5 or less";
        }
    }
    ```

### 5.2. While Loops
* Repeatedly executes a code block as long as the `condition` remains truthy.
* The `condition` is evaluated before each iteration.
    ```mipi
    var counter = 0;
    while (counter < 5) {
        print "Counting: " + counter;
        counter = counter + 1;
    }
    ```

---

## 6. Functions

### 6.1. Function Declaration
* Defined using the `fun` keyword, followed by the function name, a parameter list in parentheses, and a code block (`{}`) for the function's body.
* Parameters are identifiers, separated by commas.
    ```mipi
    fun my_function(param1, param2) {
        // Function body statements
        print "Received: " + param1 + ", " + param2;
        var local_var = 10; // Local to this function
    }
    ```

### 6.2. Function Calling
* Invokes a declared function by its name, followed by arguments in parentheses.
* Arguments are expressions, separated by commas.
* Arguments are evaluated before the call and their values are passed to the function's parameters.
    ```mipi
    my_function("Argument 1", 20); // Calls the function
    ```
* Functions currently implicitly return `nil`.

---

## 7. Built-in Functions

MyPi provides several predefined functions:

* **`print expression;`**
    * Evaluates `expression` and displays its string representation to the console.
    * **Example:** `print "The answer is: " + (5 * 5);`
* **`input(prompt_string);`**
    * Prompts the user with `prompt_string` (optional).
    * Reads a line of text from the user's input and returns it as a string.
    * **Example:**
        ```mipi
        var user_name = input("Enter your name: ");
        print "Hello, " + user_name;
        ```
* **`list_append(list_obj, value);`**
    * Appends `value` to the end of `list_obj`. Modifies the list in place.
    * Returns `nil`.
    * **Example:** `var my_list = [1, 2]; list_append(my_list, 3); print my_list; // prints [1, 2, 3]`
* **`list_remove_at(list_obj, index);`**
    * Removes the element at `index` from `list_obj`. Modifies the list in place.
    * Returns `nil`.
    * **Example:** `var my_list = [1, 2, 3]; list_remove_at(my_list, 1); print my_list; // prints [1, 3]`
