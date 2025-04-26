"""
API route to check the status of Nuanced integration.
"""
import os
import logging
import json
from fastapi import APIRouter, HTTPException, Depends, Path, Query
from pydantic import BaseModel
from typing import Dict, List, Optional, Any

# Import the NuancedService if available
try:
    from services.nuanced_service import NuancedService
    nuanced_available = True
except ImportError:
    nuanced_available = False

router = APIRouter(prefix="/api/nuanced", tags=["nuanced"])
logger = logging.getLogger(__name__)

class NuancedStatusResponse(BaseModel):
    """Response model for Nuanced status check."""
    is_installed: bool
    installation_details: Optional[Dict[str, Any]] = None
    integration_status: str
    nuanced_repos: Optional[List[Dict[str, Any]]] = None
    repositories_with_graphs: int = 0
    service_integrated: bool
    retriever_integrated: bool
    recommendations: List[str] = []

class NuancedStatus(BaseModel):
    """Response model for Nuanced status check"""
    is_installed: bool
    cli_available: bool
    library_available: bool
    version: Optional[str] = None
    python_version: Optional[str] = None
    
class GraphStorageInfo(BaseModel):
    """Response model for graph storage information"""
    project_id: str
    function_count: int
    module_count: int
    size_kb: float
    updated_at: Optional[str] = None
    call_relationships: int = 0
    format: str = "unknown"

class GraphGenerationResult(BaseModel):
    """Response model for graph generation results"""
    success: bool
    graph_path: Optional[str] = None
    function_count: int = 0
    module_count: int = 0
    call_relationships: int = 0
    stored_in_db: bool = False
    error: Optional[str] = None
    
class GraphData(BaseModel):
    """Response model for graph data"""
    project_id: str
    graph_data: Dict[str, Any]

@router.get("/status", response_model=NuancedStatus)
async def check_nuanced_status():
    """
    Check if Nuanced is properly installed and available.
    This endpoint helps diagnose issues with Nuanced integration.
    """
    try:
        logger.info("Checking Nuanced installation status")
        
        # Basic installation check
        is_installed = NuancedService.is_installed()
        
        # Get more detailed status information
        status = {
            "is_installed": is_installed,
            "cli_available": False,
            "library_available": False,
            "version": None,
            "python_version": None
        }
        
        # Get Python version
        try:
            import sys
            status["python_version"] = f"{sys.version_info.major}.{sys.version_info.minor}.{sys.version_info.micro}"
        except Exception as e:
            logger.warning(f"Failed to get Python version: {e}")
        
        # Check CLI availability
        try:
            import subprocess
            result = subprocess.run(
                ["nuanced", "--help"],
                capture_output=True,
                text=True
            )
            status["cli_available"] = result.returncode == 0
            if status["cli_available"]:
                status["version"] = "Detected (version unavailable via CLI)"
        except Exception as e:
            logger.warning(f"Failed to check CLI availability: {e}")
        
        # Check library availability
        try:
            import nuanced
            status["library_available"] = True
            status["version"] = getattr(nuanced, "__version__", status["version"] or "unknown")
        except ImportError:
            logger.warning("Nuanced Python library not installed")
        except Exception as e:
            logger.warning(f"Error checking Nuanced library: {e}")
        
        # Generate detailed logs for server console
        NuancedService.debug_logs()
        
        return status
    except Exception as e:
        logger.error(f"Error checking Nuanced status: {e}")
        raise HTTPException(status_code=500, detail=f"Failed to check Nuanced status: {str(e)}")

