import typer
from typing import Optional
from rich.console import Console
from rich.table import Table
from rich.prompt import Prompt, Confirm
from rich.progress import Progress, SpinnerColumn, TextColumn, BarColumn, TimeElapsedColumn

from nia_cli.utils.http import api_request, ApiError
from nia_cli.config import load_config, save_config

app = typer.Typer(help="Manage and start projects")
console = Console()

def list_projects():
    """
    List all your repositories
    """
    try:
        console.print("[bold yellow]Listing repositories...[/]")
        
        # Get repositories using v2 API
        repos = api_request("GET", "/v2/repositories")
        
        if repos and isinstance(repos, list):
            if len(repos) > 0:
                console.print("[bold green]Found repositories[/]")
                
                table = Table(title="Your Repositories")
                table.add_column("#", style="dim")
                table.add_column("ID", style="dim")
                table.add_column("Repository", style="green")
                table.add_column("Branch", style="blue")
                table.add_column("Status", style="yellow")
                
                for i, repo in enumerate(repos, 1):
                    repo_id = repo.get("repository_id", "N/A")
                    table.add_row(
                        str(i),
                        repo_id,
                        repo.get("repository", "Unnamed"),
                        repo.get("branch", "main"),
                        repo.get("status", "Unknown")
                    )
                
                console.print(table)
                console.print("[dim]Note: Use the ID column value with 'nia chat <ID>' or 'nia select <ID>'[/]")
            else:
                console.print("[yellow]No repositories found. Create one with 'nia create <repo>'[/]")
        else:
            console.print("[yellow]Unexpected API response format. Try creating a new repository.[/]")
            
    except ApiError as e:
        console.print(f"[bold red]Error: {str(e)}[/]")
    except Exception as e:
        console.print(f"[bold red]Unexpected error: {str(e)}[/]")

def create_project(
    repository: str,
    branch: str = None
):
    """
    Create a new repository by indexing a GitHub repository
    """
    try:
        console.print("[bold yellow]Creating repository...[/]")
        
        # Prompt for branch if not provided
        if branch is None:
            branch = Prompt.ask(
                f"[bold]Enter branch name for {repository}[/]",
                default="main"
            )
        
        # Format repository for v2 API
        repo_data = {
            "repository": repository,
            "branch": branch
        }
        
        with console.status("[bold green]Creating repository..."):
            response = api_request("POST", "/v2/repositories", data=repo_data)
        
        if isinstance(response, dict) and "data" in response:
            repo_id = response["data"].get("repository_id")
            if repo_id:
                console.print(f"[bold green]Repository created successfully![/]")
                
                # Set as default project
                config = load_config()
                config.default_project = repo_id
                save_config(config)
                
                console.print(f"[yellow]Indexing started automatically. Check status with 'nia status {repo_id}'[/]")
                return repo_id
            else:
                console.print("[bold red]Failed to get repository ID from API response.[/]")
        else:
            console.print("[bold red]Unexpected API response format.[/]")
            
    except ApiError as e:
        console.print(f"[bold red]Error creating repository: {str(e)}[/]")
    except Exception as e:
        console.print(f"[bold red]Unexpected error: {str(e)}[/]")

