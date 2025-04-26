import typer
from typing import Optional
from rich.console import Console
from rich.markdown import Markdown
from rich.prompt import Confirm
from prompt_toolkit import PromptSession
from prompt_toolkit.history import InMemoryHistory

from nia_cli.utils.http import api_request, stream_api_request, ApiError
from nia_cli.config import load_config

console = Console()

def chat(
    repository_id: Optional[str] = None,
    additional_repository_ids: Optional[str] = None
):
    """
    Start a chat session with one or more repositories
    
    If additional_repository_ids is provided, it should be a comma-separated list of repository IDs
    """
    config = load_config()
    
    # Use provided repository_id or default from config
    repo_id = repository_id or config.default_project
    
    if not repo_id:
        console.print("[bold red]No repository specified and no default set.[/]")
        console.print("[yellow]Use 'nia list' to see repositories.[/]")
        console.print("[yellow]Select a default repository with 'nia select'[/]")
        console.print("[yellow]Or specify a repository ID: 'nia chat <repository_id>'[/]")
        return
    
    # Parse additional repository IDs if provided
    additional_repos = []
    if additional_repository_ids:
        additional_repo_ids = [id.strip() for id in additional_repository_ids.split(",")]
    else:
        additional_repo_ids = []
    
    # Verify all repositories exist
    repositories = []
    try:
        # Verify primary repository
        primary_repository = api_request("GET", f"/v2/repositories/{repo_id}")
        
        if not primary_repository:
            console.print(f"[bold red]Repository with ID {repo_id} not found.[/]")
            console.print("[yellow]Try running 'nia list' to see available repositories and their IDs.[/]")
            return
        
        # Extract repository name from the response - this should be in "owner/repo" format
        repository_name = primary_repository.get("repository", "Unknown")
        status = primary_repository.get("status", "unknown")
        
        # Check if repository is indexed
        if status != "indexed":
            console.print(f"[bold yellow]Warning: Repository status is '{status}', not 'indexed'[/]")
            console.print("[yellow]Chat may not work if the repository is not fully indexed.[/]")
            if not Confirm.ask("[bold]Continue anyway?[/]"):
                return
        
        # Verify we have a valid repository name in owner/repo format
        if repository_name == "Unknown" or "/" not in repository_name:
            console.print("[bold red]Error: Could not determine repository name in owner/repo format[/]")
            console.print("[yellow]Please try again with a different repository ID.[/]")
            return
            
        # Add primary repository to our repositories list
        repositories.append({"repository": repository_name})
        
        # Verify additional repositories if provided
        for additional_id in additional_repo_ids:
            additional_repo = api_request("GET", f"/v2/repositories/{additional_id}")
            
            if not additional_repo:
                console.print(f"[bold red]Additional repository with ID {additional_id} not found.[/]")
                if not Confirm.ask("[bold]Continue without this repository?[/]"):
                    return
                continue
                
            additional_repo_name = additional_repo.get("repository", "Unknown")
            additional_status = additional_repo.get("status", "unknown")
            
            # Check if additional repository is indexed
            if additional_status != "indexed":
                console.print(f"[bold yellow]Warning: Additional repository status is '{additional_status}', not 'indexed'[/]")
                if not Confirm.ask("[bold]Continue with this repository anyway?[/]"):
                    continue
            
            # Verify we have a valid repository name in owner/repo format
            if additional_repo_name == "Unknown" or "/" not in additional_repo_name:
                console.print(f"[bold red]Error: Could not determine repository name for {additional_id}[/]")
                if not Confirm.ask("[bold]Continue without this repository?[/]"):
                    return
                continue
                
            # Add additional repository to our repositories list
            repositories.append({"repository": additional_repo_name})
            
        # Print summary of repositories being used
        if len(repositories) == 1:
            console.print(f"[bold green]Chatting with repository:[/] {repository_name}")
        else:
            console.print(f"[bold green]Chatting with primary repository:[/] {repository_name}")
            console.print("[bold green]Additional repositories:[/]")
            for repo in repositories[1:]:
                console.print(f"  - {repo['repository']}")
                
    except ApiError as e:
        console.print(f"[bold red]Error accessing repository: {str(e)}[/]")
        console.print("[yellow]The repository ID might be incorrect or the repository might have been deleted.[/]")
        console.print("[yellow]Try running 'nia list' to see available repositories.[/]")
        return
    except Exception as e:
        console.print(f"[bold red]Unexpected error: {str(e)}[/]")
        return
    
    # Start chat session
    history = InMemoryHistory()
    session = PromptSession(history=history)
    messages = []
    
    console.print("[bold yellow]Starting chat session. Type 'exit' to quit.[/]")
    
    while True:
        try:
            # Get user input
            user_input = session.prompt("\n[You]: ")
            
            # Check for exit command
            if user_input.lower() in ["exit", "quit", "q"]:
                console.print("[bold green]Ending chat session.[/]")
                break
                
            # Skip empty messages
            if not user_input.strip():
                continue
            
            # Add user message to history
            messages.append({"role": "user", "content": user_input})
            
            # Prepare API request
            # The API expects a "repository" field in the repositories list, not repository_id
            data = {
                "messages": messages,
                "repositories": repositories,
                "include_sources": True
            }
            
            
            # Make API request
            console.print("")
            import random
            import time
            
            thinking_messages = [
                "Thinking...",
                "Searching your spaghetti code...",
                "Vibing with your repository...",
                "Decoding your masterpiece...",
                "Untangling your logic...",
                "Analyzing code patterns...",
                "Finding digital breadcrumbs...",
                "Connecting the dots..."
            ]
            
            start_time = time.time()
            message_index = 0
            
            def get_elapsed_text():
                elapsed = int(time.time() - start_time)
                return f"[dim]({elapsed}s)[/]"
            
            with console.status(f"[bold green]{thinking_messages[0]}[/] {get_elapsed_text()}", refresh_per_second=4) as status:
                def update_status():
                    nonlocal message_index
                    elapsed = int(time.time() - start_time)
                    if elapsed > 0 and elapsed % 5 == 0:
                        message_index = (message_index + 1) % len(thinking_messages)
                    status.update(f"[bold green]{thinking_messages[message_index]}[/] {get_elapsed_text()}")
                
                try:
                    # Set up periodic status updates
                    import threading
                    stop_thread = False
                    def status_updater():
                        while not stop_thread:
                            update_status()
                            time.sleep(0.25)
                    
                    update_thread = threading.Thread(target=status_updater)
                    update_thread.daemon = True
                    update_thread.start()
                    
                    # Try v2 API with a longer timeout for chat queries
                    response = api_request("POST", "/v2/query", data=data, timeout=240)
                    
                    # Stop the status updater thread
                    stop_thread = True
                    update_thread.join(0.5)
                    
                    # Process response
                    if response:
                        content = response.get("content", "")
                        sources = response.get("sources", [])
                        
                        # Display response
                        console.print("[bold cyan][Nia]:[/]")
                        console.print(Markdown(content))
                        
                        # Display sources if available
                        if sources and len(sources) > 0:
                            console.print("\n[bold yellow]Sources:[/]")
                            for i, source in enumerate(sources, 1):
                                if isinstance(source, dict):
                                    file_path = source.get("file_path", "Unknown")
                                    console.print(f"  {i}. {file_path}")
                                elif isinstance(source, str):
                                    console.print(f"  {i}. {source}")
                        
                        # Add assistant message to history
                        messages.append({"role": "assistant", "content": content})
                    else:
                        console.print("[bold red]Error: Empty response from API[/]")
                except ApiError as e:
                    # Stop the status updater thread if it exists
                    if 'stop_thread' in locals():
                        stop_thread = True
                        update_thread.join(0.5)
                    console.print(f"[bold red]API Error: {str(e)}[/]")
                except Exception as e:
                    # Stop the status updater thread if it exists
                    if 'stop_thread' in locals():
                        stop_thread = True
                        update_thread.join(0.5)
                    console.print(f"[bold red]Error: {str(e)}[/]")
                    
        except KeyboardInterrupt:
            console.print("\n[bold yellow]Chat session interrupted.[/]")
            break
        except EOFError:
            console.print("\n[bold yellow]Chat session ended.[/]")
            break