@router.post("/generate/{project_id}", response_model=GraphGenerationResult)
async def generate_test_graph(project_id: str = Path(..., description="Project ID to associate with the test graph")):
    """
    Generate a test Nuanced graph for a given project ID.
    This endpoint creates a test repository with sample Python code and generates a graph.
    
    Note: This is intended for diagnostics only and should not be used in production.
    """
    try:
        logger.info(f"Generating test Nuanced graph for project {project_id}")
        
        # Create test directory in /tmp
        test_dir = f"/tmp/nuanced_test_{project_id}"
        os.makedirs(test_dir, exist_ok=True)
        
        # Create a simple Python file with functions
        with open(f"{test_dir}/test_module.py", "w") as f:
            f.write("""
def greet(name):
    \"\"\"Greet a person by name\"\"\"
    return f"Hello, {name}!"

def calculate_sum(a, b):
    \"\"\"Calculate the sum of two numbers\"\"\"
    return a + b

def main():
    \"\"\"Main function that calls other functions\"\"\"
    name = "World"
    greeting = greet(name)
    result = calculate_sum(5, 10)
    print(f"{greeting} The sum is {result}.")

if __name__ == "__main__":
    main()
""")
        
        # Create a second Python file with a class
        with open(f"{test_dir}/test_class.py", "w") as f:
            f.write("""
class Calculator:
    \"\"\"A simple calculator class\"\"\"
    
    def __init__(self, initial_value=0):
        self.value = initial_value
    
    def add(self, x):
        \"\"\"Add a number to the current value\"\"\"
        self.value += x
        return self.value
    
    def subtract(self, x):
        \"\"\"Subtract a number from the current value\"\"\"
        self.value -= x
        return self.value
    
def create_calculator():
    \"\"\"Factory function to create a calculator\"\"\"
    return Calculator()

if __name__ == "__main__":
    calc = Calculator(10)
    print(f"Add 5: {calc.add(5)}")
    print(f"Subtract 3: {calc.subtract(3)}")
""")
        
        # Initialize Nuanced graph
        graph_path = NuancedService.init_graph(test_dir)
        
        if not graph_path:
            logger.warning(f"Failed to generate Nuanced graph in {test_dir}")
            return GraphGenerationResult(
                success=False,
                function_count=0,
                module_count=0,
                error="Failed to generate graph"
            )
        
        # Get graph statistics
        function_count = 0
        module_count = 0
        call_count = 0
        
        try:
            with open(graph_path, 'r') as f:
                graph_data = json.load(f)
                
            # Determine format and count functions/modules
            if "functions" in graph_data and "modules" in graph_data:
                # Traditional format
                function_count = len(graph_data.get("functions", {}))
                module_count = len(graph_data.get("modules", {}))
                
                # Count relationships
                for _, func_data in graph_data.get("functions", {}).items():
                    call_count += len(func_data.get("callees", []))
            else:
                # Flat format (function names as keys)
                function_count = len(graph_data)
                
                # Count relationships
                for _, func_data in graph_data.items():
                    call_count += len(func_data.get("callees", []))
        except Exception as e:
            logger.error(f"Error reading graph file: {e}")
        
        # Store in database if graph has any content
        stored = False
        if function_count > 0 or module_count > 0:
            stored = NuancedService.store_graph_in_db(project_id, graph_path)
            logger.info(f"Graph stored in database: {stored}")
            
            # Generate compact representation
            compact_graph = NuancedService.extract_compact_graph(graph_path)
            if compact_graph:
                compact_function_count = len(compact_graph.get("functions", {}))
                logger.info(f"Generated compact graph with {compact_function_count} function relationships")
            
        return GraphGenerationResult(
            success=True,
            graph_path=graph_path,
            function_count=function_count,
            module_count=module_count,
            call_relationships=call_count,
            stored_in_db=stored
        )
    
    except Exception as e:
        logger.error(f"Error generating test graph: {e}")
        return GraphGenerationResult(
            success=False,
            function_count=0,
            module_count=0,
            error=str(e)
        )

@router.get("/stored", response_model=List[GraphStorageInfo])
async def list_stored_graphs():
    """
    List all Nuanced graphs stored in the database.
    This endpoint helps verify that graphs are being properly stored.
    """
    try:
        from db import db
        
        if not hasattr(db, 'nuanced_graphs'):
            raise HTTPException(status_code=500, detail="MongoDB does not have nuanced_graphs collection")
        
        # Query MongoDB for all nuanced graphs
        graphs = list(db.nuanced_graphs.find({}))
        
        # Format results
        result = []
        for graph in graphs:
            graph_data = graph.get("graph_data", {})
            metadata = graph.get("metadata", {})
            
            # Determine format and count functions
            if "functions" in graph_data:
                # Traditional format
                function_count = len(graph_data.get("functions", {}))
                module_count = len(graph_data.get("modules", {}))
            else:
                # Flat format
                function_count = len(graph_data)
                module_count = 0
            
            # Calculate call relationships
            call_count = 0
            if "functions" in graph_data:
                # Traditional format
                for _, func_data in graph_data.get("functions", {}).items():
                    call_count += len(func_data.get("callees", []))
            else:
                # Flat format
                for _, func_data in graph_data.items():
                    call_count += len(func_data.get("callees", []))
                    
            # Create result object
            result.append(GraphStorageInfo(
                project_id=graph.get("project_id", "unknown"),
                function_count=function_count,
                module_count=module_count,
                call_relationships=call_count,
                size_kb=graph.get("size_kb", 0),
                updated_at=str(graph.get("updated_at", "unknown")),
                format=metadata.get("graph_format", "unknown")
            ))
        
        return result
    except Exception as e:
        logger.error(f"Error listing stored graphs: {e}")
        raise HTTPException(status_code=500, detail=f"Failed to list stored graphs: {str(e)}")

