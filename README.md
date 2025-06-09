# MiPi

## Overview

MyPi is a dynamically-typed, imperative programming language, implemented as a tree-walking interpreter in Python. It's designed for simplicity and clarity, allowing users to write and execute basic programs involving arithmetic, boolean logic, strings, lists, variables, control flow, and functions.

## Features:
## Core Language Features (Stages 1-5 Complete):

### Stage 1. Numbers:
* Support for integers and floating-point values.
* Binary arithmetic: addition (`+`), subtraction (`-`), multiplication (`*`), division (`/`).
* Unary negation (`-`).
* Parentheses for grouping expressions.

### Stage 2. Booleans:
* `true` and `false` literals.
* Binary comparison: greater than (`>`), greater than or equal to (`>=`), less than (`<`), less than or equal to (`<=`) for numbers.
* Binary equality (`==`) and inequality (`!=`) for numbers, booleans, strings, and lists (strict type equality).
* Logical operators: `AND` (`and`), `OR` (`or`), `NOT` (`!`).
* Truthiness: `nil`, `false`, `0`, `0.0`, empty string (`""`), and empty list (`[]`) are considered falsey; all other values are truthy.

### Stage 3. Strings (Text Values):
* String literals enclosed in double quotes (`""`).
* Binary concatenation (`+`) for strings (automatic conversion of numbers, booleans, lists, nil to string if concatenated with a string).
* String equality (`==`) and inequality (`!=`).
* Escape sequences: `\n`, `\t`, `\"`, `\\`, `\r`, `\0`.
* String indexing (read-only random access) like `"abc"[0]`.

### Stage 4. Global Data (Variables):
* Variable declaration (`var` keyword).
* Variable assignment (`=`).
* Persistence of variable values across the program's execution.
* All operations from Stages 1-3 compose with global variables.
* Efficient variable lookup (average O(1) time complexity using hash maps).

### Stage 5. Control Flow:
* If-then statements.
* If-then-else statements.
* Nested if-then-else statements.
* While loops.
* Nested while loops.
* Code blocks (`{}`) for grouping statements and defining scope.

###User Input:
* `input(prompt_string)` built-in function to read user input.

---

## Additional Features (Stage 6 Complete):

### List Data Structure:
* List literals (`[]`).
* Random access by index (`myList[index]`) for both reading and assignment.
* List concatenation (`list1 + list2`).
* `list_append(list_obj, value)` built-in function for back-insertion.
* `list_remove_at(list_obj, index)` built-in function for random removal.

### Function-Based Code Reusability:
* Function declaration (`fun name(params) { body }`).
* Function calling (`name(args)`).
* Parameters create local variables within function scope.
* Functions support lexical scoping (closures).

### Local Variables:
* Variables declared within code blocks (`{}`) or function bodies are local to that scope.
* Correct handling of variable shadowing.

---

## Error Handling & Robustness:

* Runtime errors for type mismatches (e.g., non-numeric operands for arithmetic), division by zero, undefined variables, list index out of bounds, calling non-callable types, incorrect function argument counts, and variable redefinition in the same scope.
* Single-line comments (`//`).
* Statement termination with semicolons (`;`).

## 1. How to Run MyPi Programs

### 1.1. Prerequisites

* **Python 3.12:** Ensure Python 3 (e.g., Python 3.12 or newer) is installed on your computer, whilst older versions may work they have not been tested. This will can be downlaoded directly from https://www.python.org/downloads/ 
### 1.2. Setup Steps

1.  **Download & Extract:**
    * Download the MyPi project zip archive.
    * Extract its contents to a folder on your computer (e.g., `MyPi/`).

2.  **Navigate to Project Directory:**
    * Open a terminal or command prompt (e.g., PowerShell on Windows, Terminal on macOS/Linux).
    * Change your current directory to the root of the extracted project folder. This folder should contain `main.py`, `README.md`, `examples/`, `Stages_Pass/`, `Errors/`'and all other `.py` files.
        ```bash
        cd /path/to/your/extracted/MyPi_Language
        # Example on Windows: cd C:\Users\'YourUser'\Downloads\MyPi
        ```
    * **(Optional but Recommended) Activate Virtual Environment:** If a `.venv` folder is present and you wish to use it, activate it:
        * **Windows (PowerShell):** `.\.venv\Scripts\Activate.ps1`
        * **Linux/macOS (Bash):** `source ./.venv/bin/activate`

