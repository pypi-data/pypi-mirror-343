import time
import typer
from typing import Optional
from rich.console import Console
from rich.progress import Progress, TextColumn, BarColumn, TaskProgressColumn

from nia_cli.utils.http import api_request, ApiError
from nia_cli.config import load_config

console = Console()

def index(project_id: Optional[str] = None):
    """
    Index a repository for the given project
    """
    config = load_config()
    project_id = project_id or config.default_project
    
    if not project_id:
        console.print("[yellow]No project selected. Use 'nia start select' to choose a project.[/]")
        return
    
    try:
        # Start indexing - use consistent endpoint pattern with user_id=me
        with console.status("[bold green]Starting indexing..."):
            # Trigger indexing for the project
            index_data = {"user_id": "me"}
            response = api_request("POST", f"/projects/{project_id}/index", data=index_data)
        
        console.print("[bold green]Indexing started![/]")
        
        # Create progress display
        with Progress(
            TextColumn("[bold blue]{task.description}"),
            BarColumn(),
            TaskProgressColumn(),
            console=console
        ) as progress:
            task = progress.add_task("[bold green]Indexing repository...", total=100)
            
            # Poll for status
            while True:
                status_response = api_request("GET", f"/projects/{project_id}/status?user_id=me")
                status = status_response.get("status", "").lower()
                progress_value = status_response.get("progress", 0)
                
                # Update progress
                progress.update(task, completed=progress_value)
                
                if status == "error":
                    error_message = status_response.get("error", "Unknown error")
                    console.print(f"[bold red]Indexing failed: {error_message}[/]")
                    return
                
                if status == "ready":
                    progress.update(task, completed=100)
                    console.print("[bold green]Indexing completed successfully![/]")
                    break
                
                time.sleep(3)  # Poll every 3 seconds
        
        console.print("[bold green]You can now chat with your codebase using 'nia chat'[/]")
    
    except KeyboardInterrupt:
        console.print("\n[yellow]Indexing operation was canceled by user...[/]")
        # Attempt to cancel the operation
        try:
            api_request("POST", f"/api/projects/{project_id}/cancel")
            console.print("[bold yellow]Indexing canceled.[/]")
        except:
            console.print("[bold red]Could not cancel indexing properly.[/]")
    
    except ApiError as e:
        console.print(f"[bold red]Error: {str(e)}[/]")