@router.get("/graph/{project_id}")
async def get_graph_for_project(project_id: str = Path(..., description="Project ID to retrieve the graph for")):
    """
    Retrieve the Nuanced graph for a specific project.
    This endpoint allows you to verify the graph data stored in the database.
    """
    try:
        # Retrieve graph from the database
        graph_data = NuancedService.get_graph_from_db(project_id)
        
        if not graph_data:
            raise HTTPException(status_code=404, detail=f"No graph found for project {project_id}")
        
        # Determine graph format and extract information
        if "functions" in graph_data and "modules" in graph_data:
            # Traditional format
            function_count = len(graph_data.get("functions", {}))
            module_count = len(graph_data.get("modules", {}))
            functions = list(graph_data.get("functions", {}).keys())[:20]  # Top 20 function names
            modules = list(graph_data.get("modules", {}).keys())[:20]  # Top 20 module names
        else:
            # Flat format (function names as keys)
            function_count = len(graph_data)
            module_count = 0
            functions = list(graph_data.keys())[:20]  # Top 20 function names
            modules = []
            
            # Count call relationships
            call_count = 0
            for _, func_data in graph_data.items():
                call_count += len(func_data.get("callees", []))
        
        # Return a simplified version to avoid overwhelming the API response
        return {
            "project_id": project_id,
            "function_count": function_count,
            "module_count": module_count,
            "functions": functions,
            "modules": modules,
            "call_relationships": call_count if 'call_count' in locals() else 0
        }
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error retrieving graph for project {project_id}: {e}")
        raise HTTPException(status_code=500, detail=f"Failed to retrieve graph: {str(e)}")

@router.get("/nuanced/status", response_model=NuancedStatusResponse)
async def check_nuanced_status():
    """
    Check if Nuanced is installed and the status of its integration.
    
    Returns:
        NuancedStatusResponse: Details about the Nuanced integration status
    """
    try:
        response = NuancedStatusResponse(
            is_installed=False,
            integration_status="unavailable",
            service_integrated=nuanced_available,
            retriever_integrated=False,
            repositories_with_graphs=0
        )
        
        # Initialize recommendations
        recommendations = []
        
        # Check if NuancedService is available
        if nuanced_available:
            response.service_integrated = True
            
            # Check if Nuanced is installed
            is_installed = NuancedService.is_installed()
            response.is_installed = is_installed
            
            if is_installed:
                # Get detailed status
                if hasattr(NuancedService, "verify_integration"):
                    details = NuancedService.verify_integration()
                    response.installation_details = details
                    
                # Check for the retriever class
                try:
                    from retriever import NuancedEnhancedRetriever
                    response.retriever_integrated = True
                except ImportError:
                    response.retriever_integrated = False
                    recommendations.append("The NuancedEnhancedRetriever could not be imported. Check the import paths.")
                
                # Check for repositories with Nuanced graphs
                nuanced_repos = []
                try:
                    # Look in temp directory for repositories with .nuanced directories
                    temp_dirs = [d for d in os.listdir("/tmp") if os.path.isdir(f"/tmp/{d}")]
                    for d in temp_dirs:
                        nuanced_dir = f"/tmp/{d}/.nuanced"
                        if os.path.exists(nuanced_dir):
                            graph_file = f"{nuanced_dir}/nuanced-graph.json"
                            nuanced_repos.append({
                                "repo_dir": f"/tmp/{d}",
                                "graph_exists": os.path.exists(graph_file),
                                "graph_size": os.path.getsize(graph_file) if os.path.exists(graph_file) else 0
                            })
                except Exception as e:
                    logger.warning(f"Error checking for Nuanced repos: {e}")
                
                response.nuanced_repos = nuanced_repos
                response.repositories_with_graphs = len(nuanced_repos)
                
                # Set overall status
                if response.retriever_integrated and response.repositories_with_graphs > 0:
                    response.integration_status = "fully_integrated"
                else:
                    response.integration_status = "partially_integrated"
                    if not response.retriever_integrated:
                        recommendations.append("The NuancedEnhancedRetriever is not properly integrated.")
                    if response.repositories_with_graphs == 0:
                        recommendations.append("No repositories with Nuanced graphs found. Try indexing a repository.")
            else:
                response.integration_status = "not_installed"
                recommendations.append("Nuanced is not installed. Install it with: pip install nuanced")
        else:
            response.integration_status = "service_missing"
            recommendations.append("The NuancedService module is not available. Check that the services directory exists.")
        
        # Add recommendations to response
        response.recommendations = recommendations
        
        return response
    except Exception as e:
        logger.error(f"Error checking Nuanced status: {e}")
        raise HTTPException(status_code=500, detail=f"Error checking Nuanced status: {str(e)}")