def check_status(
    repository_id: Optional[str] = None
):
    """
    Check indexing status of a repository
    """
    try:
        config = load_config()
        
        # Use provided repository_id or default from config
        repo_id = repository_id or config.default_project
        
        if not repo_id:
            console.print("[yellow]No repository specified and no default set.[/]")
            console.print("[yellow]Use 'nia list' to see your repositories.[/]")
            return
        
        console.print(f"[bold yellow]Checking status of repository {repo_id}...[/]")
        
        response = api_request("GET", f"/v2/repositories/{repo_id}", timeout=60)
        
        if response:
            repo_name = response.get("repository", "Unknown")
            status = response.get("status", "unknown")
            progress = response.get("progress", {})
            
            # Format status nicely
            status_color = "green" if status == "indexed" else "yellow" if status == "indexing" else "red"
            
            console.print(f"[bold]Repository:[/] {repo_name}")
            console.print(f"[bold]Status:[/] [{status_color}]{status}[/{status_color}]")
            
            # Show progress details if available
            if progress:
                percentage = progress.get("percentage", 0)
                stage = progress.get("stage", "unknown")
                message = progress.get("message", "")
                
                console.print(f"[bold]Progress:[/] {percentage}%")
                console.print(f"[bold]Current stage:[/] {stage}")
                if message:
                    console.print(f"[bold]Message:[/] {message}")
                    
                # Show a progress bar
                with Progress(
                    SpinnerColumn(),
                    TextColumn("[progress.description]{task.description}"),
                    BarColumn(),
                    TextColumn("[progress.percentage]{task.percentage:>3.0f}%"),
                    TimeElapsedColumn(),
                    console=console
                ) as progress_bar:
                    task = progress_bar.add_task("[green]Indexing progress", total=100, completed=percentage)
                    
            # Show error if any
            if status == "error":
                error = response.get("error", "Unknown error")
                console.print(f"[bold red]Error:[/] {error}")
        else:
            console.print("[bold red]Could not retrieve repository status.[/]")
                
    except ApiError as e:
        console.print(f"[bold red]Error: {str(e)}[/]")
    except Exception as e:
        console.print(f"[bold red]Unexpected error: {str(e)}[/]")

def select_project(repository_id: Optional[str] = None):
    """
    Select a repository to use by default
    """
    if not repository_id:
        # List repositories and prompt for selection
        repos = None
        try:
            repos = api_request("GET", "/v2/repositories")
            
            if not repos or len(repos) == 0:
                console.print("[yellow]You don't have any repositories yet. Create one with 'nia create <owner/repo>'[/]")
                return
            
            table = Table(title="Select a Repository")
            table.add_column("#", style="dim")
            table.add_column("ID", style="dim")
            table.add_column("Repository", style="green")
            table.add_column("Status", style="blue")
            
            for i, repo in enumerate(repos, 1):
                repo_id = repo.get("repository_id", "N/A")
                table.add_row(
                    str(i),
                    repo_id,
                    repo.get("repository", "Unknown"),
                    repo.get("status", "Unknown")
                )
            
            console.print(table)
            
            choice = Prompt.ask(
                "[bold]Enter the number of the repository to select[/]",
                choices=[str(i) for i in range(1, len(repos) + 1)]
            )
            
            # Get the actual repository ID from selected item
            selected_repo = repos[int(choice) - 1]
            repository_id = selected_repo.get("repository_id")
            
            # Validate that this ID exists
            try:
                check_response = api_request("GET", f"/v2/repositories/{repository_id}", timeout=60)
                if not check_response:
                    console.print(f"[bold yellow]Warning: Could not verify repository with ID {repository_id}[/]")
                else:
                    # Additional validation of the repository
                    repo_name = check_response.get("repository", "Unknown")
                    repo_status = check_response.get("status", "unknown")
                    
                    if repo_status != "indexed":
                        console.print(f"[bold yellow]Warning: Repository is not fully indexed (status: {repo_status})[/]")
                        
                    if not repository_id or not repo_name or repo_name == "Unknown":
                        console.print("[bold yellow]Warning: Repository details incomplete[/]")
            except Exception as e:
                console.print(f"[bold yellow]Warning: {str(e)}[/]")
                console.print("[bold yellow]This repository ID might not be valid for API requests.[/]")
                
        except ApiError as e:
            console.print(f"[bold red]Error: {str(e)}[/]")
            return
        except Exception as e:
            console.print(f"[bold red]Error listing repositories: {str(e)}[/]")
            return
    
    # Save the selection
    if repository_id:
        config = load_config()
        config.default_project = repository_id
        save_config(config)
        
        console.print(f"[bold green]Repository selected as default[/]")
        console.print(f"[yellow]You can now use 'nia chat' without specifying a repository ID[/]")
    else:
        console.print(f"[bold red]No repository ID selected[/]")