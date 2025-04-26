#!/usr/bin/env python3
import os
import sys
import typer
from typing import Optional
from rich.console import Console

# Import functions directly from command modules
from nia_cli.commands.start import list_projects, create_project, check_status, select_project
from nia_cli.commands.chat import chat
from nia_cli.config import load_config, Config, save_config
from nia_cli.auth import login as auth_login

app = typer.Typer(help="NIA - Code Assistant CLI")
console = Console()

@app.callback()
def callback():
    """
    NIA CLI - Chat with your codebase
    """
    # Initialize config if it doesn't exist
    config_dir = os.path.expanduser("~/.nia")
    if not os.path.exists(config_dir):
        os.makedirs(config_dir, exist_ok=True)
        save_config(Config())

@app.command()
def login(api_key: Optional[str] = None):
    """
    Authenticate with NIA using an API key
    """
    auth_login(api_key)

@app.command()
def list():
    """
    List all your repositories
    """
    list_projects()

@app.command()
def create(
    repository: str = typer.Argument(..., help="GitHub repository (owner/repo format)"),
    branch: Optional[str] = typer.Option(None, "--branch", "-b", help="Branch name to index (will prompt if not provided)")
):
    """
    Create a new repository
    """
    create_project(repository, branch)

@app.command()
def status(
    repository_id: Optional[str] = typer.Argument(None, help="Repository ID (uses default if not specified)")
):
    """
    Check indexing status of a repository
    """
    check_status(repository_id)

@app.command()
def select(
    repository_id: Optional[str] = typer.Argument(None, help="Repository ID to set as default")
):
    """
    Select a repository to use by default
    """
    select_project(repository_id)

@app.command()
def chat(
    repository_id: Optional[str] = typer.Argument(None, help="Repository ID (uses default if not specified)"),
    additional: Optional[str] = typer.Option(None, "--additional", "-a", help="Comma-separated list of additional repository IDs to include")
):
    """
    Chat with one or more repositories
    """
    from nia_cli.commands.chat import chat as chat_function
    chat_function(repository_id, additional)

def main():
    # Check if user is authenticated
    config = load_config()
    if len(sys.argv) > 1 and sys.argv[1] != "login" and not config.api_key:
        console.print("[bold red]Not authenticated. Please run 'nia login' first.[/]")
        return
    
    # If no command is provided, show welcome screen
    if len(sys.argv) == 1:
        import random
        
        # ASCII art logo with color
        logo = """
[bold cyan] _   _ [/][bold yellow]_[/][bold magenta]    [/]
[bold cyan]| \\ | |[/][bold yellow](_)[/][bold magenta]__ _ [/]
[bold cyan]|  \\| |[/][bold yellow]| /[/][bold magenta] _` |[/]
[bold cyan]| |\\  |[/][bold yellow]| |[/][bold magenta] (_| |[/]
[bold cyan]|_| \\_|[/][bold yellow]|_|[/][bold magenta]\\__,_|[/]"""
    
        taglines = [
            "🧠 Your AI-powered code companion",
            "✨ Supercharge your coding experience",
            "🔍 Explore your codebase intelligently",
            "💡 Code smarter, not harder",
            "🚀 Take your development to the next level"
        ]
        
        # Display ASCII logo and random tagline
        console.print(logo)
        console.print(f"[bold yellow]{random.choice(taglines)}[/]", justify="center")
        console.print("")
        
        # Show version info
        console.print("[dim]v1.0.0[/]", justify="right")
        console.print("")
        
        # Commands in a nice panel with categories
        from rich.panel import Panel
        from rich.table import Table
        from rich.align import Align
        
        command_table = Table(show_header=False, box=None, padding=(0, 2))
        
        # Authentication commands
        command_table.add_row("[bold magenta]Authentication[/]")
        command_table.add_row("[bold]nia login[/]", "Authenticate with your API key")
        command_table.add_row("")
        
        # Project commands
        command_table.add_row("[bold yellow]Projects[/]")
        command_table.add_row("[bold]nia list[/]", "List your repositories")
        command_table.add_row("[bold]nia create[/] [cyan]REPO[/]", "Create a new repository (owner/repo format)")
        command_table.add_row("[bold]nia status[/] [cyan][REPO_ID][/]", "Check repository indexing status")
        command_table.add_row("[bold]nia select[/] [cyan][REPO_ID][/]", "Select default repository")
        command_table.add_row("")
        
        # Chat commands
        command_table.add_row("[bold green]Chat[/]")
        command_table.add_row("[bold]nia chat[/] [cyan][REPO_ID][/]", "Chat with your code")
        command_table.add_row("", "[dim]Use --additional flag for multi-repo chat[/]")
        
        commands_panel = Panel(
            Align(command_table, align="center"),
            title="[bold]Available Commands[/]",
            border_style="blue",
            padding=(1, 2)
        )
        
        console.print(commands_panel)
        
        # Show tip at the bottom
        tip_messages = [
            "Tip: Use 'nia select' to set a default repository for faster access",
            "Tip: Multi-repository chats combine knowledge from multiple codebases",
            "Tip: Type 'exit' to end a chat session",
            "Tip: Try asking about code structure, bugs, or feature ideas"
        ]
        console.print(f"\n[dim]{random.choice(tip_messages)}[/]", justify="center")
        return
    
    app()

if __name__ == "__main__":
    main()