@router.post("/nuanced/test-indexing")
async def test_nuanced_indexing(repo_url: str = "https://github.com/python/peps", branch: str = "main"):
    """
    Test Nuanced integration by indexing a small repository.
    
    Args:
        repo_url: Repository URL to index
        branch: Branch to index
        
    Returns:
        Dict with test results
    """
    try:
        # Import the necessary functions
        from index import index_repository
        import time
        import os
        
        # Get the absolute path to sample-exclude.txt
        current_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))  # Get backend dir
        exclude_file = os.path.join(current_dir, "sample-exclude.txt")
        
        # Create a progress tracking function
        progress_data = []
        
        async def progress_callback(stage, message, progress, details=None):
            progress_data.append({
                "timestamp": time.time(),
                "stage": stage,
                "message": message,
                "progress": progress,
                "details": details
            })
        
        # Create a temporary directory
        temp_dir = f"/tmp/nuanced_test_{int(time.time())}"
        os.makedirs(temp_dir, exist_ok=True)
        
        logger.info(f"Starting test indexing of {repo_url}")
        logger.info(f"Using exclusion file: {exclude_file}")
        
        # Index the repository with Nuanced enabled
        result = await index_repository(
            repo_url=repo_url,
            commit_hash=branch,
            local_dir=temp_dir,
            max_tokens=800,
            overlap=100,
            user_id="test_user",
            project_id=f"nuanced_test_{int(time.time())}",
            progress_callback=progress_callback,
            use_nuanced=True,
            exclusion_file=exclude_file  # Add the exclusion file path
        )
        
        # Check for Nuanced graph
        nuanced_dir = os.path.join(temp_dir, ".nuanced")
        graph_file = os.path.join(nuanced_dir, "nuanced-graph.json")
        
        return {
            "success": os.path.exists(graph_file),
            "repo_url": repo_url,
            "branch": branch,
            "temp_dir": temp_dir,
            "nuanced_dir_exists": os.path.exists(nuanced_dir),
            "graph_file_exists": os.path.exists(graph_file),
            "graph_file_size": os.path.getsize(graph_file) if os.path.exists(graph_file) else 0,
            "indexing_result": result,
            "progress_log": progress_data
        }
    except Exception as e:
        logger.error(f"Error in test indexing: {e}")
        raise HTTPException(status_code=500, detail=f"Error in test indexing: {str(e)}")