### 1.3. Execute MyPi Code

Once in the project directory, run the `main.py` script, providing the path to your MyPi source file as an argument.

```bash
python main.py <path_to_your_executeable_file> ```

# Run one of the provided example files
python main.py examples/Example_1.txt
# Run a file that requires user input
python main.py examples/Example_3.txt
# The terminal will pause and prompt for input. Type your response and press Enter.
```

## 2. MyPi Language Features (Quick Reference)

### Data Types:
- **Numbers:** Integers (`10`), decimals (`3.14`).
- **Booleans:** `true`, `false`.
- **Strings:** `"hello world"`, `"Quotes: \"A\""`. Supports `\n`, `\t`, `\"`, `\\`, `\r`, `\0` escape sequences.
- **Lists:** `[]`, `[1, "item", true, nil, [nested]]`.
- **Nil:** Represents the absence of a value (like `null`).

### Variables:
- **Declare:** `var myVar = 10;` or `var anotherVar;` (defaults to `nil`).
- **Assign:** `myVar = "new value";`, `counter = counter + 1;`.
- **Scope:** Global (top-level) or Local (inside `{}` blocks or functions). Local variables can `shadow` global ones.

### Operators (Precedence from high to low):
- **Grouping:** `()`
- **List Indexing:** `myList[index]` (for read and assign)
- **Unary:** `-` (negation), `!` (logical NOT).
- **Multiplication/Division:** `*`, `/`.
- **Addition/Subtraction/Concatenation:** `+`, `-`.
    - `+` concatenates strings (e.g., `"Age: " + 30`).
    - `+` concatenates lists (e.g., `[1] + [2]`).
- **Comparison:** `>`, `>=`, `<`, `<=`.
- **Equality:** `==`, `!=` (strict type equality).
- **Logical:** `and`, `or`.
- **Assignment:** `=`.

### Control Flow:
- **If-Then-Else:** `if (condition) { ... } else { ... }`. `else` is optional. Nested conditionals are supported.
- **While Loops:** `while (condition) { ... }`. Nested loops are supported.
- **Code Blocks:** Group statements using `{}`.

### Functions:
- **Declare:** `fun myFunc(param1, param2) { ... }`.
- **Call:** `myFunc("arg1", 123);`.
- Parameters create local variables. Functions implicitly return `nil`.

### Built-in Functions:
- `print expression;`: Displays a value to the console.
- `input(prompt_string);`: Prompts user for input and returns it as a string. Prompt is optional.
- `list_append(list_obj, value);`: Adds `value` to `list_obj`.
- `list_remove_at(list_obj, index);`: Removes element from `list_obj` at `index`.


### 3. Troubleshooting

- **`can't open file '...main.py': [Errno 2] No such file or directory`**:
    - Ensure your terminal's current directory is the one containing `main.py`.
    - Verify `main.py` is correctly named (case-sensitive) and present in that directory.
- **`UnicodeDecodeError: 'charmap' codec can't decode byte...`**:
    - Your `.mipi` or `.txt` source file has an encoding issue. Open it in a text editor (e.g., VS Code, Notepad++) and **resave it explicitly as UTF-8 encoding**.
    - **Crucially, replace any "smart quotes" (`“ ”`) or other non-standard characters with standard straight quotes (`" "`).**
- **`Runtime error: ...`**:
    - An error occurred in your MyPi code during execution. The error message will describe the issue (e.g., `Division by zero`, `Undefined variable`, `Operand must be a number`), often with a line number. Review your MyPi code at the indicated line.
- **`No module named '...'`**:
    - All Python source files (`Token.py`, `ast.py`, `Lexer.py`, `Parser.py`, `Interpreter.py`, `main.py`) must be in the same directory.
- **Python Version:**
    - MyPi requires **Python 3.12**. If you have multiple Python versions installed, ensure the `python` command in your terminal links to Python 3, or explicitly use `python3 main.py`.

For a detailed list of all features and their technical implementation notes, please refer to `FEATURE_LIST.md`.


