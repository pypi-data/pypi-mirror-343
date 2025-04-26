# DotCommandParser

DotCommandParser is a Python module for parsing and executing dot-separated commands with arguments. It provides support for error correction by suggesting probable commands based on previous inputs.

## Installation

You can install the module via pip:


## Usage Example

```python
from dotcommandparser import DotCommandParser

# Initialize the parser with some commands
parser = DotCommandParser()

# Execute a command
parser.execute_command("commands.test")

# Show available commands
parser.execute_command("commands.show")

# Execute a non-existent command (Error handling example)
parser.execute_command("unknown_command")

# Example Functions
def set_color(color):
    print(f">> Background color set to {color}")

def set_colors(foreground, background):
    print(f">> Foreground: {foreground}, Background: {background}")

# Make a dictionary
COMMANDS = {
    "chat": {
        "font": {
            "color": set_color,
        },
        "icon": {
            "color": set_colors,
        },
    },
}

parser2 = DotCommandParser(COMMANDS)
parser2.execute_command("chat.icon.color.white,black")
