import re
from rich.markdown import Markdown
from rich.syntax import Syntax
from rich.console import Console
from rich.panel import Panel

console = Console()

def format_message(message: str) -> None:
    """
    Format and print a chat message with proper rendering of code blocks
    """
    # Split the message into parts with and without code blocks
    parts = re.split(r'(```(?:[\w]*)\n[\s\S]*?\n```)', message)
    
    for part in parts:
        # If this is a code block
        if part.startswith('```') and part.endswith('```'):
            # Extract the language and code
            match = re.match(r'```([\w]*)\n([\s\S]*?)\n```', part)
            if match:
                language, code = match.groups()
                language = language or "text"  # Default to "text" if no language is specified
                
                # Display the code with syntax highlighting
                syntax = Syntax(code, language, theme="monokai", line_numbers=True)
                console.print(Panel(syntax, border_style="dim"))
        else:
            # For non-code parts, render as markdown
            if part.strip():
                console.print(Markdown(part))