@router.post("/debug-project", response_model=GraphGenerationResult)
async def debug_project_graph(project_id: str, repo_url: str = None):
    """
    Debug endpoint to help diagnose issues with Nuanced graph generation for real projects.
    This endpoint will create a temporary clone of a repository and generate a graph for it.
    
    Args:
        project_id: The project ID to associate with the graph
        repo_url: Optional repository URL to clone. If not provided, will try to find the project in MongoDB
    """
    try:
        import time
        import subprocess
        import tempfile
        from datetime import datetime
        
        logger.info(f"==== NUANCED PROJECT DEBUG ====")
        logger.info(f"Project ID: {project_id}")
        
        # If no repo_url provided, try to find it from MongoDB
        if not repo_url:
            try:
                from db import db
                project = db.projects.find_one({"id": project_id})
                if project:
                    repo_url = project.get("repoUrl")
                    logger.info(f"Found project in MongoDB with URL: {repo_url}")
                else:
                    logger.warning(f"No project found in MongoDB with ID: {project_id}")
            except Exception as e:
                logger.error(f"Error finding project in MongoDB: {e}")
                
        if not repo_url:
            return GraphGenerationResult(
                success=False,
                error="No repository URL provided and couldn't find project in MongoDB"
            )
            
        # Create temporary directory
        temp_dir = tempfile.mkdtemp(prefix=f"nuanced_debug_{project_id}_")
        logger.info(f"Created temporary directory: {temp_dir}")
        
        # Clone repository
        try:
            logger.info(f"Cloning repository: {repo_url}")
            result = subprocess.run(
                ["git", "clone", "--depth", "1", repo_url, temp_dir],
                capture_output=True,
                text=True
            )
            
            if result.returncode != 0:
                logger.error(f"Failed to clone repository: {result.stderr}")
                return GraphGenerationResult(
                    success=False,
                    error=f"Failed to clone repository: {result.stderr}"
                )
                
            logger.info(f"Successfully cloned repository to {temp_dir}")
            
            # Count Python files in repository
            python_files = []
            for root, _, files in os.walk(temp_dir):
                if '.git' in root:
                    continue
                for file in files:
                    if file.endswith('.py'):
                        python_files.append(os.path.join(root, file))
            
            logger.info(f"Found {len(python_files)} Python files in repository")
            
            # Initialize Nuanced graph
            logger.info(f"Initializing Nuanced graph...")
            graph_path = NuancedService.init_graph(temp_dir)
            
            if not graph_path:
                logger.error(f"Failed to generate Nuanced graph")
                return GraphGenerationResult(
                    success=False,
                    error="Failed to generate graph"
                )
            
            # Get graph statistics
            function_count = 0
            module_count = 0
            call_count = 0
            graph_format = "unknown"
            
            try:
                with open(graph_path, 'r') as f:
                    graph_data = json.load(f)
                
                # Determine format
                if "functions" in graph_data and "modules" in graph_data:
                    # Traditional format
                    function_count = len(graph_data.get("functions", {}))
                    module_count = len(graph_data.get("modules", {}))
                    graph_format = "traditional"
                    
                    # Count relationships
                    for _, func_data in graph_data.get("functions", {}).items():
                        call_count += len(func_data.get("callees", []))
                else:
                    # Flat format
                    function_count = len(graph_data)
                    graph_format = "flat"
                    
                    # Count relationships
                    for _, func_data in graph_data.items():
                        call_count += len(func_data.get("callees", []))
                
                # Print first few entries to debug
                logger.info(f"Graph format: {graph_format}")
                logger.info(f"Functions: {function_count}")
                logger.info(f"Modules: {module_count}")
                logger.info(f"Call relationships: {call_count}")
                
                if graph_format == "flat":
                    sample_keys = list(graph_data.keys())[:3]
                    for key in sample_keys:
                        logger.info(f"Sample function: {key}")
                        logger.info(f"  - Filepath: {graph_data[key].get('filepath', 'unknown')}")
                        logger.info(f"  - Callees: {graph_data[key].get('callees', [])[:5]}")
                else:
                    sample_keys = list(graph_data.get("functions", {}).keys())[:3]
                    for key in sample_keys:
                        func_data = graph_data["functions"][key]
                        logger.info(f"Sample function: {func_data.get('name', key)}")
                        logger.info(f"  - Filepath: {func_data.get('filepath', 'unknown')}")
                        logger.info(f"  - Callees: {func_data.get('callees', [])[:5]}")
                
                # Store in database
                stored = False
                if function_count > 0 or module_count > 0:
                    stored = NuancedService.store_graph_in_db(project_id, graph_path)
                    logger.info(f"Graph stored in database: {stored}")
                    
                    # Generate compact representation
                    compact_graph = NuancedService.extract_compact_graph(graph_path)
                    if compact_graph:
                        compact_function_count = len(compact_graph.get("functions", {}))
                        logger.info(f"Generated compact graph with {compact_function_count} function relationships")
                
                return GraphGenerationResult(
                    success=True,
                    graph_path=graph_path,
                    function_count=function_count,
                    module_count=module_count,
                    call_relationships=call_count,
                    stored_in_db=stored,
                    format=graph_format
                )
            except Exception as e:
                logger.error(f"Error analyzing graph: {e}")
                return GraphGenerationResult(
                    success=False,
                    error=f"Error analyzing graph: {e}"
                )
        finally:
            # Clean up temporary directory (optional, comment out to keep it for further debugging)
            # import shutil
            # shutil.rmtree(temp_dir, ignore_errors=True)
            pass
            
    except Exception as e:
        logger.error(f"Error in debug_project_graph: {e}")
        import traceback
        logger.error(f"Traceback: {traceback.format_exc()}")
        return GraphGenerationResult(
            success=False,
            error=str(e)
        ) 

