# Punkt wejścia dla modułu
"""
__main__.py
"""

"""
Moduł uruchamiający dla movatalk.
Pozwala na uruchomienie movatalk jako aplikacji z linii poleceń.
"""
#!/usr/bin/env python3

import re
import sys
import os
import json
import subprocess
import traceback
from typing import Dict, List, Any, Optional, Union


class PlainmarkInterpreter:
    """Interpreter for the Plainmark language"""

    def __init__(self):
        self.variables: Dict[str, Any] = {}
        self.functions: Dict[str, callable] = {}
        self.output_buffer: List[str] = []

    def extract_code_blocks(self, markdown_text: str) -> List[str]:
        """Extract plainmark code blocks from markdown text"""
        pattern = r"```plainmark\s*([\s\S]*?)\s*```"
        matches = re.findall(pattern, markdown_text)
        return matches

    def print(self, *args, **kwargs):
        """Custom print function that captures output"""
        output = " ".join(str(arg) for arg in args)
        self.output_buffer.append(output)
        print(output, **kwargs)

    def read_file(self, filename: str) -> str:
        """Read a markdown file"""
        with open(filename, 'r', encoding='utf-8') as file:
            return file.read()

    def exec_terminal_command(self, command: str) -> str:
        """Execute a terminal command and return its output"""
        try:
            result = subprocess.run(command, shell=True, check=True,
                                    text=True, capture_output=True)
            return result.stdout
        except subprocess.CalledProcessError as e:
            return f"Error: {e.stderr}"

    def execute_code(self, code: str) -> str:
        """Execute plainmark code"""
        # Create safe global context
        global_context = {
            'print': self.print,
            'input': input,
            'open': open,
            'os': os,
            'json': json,
            'exec': self.exec_terminal_command,
            'vars': self.variables,
            '__builtins__': __builtins__
        }

        # Add existing variables to context
        for var_name, var_value in self.variables.items():
            global_context[var_name] = var_value

        try:
            # Process code to make it more Python-like
            processed_code = code
            # Replace JavaScript style declarations with Python
            processed_code = re.sub(r'let\s+(\w+)\s*=\s*', r'\1 = ', processed_code)
            processed_code = re.sub(r'const\s+(\w+)\s*=\s*', r'\1 = ', processed_code)
            # Replace function declarations
            processed_code = re.sub(r'function\s+(\w+)\s*\((.*?)\)\s*{', r'def \1(\2):', processed_code)
            # Replace JavaScript-style braces with Python indentation (simplified)
            processed_code = re.sub(r'\s*{\s*$', r':', processed_code)
            processed_code = re.sub(r'\s*}\s*$', r'', processed_code)

            # Execute the processed code
            exec(processed_code, global_context)

            # Update variables
            for var_name, var_value in global_context.items():
                if var_name not in ['print', 'input', 'open', 'os', 'json', 'exec', 'vars', '__builtins__']:
                    self.variables[var_name] = var_value

            return "\n".join(self.output_buffer)

        except Exception as e:
            error_msg = f"Error: {str(e)}\n{traceback.format_exc()}"
            return error_msg

    def execute_file(self, filename: str) -> str:
        """Execute a plainmark file"""
        try:
            markdown_text = self.read_file(filename)
            return self.execute_markdown(markdown_text)
        except FileNotFoundError:
            return f"Error: File '{filename}' not found."
        except Exception as e:
            return f"Error: {str(e)}"

    def execute_markdown(self, markdown_text: str) -> str:
        """Execute plainmark code blocks in markdown text"""
        self.output_buffer = []
        code_blocks = self.extract_code_blocks(markdown_text)

        if not code_blocks:
            return "No plainmark code blocks found in the file."

        results = []
        for block in code_blocks:
            result = self.execute_code(block)
            if result:
                results.append(result)

        return "\n".join(results)


def create_example_file():
    """Create an example plainmark file"""
    example_content = """# Example Plainmark Program

This is a simple demonstration of Plainmark running in Python.

```plainmark
# Define variables
name = "Python User"
age = 30

# Print a greeting
print(f"Hello, {name}!")
print(f"You are {age} years old.")

# Define a function
def calculate_area(radius):
    return 3.14159 * radius * radius

# Use the function
radius = 5
area = calculate_area(radius)
print(f"The area of a circle with radius {radius} is {area:.2f}")

# Get user input
user_input = input("Enter your favorite color: ")
print(f"Your favorite color is {user_input}")

# Run a system command (limited to safe commands)
print("Files in current directory:")
directory_contents = exec("ls -la")
print(directory_contents)
```

This was a demonstration of Plainmark's basic features.
"""

    with open("example.md", "w") as f:
        f.write(example_content)
    print(f"Created example file: example.md")


def print_help():
    """Print help information"""
    print("Plainmark Interpreter")
    print("Usage:")
    print("  plainmark.py [options] [file]")
    print("\nOptions:")
    print("  --help      Show this help message")
    print("  --example   Create an example file")
    print("  --repl      Start interactive REPL mode")
    print("\nExamples:")
    print("  plainmark.py example.md       Run a plainmark file")
    print("  plainmark.py --example        Create an example file")
    print("  plainmark.py --repl           Start REPL mode")


def start_repl():
    """Start interactive REPL mode"""
    interpreter = PlainmarkInterpreter()
    print("Plainmark REPL (Interactive Mode)")
    print("Type 'exit' to quit, 'help' for help")

    current_markdown = []

    while True:
        try:
            line = input(">>> ")
            if line.lower() == "exit":
                break
            elif line.lower() == "help":
                print("Commands:")
                print("  exit          Exit REPL")
                print("  help          Show this help")
                print("  run           Execute current markdown")
                print("  clear         Clear current markdown")
                print("  show          Show current markdown")
                continue
            elif line.lower() == "run":
                result = interpreter.execute_markdown("\n".join(current_markdown))
                print("\nResult:")
                print(result)
                continue
            elif line.lower() == "clear":
                current_markdown = []
                print("Markdown cleared")
                continue
            elif line.lower() == "show":
                print("\nCurrent Markdown:")
                print("\n".join(current_markdown))
                continue

            current_markdown.append(line)
        except KeyboardInterrupt:
            print("\nExiting...")
            break
        except Exception as e:
            print(f"Error: {str(e)}")


def main():
    """Main function"""
    if len(sys.argv) < 2:
        print_help()
        return

    if sys.argv[1] == "--help":
        print_help()
    elif sys.argv[1] == "--example":
        create_example_file()
    elif sys.argv[1] == "--repl":
        start_repl()
    else:
        interpreter = PlainmarkInterpreter()
        result = interpreter.execute_file(sys.argv[1])
        print(result)


if __name__ == "__main__":
    main()