### 4. Testing Strategy

The interpreter's functionality was validated through a comprehensive, stage-by-stage testing approach:

-   **Unit-like Tests:** Each new feature was tested in isolation, starting from basic arithmetic (Stage 1) and incrementally adding complexity (Boolean logic, strings, variables, control flow, lists, functions). This allowed for focused debugging and confirmation of individual components.
-   **Error Testing:** Specific test cases were designed to trigger expected runtime errors (e.g., division by zero, type mismatches, out-of-bounds access, incorrect argument counts), confirming robust error handling and controlled program termination.
-   **Reproducibility:** All example source files are provided and designed to run correctly with the interpreter, allowing for easy verification of functionality.

---

## 5. Provided Example Source Files

The `examples/` directory contains several  `.txt` source files demonstrating various features of the MyPi language.

* `examples/Example_1.txt`
    * **Purpose:** Tests the foundational arithmetic operations (addition, subtraction, multiplication, division, unary negation, parentheses) from **Stage 1: Basic Calculator**. Also introduces and verifies the basic creation, assignment, and usage of **Global Variables** from **Stage 4**.
    * **Key Features Demonstrated:** Numbers, basic operators, `var` declaration, `print` statement.

* `examples/Example_2.txt`
    * **Purpose:** Verifies **Stage 2: Boolean Logic** (boolean literals, comparison, equality, logical operators) and **Stage 3: Text Values** (string literals, concatenation, equality, escape sequences). It also demonstrates type interaction decisions.
    * **Key Features Demonstrated:** `true`/`false`, `and`/`or`/`!`, `==`/`!=`, `>`, etc., string literals, `+` for string concat, `\n`/`\t` escapes.

* `examples/Example_3.txt`
    * **Purpose:** Tests **Stage 5: Control Flow** (basic `if-then-else` and `while` loops, including nesting) and the **User Input** feature.
    * **Key Features Demonstrated:** `if`/`else` statements, `while` loops, nested control flow, `input()` built-in, variable updates within loops.

* `examples/Ex_4.txt`
    * **Purpose:** Focuses on the **List Data Structure** feature from **Stage 6: Additional Features**. It verifies list literals, element access (read and write), list concatenation, and the built-in `list_append` and `list_remove_at` functions.
    * **Key Features Demonstrated:** `[]` for lists, `myList[index]`, `+` for list concat, `list_append()`, `list_remove_at()`.

*`examples/Ex_5.txt`
    * **Purpose:** Demonstrates **Function-Based Code Reusability** and **Local Variables** from **Stage 6: Additional Features**. It covers function declaration, calls, parameter passing, local scoping, global variable interaction, and shadowing.
    * **Key Features Demonstrated:** `fun` declaration, function calls, parameters, local variables, global variable modification from functions, variable shadowing.



### 6. Development Testing Files (`Stage_Pass/sX.txt`)

During the development process, a set of specific test files, named in the pattern `Stage_Pass/sX.txt` (e.g., `s1.txt`, `s2.txt`, `s3.txt`, `s4.txt`, `s5.txt`, `s5A.txt`, `s6.txt`), were created.

These files serve as **demonstrations of each stage's successful implementation and full functionality.**

-   **Purpose:** Each `sX.txt` file contains MyPi code specifically designed to thoroughly test all features introduced in its corresponding development stage (Stage X), encompassing all examples from the assignment brief.
-   **Verification:** Upon execution, these files produced output that precisely matched the expected results for all features of that stage, providing concrete evidence of correct implementation.
-   **Progress Tracking:** These files acted as crucial checkpoints, confirming the interpreter's ability to reliably process and execute language features up to that point before proceeding with the implementation of subsequent, more complex stages. They represent the "pass" state for each stage's requirements.

**Example:**
-   `s1.txt`  demonstrates the full functionality of the basic calculator from Stage 1.
-   `s4.txt` verifies all aspects of global variable handling from Stage 4.
-   `s5A.txt` showcases the complete implementation of advanced control flow features (nested `if`/`while`, `else if` structures) from Stage 5.
-   `s6.txt`  showcases **Stage 6: Additional Features**, encompassing both the **List Data Structure** and **Function-Based Code Reusability**