@router.get("/relationships/{project_id}")
async def get_call_relationships(project_id: str):
    """
    Get a summary of call relationships for a project.
    This endpoint returns detailed statistics about function call relationships from the Nuanced graph.
    """
    try:
        # Import here to avoid circular imports
        from services.nuanced_service import NuancedService
        
        # Try to get graph from DB
        graph_data = NuancedService.get_graph_from_db(project_id)
        
        if not graph_data:
            raise HTTPException(status_code=404, detail="No graph found for this project")
            
        # Prepare response data
        response = {
            "project_id": project_id,
            "success": True,
            "error": None,
            "stats": {}
        }
        
        # Check for expected keys based on format
        if "functions" in graph_data and "modules" in graph_data:
            # Traditional format
            format = "traditional"
            function_count = len(graph_data.get("functions", {}))
            module_count = len(graph_data.get("modules", {}))
            
            # Count call relationships
            call_relationships = 0
            functions_with_calls = 0
            for func_id, func_data in graph_data.get("functions", {}).items():
                callee_count = len(func_data.get("callees", []))
                if callee_count > 0:
                    functions_with_calls += 1
                    call_relationships += callee_count
            
            # Add to response
            response["stats"] = {
                "format": format,
                "function_count": function_count,
                "module_count": module_count,
                "call_relationships": call_relationships,
                "functions_with_calls": functions_with_calls,
                "functions": []
            }
            
            # Add some example functions with their call relationships
            sample_size = min(10, function_count)
            for func_id, func_data in list(graph_data.get("functions", {}).items())[:sample_size]:
                callees = []
                for callee_id in func_data.get("callees", []):
                    if callee_id in graph_data.get("functions", {}):
                        callee_data = graph_data["functions"][callee_id]
                        callees.append(callee_data.get("name", "unknown"))
                
                if callees:
                    response["stats"]["functions"].append({
                        "name": func_data.get("name", "unknown"),
                        "calls": callees
                    })
        else:
            # Flat format
            format = "flat"
            function_count = len(graph_data)
            
            # Count call relationships
            call_relationships = 0
            functions_with_calls = 0
            for func_name, func_data in graph_data.items():
                callee_count = len(func_data.get("callees", []))
                if callee_count > 0:
                    functions_with_calls += 1
                    call_relationships += callee_count
            
            # Add to response
            response["stats"] = {
                "format": format,
                "function_count": function_count,
                "module_count": 0,
                "call_relationships": call_relationships,
                "functions_with_calls": functions_with_calls,
                "functions": []
            }
            
            # Add some example functions with their call relationships
            sample_size = min(10, function_count)
            for func_name, func_data in list(graph_data.items())[:sample_size]:
                if func_data.get("callees", []):
                    # Extract simple names for readability
                    simple_callees = []
                    for callee in func_data.get("callees", []):
                        if "." in callee:
                            simple_callees.append(callee.split(".")[-1])
                        else:
                            simple_callees.append(callee)
                    
                    # Extract simple function name
                    simple_name = func_name
                    if "." in func_name:
                        simple_name = func_name.split(".")[-1]
                        
                    response["stats"]["functions"].append({
                        "name": simple_name,
                        "full_name": func_name,
                        "calls": simple_callees
                    })
        
        return response
    except HTTPException:
        raise
    except Exception as e:
        logging.error(f"Error getting call relationships: {str(e)}")
        return {
            "project_id": project_id,
            "success": False,
            "error": str(e),
            "stats": {}
        } 

