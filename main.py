import sys
from Lexer import Lexer
from Parser import Parser
from Interpreter import Interpreter


def run_file(file_path: str):
    """
    Reads a source code file, tokenizes it, parses it, and then interprets the statements.
    Processes the entire file content as a single program.
    """
    try:
        with open(file_path, 'r') as file:
            source_code = file.read()  # Read the entire content of the file

        print(f"--- Interpreting file: '{file_path}' ---")

        # 1. Lexing: Convert the entire source code into a list of tokens.
        lexer = Lexer(source_code)  # Pass the *entire* source_code string
        tokens = lexer.scan_tokens()
        # print("Tokens:", tokens) # Uncomment for debugging tokens

        # 2. Parsing: Convert the list of tokens into a list of Abstract Syntax Tree (AST) statements.
        parser = Parser(tokens)
        statements = parser.parse()  # Get all statements from the file
        # print("AST:", statements) # Uncomment for debugging AST structure

        # 3. Interpretation: Execute the AST statements.
        interpreter = Interpreter()
        interpreter.interpret(statements)  # Interpret all statements

        print("-" * 40)  # Readability

    except FileNotFoundError:
        print(f"Error: File '{file_path}' not found.")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")


# Main execution block
if __name__ == "__main__":
    # Check if a file path argument is provided when running the script.
    if len(sys.argv) < 2:
        print("Usage: python main.py <source_file_path>")
        sys.exit(1)  # Exit with an error code

    # Get the file path from the command-line arguments.
    source_file = sys.argv[1]
    run_file(source_file)  # Run the interpreter with the provided file