@router.post("/regenerate/{project_id}", response_model=GraphGenerationResult)
async def regenerate_nuanced_graph(project_id: str = Path(..., description="Project ID to regenerate the graph for")):
    """
    Regenerate a Nuanced graph for a project using code stored in Pinecone.
    
    This endpoint is useful when:
    1. The temporary repository used during indexing has been cleaned up
    2. The Nuanced graph was not generated during indexing
    3. You need to update the graph after Nuanced was updated
    
    Note: This requires code to be available in Pinecone vectorstore.
    """
    try:
        logger.info(f"==== 🔍 NUANCED GRAPH REGENERATION REQUESTED ====")
        logger.info(f"Project ID: {project_id}")
        
        # Check if Nuanced is installed
        from services.nuanced_service import NuancedService
        if not NuancedService.is_installed():
            logger.warning("❌ NUANCED NOT INSTALLED: Cannot regenerate graph")
            return GraphGenerationResult(
                success=False,
                error="Nuanced is not installed. Please install it first with 'pip install nuanced'."
            )
            
        # Check if we already have a graph in MongoDB
        existing_graph = NuancedService.get_graph_from_db(project_id)
        if existing_graph:
            logger.info(f"Graph already exists in database with {len(existing_graph)} functions")
            function_count = 0
            if "functions" in existing_graph:
                function_count = len(existing_graph.get("functions", {}))
                module_count = len(existing_graph.get("modules", {}))
                format_type = "traditional"
            else:
                function_count = len(existing_graph)
                module_count = 0
                format_type = "flat"
                
            return GraphGenerationResult(
                success=True,
                function_count=function_count,
                module_count=module_count,
                stored_in_db=True,
                call_relationships=function_count * 2,  # Estimate
            )
        
        # Create a temporary directory for code extraction
        temp_dir = f"/tmp/nuanced_regen_{project_id}"
        os.makedirs(temp_dir, exist_ok=True)
        
        logger.info(f"Created temporary directory: {temp_dir}")
        
        # Get the code from Pinecone
        from langchain.vectorstores import Pinecone
        from langchain.embeddings import OpenAIEmbeddings
        import pinecone
        from db import get_settings, get_user_namespace
        
        settings = get_settings()
        pc = pinecone.Pinecone(api_key=settings.pinecone_api_key)
        
        # Get the user namespace
        # This endpoint is project-specific, so we'll need to query the database to get the user ID
        from db import db
        project = db.projects.find_one({"id": project_id})
        if not project:
            logger.warning(f"❌ PROJECT NOT FOUND: {project_id}")
            return GraphGenerationResult(
                success=False,
                error=f"Project {project_id} not found in database"
            )
            
        user_id = project.get("user_id")
        if not user_id:
            logger.warning("❌ USER ID NOT FOUND IN PROJECT")
            return GraphGenerationResult(
                success=False,
                error="User ID not found in project data"
            )
            
        logger.info(f"User ID: {user_id}")
        
        # Create the namespace
        namespace = f"{user_id}/{project_id}"
        logger.info(f"Using namespace: {namespace}")
        
        # Initialize the vectorstore
        embeddings = OpenAIEmbeddings()
        try:
            vectorstore = Pinecone(
                pc.Index("nia-app"),
                embeddings,
                namespace=namespace
            )
        except Exception as e:
            logger.error(f"❌ PINECONE CONNECTION ERROR: {str(e)}")
            return GraphGenerationResult(
                success=False,
                error=f"Failed to connect to Pinecone: {str(e)}"
            )
            
        # Get documents from vectorstore
        try:
            # Use a simple query to get all documents
            docs = vectorstore.similarity_search(
                "code python file",
                k=500  # Limit to 500 docs to avoid overwhelming the server
            )
            
            logger.info(f"Retrieved {len(docs)} documents from Pinecone")
            
            if not docs:
                logger.warning("❌ NO DOCUMENTS FOUND IN PINECONE")
                return GraphGenerationResult(
                    success=False,
                    error="No documents found in Pinecone for this project"
                )
                
            # Extract Python files
            python_files = {}
            file_count = 0
            for doc in docs:
                metadata = doc.metadata
                if "file_path" in metadata:
                    file_path = metadata["file_path"]
                    if file_path.endswith(".py"):
                        # Create directory structure
                        rel_path = file_path
                        if rel_path.startswith("/"):
                            rel_path = rel_path[1:]
                            
                        full_path = os.path.join(temp_dir, rel_path)
                        os.makedirs(os.path.dirname(full_path), exist_ok=True)
                        
                        # Store content if we haven't seen this file before
                        if file_path not in python_files:
                            python_files[file_path] = doc.page_content
                            file_count += 1
                            
            logger.info(f"Found {file_count} unique Python files")
            
            if file_count == 0:
                logger.warning("❌ NO PYTHON FILES FOUND")
                return GraphGenerationResult(
                    success=False,
                    error="No Python files found in the documents"
                )
                
            # Write files to disk
            for file_path, content in python_files.items():
                if file_path.startswith("/"):
                    file_path = file_path[1:]
                    
                full_path = os.path.join(temp_dir, file_path)
                os.makedirs(os.path.dirname(full_path), exist_ok=True)
                
                with open(full_path, "w") as f:
                    f.write(content)
                    
            logger.info(f"Wrote {file_count} Python files to {temp_dir}")
            
            # Initialize Nuanced graph
            nuanced_graph_path = NuancedService.init_graph(temp_dir)
            
            if not nuanced_graph_path or not os.path.exists(nuanced_graph_path):
                logger.warning(f"❌ FAILED TO GENERATE GRAPH")
                return GraphGenerationResult(
                    success=False,
                    error="Failed to generate Nuanced graph"
                )
                
            # Store in database
            if not NuancedService.store_graph_in_db(project_id, nuanced_graph_path):
                logger.warning(f"❌ FAILED TO STORE GRAPH IN DATABASE")
                return GraphGenerationResult(
                    success=True,
                    graph_path=nuanced_graph_path,
                    stored_in_db=False,
                    error="Graph generated but storage in database failed"
                )
                
            # Get graph statistics
            with open(nuanced_graph_path, "r") as f:
                graph_data = json.load(f)
                
            if "functions" in graph_data and "modules" in graph_data:
                # Traditional format
                function_count = len(graph_data.get("functions", {}))
                module_count = len(graph_data.get("modules", {}))
                format_type = "traditional"
                call_relationships = 0
            else:
                # Flat format
                function_count = len(graph_data)
                module_count = 0
                format_type = "flat"
                
                # Count call relationships
                call_relationships = 0
                for _, func_data in graph_data.items():
                    call_relationships += len(func_data.get("callees", []))
            
            logger.info(f"✅ GRAPH REGENERATION COMPLETE")
            logger.info(f"- Format: {format_type}")
            logger.info(f"- Functions: {function_count}")
            logger.info(f"- Modules: {module_count}")
            logger.info(f"- Call relationships: {call_relationships}")
            
            return GraphGenerationResult(
                success=True,
                graph_path=nuanced_graph_path,
                function_count=function_count,
                module_count=module_count,
                call_relationships=call_relationships,
                stored_in_db=True
            )
            
        except Exception as e:
            logger.error(f"❌ ERROR RETRIEVING DOCUMENTS: {str(e)}")
            import traceback
            logger.error(f"Traceback: {traceback.format_exc()}")
            return GraphGenerationResult(
                success=False,
                error=f"Error retrieving documents: {str(e)}"
            )
            
    except Exception as e:
        logger.error(f"❌ ERROR REGENERATING GRAPH: {str(e)}")
        import traceback
        logger.error(f"Traceback: {traceback.format_exc()}")
        return GraphGenerationResult(
            success=False,
            error=f"Error regenerating graph: {str(e)}"
        ) 

@router.post("/regenerate-graph/{project_id}")
async def regenerate_graph_for_project(
    project_id: str = Path(..., description="Project ID to regenerate the graph for"),
    user_id: str = Query(..., description="User ID making the request"),
    force: bool = Query(False, description="Force regeneration even if graph exists")
):
    """
    Regenerate the graph data for a project from its repository or vectorstore.
    This endpoint can be used to fix issues with missing GraphRAG data.
    """
    try:
        # Check project access
        from routes.projects import get_project
        project = get_project(project_id, user_id)
        
        if not project:
            raise HTTPException(status_code=404, detail=f"Project {project_id} not found or not accessible by this user")
            
        # Check if graph already exists and force flag is not set
        existing_graph = NuancedService.get_graph_from_db(project_id)
        if existing_graph and not force:
            # Return existing graph info without regenerating
            return {
                "project_id": project_id,
                "status": "exists",
                "message": "Graph already exists. Use force=true to regenerate.",
                "function_count": len(existing_graph.get("functions", {})) if "functions" in existing_graph else len(existing_graph)
            }
            
        # Try to find local repo path
        repo_path = ""
        potential_paths = [
            f"/tmp/my_local_repo_{project_id}",
            f"/tmp/nia_repo_{project_id}",
            f"/tmp/graph_rag_repo_{project_id}"
        ]
        
        # Check also in project metadata
        from db import MongoDB
        db = MongoDB()
        proj_metadata = db.db.projects.find_one({"project_id": project_id})
        if proj_metadata and "graphrag_repo_path" in proj_metadata:
            potential_paths.insert(0, proj_metadata["graphrag_repo_path"])
            
        # Find first existing path
        for path in potential_paths:
            if os.path.exists(path):
                repo_path = path
                break
                
        # First try to generate from local repo if it exists
        if repo_path:
            logger.info(f"Regenerating graph from local repo at {repo_path}")
            graph_data = NuancedService.generate_graph(repo_path)
            
            if graph_data:
                # Store in database
                NuancedService.store_graph_in_db(project_id, graph_data)
                return {
                    "project_id": project_id,
                    "status": "success",
                    "method": "local_repo",
                    "repo_path": repo_path,
                    "function_count": len(graph_data.get("functions", {})) if "functions" in graph_data else len(graph_data)
                }
        
        # If local repo doesn't exist or graph generation failed, try vectorstore
        logger.info(f"Local repo not found or generation failed, trying vectorstore regeneration")
        graph_data = NuancedService.regenerate_graph_from_vectorstore(project_id)
        
        if graph_data:
            # Store in database
            NuancedService.store_graph_in_db(project_id, graph_data)
            return {
                "project_id": project_id,
                "status": "success",
                "method": "vectorstore",
                "function_count": len(graph_data.get("functions", {})) if "functions" in graph_data else len(graph_data)
            }
            
        # If all methods failed
        raise HTTPException(
            status_code=500, 
            detail="Failed to regenerate graph from any source. Try re-indexing the repository."
        )
            
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error regenerating graph for project {project_id}: {e}")
        import traceback
        logger.error(f"Traceback: {traceback.format_exc()}")
        raise HTTPException(status_code=500, detail=f"Failed to regenerate graph: {str(e)}") 