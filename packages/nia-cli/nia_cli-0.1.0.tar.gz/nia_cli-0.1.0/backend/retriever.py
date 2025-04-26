import logging
import os
import re
import json
import time
import datetime
import asyncio
from typing import Dict, List, Optional, Any, Tuple, Callable, Union, Set
from pathlib import Path
from types import SimpleNamespace
from langchain.retrievers import EnsembleRetriever
import anthropic
import Levenshtein
import networkx as nx
from anytree import Node, RenderTree
from langchain.callbacks.manager import CallbackManagerForRetrieverRun
from langchain.retrievers import ContextualCompressionRetriever
from langchain.retrievers.multi_query import MultiQueryRetriever
from langchain.schema import BaseRetriever, Document
from langchain_google_genai import GoogleGenerativeAIEmbeddings
from langchain_openai import OpenAIEmbeddings
from langchain_voyageai import VoyageAIEmbeddings
from pydantic import Field

from code_symbols import get_code_symbols
from data_manager import DataManager, GitHubRepoManager
from db import MongoDB
from llm import build_llm_via_langchain
from reranker import build_reranker
from vector_store import build_vector_store_from_args

# Try to import the NuancedService if available
try:
    from services.nuanced_service import NuancedService
except ImportError:
    NuancedService = None

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger()
logger.setLevel(logging.INFO)

CLAUDE_MODEL = "claude-3-7-sonnet-20250219"
CLAUDE_MODEL_CONTEXT_SIZE = 200_000


class LLMRetriever(BaseRetriever):
    """Custom Langchain retriever based on an LLM.

    Builds a representation of the folder structure of the repo, feeds it to an LLM, and asks the LLM for the most
    relevant files for a particular user query, expecting it to make decisions based solely on file names.

    Only works with Claude/Anthropic, because it's very slow (e.g. 15s for a mid-sized codebase) and we need prompt
    caching to make it usable.
    """

    repo_manager: GitHubRepoManager = Field(...)
    top_k: int = Field(...)

    cached_repo_metadata: List[Dict] = Field(...)
    cached_repo_files: List[str] = Field(...)
    cached_repo_hierarchy: str = Field(...)

    def __init__(self, repo_manager: GitHubRepoManager, top_k: int):
        super().__init__()
        self.repo_manager = repo_manager
        self.top_k = top_k

        # We cached these fields manually because:
        # 1. Pydantic doesn't work with functools's @cached_property.
        # 2. We can't use Pydantic's @computed_field because these fields depend on each other.
        # 3. We can't use functools's @lru_cache because LLMRetriever needs to be hashable.
        self.cached_repo_metadata = None
        self.cached_repo_files = None
        self.cached_repo_hierarchy = None

        if not os.environ.get("ANTHROPIC_API_KEY"):
            raise ValueError("Please set the ANTHROPIC_API_KEY environment variable for the LLMRetriever.")

    @property
    def repo_metadata(self):
        if not self.cached_repo_metadata:
            self.cached_repo_metadata = [metadata for metadata in self.repo_manager.walk(get_content=False)]

            # Extracting code symbols takes quite a while, since we need to read each file from disk.
            # As a compromise, we do it for small codebases only.
            small_codebase = len(self.repo_files) <= 200
            if small_codebase:
                for metadata in self.cached_repo_metadata:
                    file_path = metadata["file_path"]
                    content = self.repo_manager.read_file(file_path)
                    metadata["code_symbols"] = get_code_symbols(file_path, content)

        return self.cached_repo_metadata

    @property
    def repo_files(self):
        if not self.cached_repo_files:
            self.cached_repo_files = set(metadata["file_path"] for metadata in self.repo_metadata)
        return self.cached_repo_files

    @property
    def repo_hierarchy(self):
        """Produces a string that describes the structure of the repository. Depending on how big the codebase is, it
        might include class and method names."""
        if self.cached_repo_hierarchy is None:
            render = LLMRetriever._render_file_hierarchy(self.repo_metadata, include_classes=True, include_methods=True)
            max_tokens = CLAUDE_MODEL_CONTEXT_SIZE - 50_000  # 50,000 tokens for other parts of the prompt.
            client = anthropic.Anthropic()

            def count_tokens(x):
                count = client.beta.messages.count_tokens(model=CLAUDE_MODEL, messages=[{"role": "user", "content": x}])
                return count.input_tokens

            if count_tokens(render) > max_tokens:
                logging.info("File hierarchy is too large; excluding methods.")
                render = LLMRetriever._render_file_hierarchy(
                    self.repo_metadata, include_classes=True, include_methods=False
                )
                if count_tokens(render) > max_tokens:
                    logging.info("File hierarchy is still too large; excluding classes.")
                    render = LLMRetriever._render_file_hierarchy(
                        self.repo_metadata, include_classes=False, include_methods=False
                    )
                    if count_tokens(render) > max_tokens:
                        logging.info("File hierarchy is still too large; truncating.")
                        tokenizer = anthropic.Tokenizer()
                        tokens = tokenizer.tokenize(render)[:max_tokens]
                        render = tokenizer.detokenize(tokens)
            self.cached_repo_hierarchy = render
        return self.cached_repo_hierarchy

    def _get_relevant_documents(self, query: str, *, run_manager: CallbackManagerForRetrieverRun = None) -> List[Document]:
        """Retrieve relevant documents for a given query."""
        filenames = self._ask_llm_to_retrieve(user_query=query, top_k=self.top_k)
        documents = []
        for filename in filenames:
            document = Document(
                page_content=self.repo_manager.read_file(filename),
                metadata={"file_path": filename, "url": self.repo_manager.url_for_file(filename)},
            )
            documents.append(document)
        return documents

    def _ask_llm_to_retrieve(self, user_query: str, top_k: int) -> List[str]:
        """Feeds the file hierarchy and user query to the LLM and asks which files might be relevant."""
        repo_hierarchy = str(self.repo_hierarchy)
        sys_prompt = f"""
You are a retriever system. You will be given a user query and a list of files in a GitHub repository, together with the class names in each file.

For instance:
folder1
    folder2
        folder3
            file123.py
                ClassName1
                ClassName2
                ClassName3
means that there is a file with path folder1/folder2/folder3/file123.py, which contains classes ClassName1, ClassName2, and ClassName3.

Your task is to determine the top {top_k} files that are most relevant to the user query.
DO NOT RESPOND TO THE USER QUERY DIRECTLY. Instead, respond with full paths to relevant files that could contain the answer to the query. Say absolutely nothing else other than the file paths.

Here is the file hierarchy of the GitHub repository, together with the class names in each file:

{repo_hierarchy}
"""

        # We are deliberately repeating the "DO NOT RESPOND TO THE USER QUERY DIRECTLY" instruction here.
        augmented_user_query = f"""
User query: {user_query}

DO NOT RESPOND TO THE USER QUERY DIRECTLY. Instead, respond with full paths to relevant files that could contain the answer to the query. Say absolutely nothing else other than the file paths.
"""
        response = LLMRetriever._call_via_anthropic_with_prompt_caching(sys_prompt, augmented_user_query)

        files_from_llm = response.content[0].text.strip().split("\n")
        validated_files = []

        for filename in files_from_llm:
            if filename not in self.repo_files:
                if "/" not in filename:
                    # This is most likely some natural language excuse from the LLM; skip it.
                    continue
                # Try a few heuristics to fix the filename.
                filename = LLMRetriever._fix_filename(filename, self.repo_manager.repo_id)
                if filename not in self.repo_files:
                    # The heuristics failed; try to find the closest filename in the repo.
                    filename = LLMRetriever._find_closest_filename(filename, self.repo_files)
            if filename in self.repo_files:
                validated_files.append(filename)
        return validated_files

    @staticmethod
    def _call_via_anthropic_with_prompt_caching(system_prompt: str, user_prompt: str) -> str:
        """Calls the Anthropic API with prompt caching for the system prompt.

        See https://docs.anthropic.com/en/docs/build-with-claude/prompt-caching.

        We're circumventing LangChain for now, because the feature is < 1 week old at the time of writing and has no
        documentation: https://github.com/langchain-ai/langchain/pull/27087
        """
        system_message = {"type": "text", "text": system_prompt, "cache_control": {"type": "ephemeral"}}
        user_message = {"role": "user", "content": user_prompt}

        response = anthropic.Anthropic().beta.prompt_caching.messages.create(
            model=CLAUDE_MODEL,
            max_tokens=4096,  # The maximum number of *output* tokens to generate.
            system=[system_message],
            messages=[user_message],
        )
        # Caching information will be under `cache_creation_input_tokens` and `cache_read_input_tokens`.
        # Note that, for prompts shorter than 1024 tokens, Anthropic will not do any caching.
        logging.info("Anthropic prompt caching info: %s", response.usage)
        return response

    @staticmethod
    def _render_file_hierarchy(
        repo_metadata: List[Dict], include_classes: bool = True, include_methods: bool = True
    ) -> str:
        """Given a list of files, produces a visualization of the file hierarchy. This hierarchy optionally includes
        class and method names, if available.

        For large codebases, including both classes and methods might exceed the token limit of the LLM. In that case,
        try setting `include_methods=False` first. If that's still too long, try also setting `include_classes=False`.

        As a point of reference, the Transformers library requires setting `include_methods=False` to fit within
        Claude's 200k context.

        Example:
        folder1
            folder11
                file111.md
                file112.py
                    ClassName1
                        method_name1
                        method_name2
                        method_name3
            folder12
                file121.py
                    ClassName2
                    ClassName3
        folder2
            file21.py
        """
        # The "nodepath" is the path from root to the node (e.g. huggingface/transformers/examples)
        nodepath_to_node = {}

        for metadata in repo_metadata:
            path = metadata["file_path"]
            paths = [path]

            if include_classes or include_methods:
                # Add the code symbols to the path. For instance, "folder/myfile.py/ClassName/method_name".
                for class_name, method_name in metadata.get("code_symbols", []):
                    if include_classes and class_name:
                        paths.append(path + "/" + class_name)
                    # We exclude private methods to save tokens.
                    if include_methods and method_name and not method_name.startswith("_"):
                        paths.append(
                            path + "/" + class_name + "/" + method_name if class_name else path + "/" + method_name
                        )

            for path in paths:
                items = path.split("/")
                nodepath = ""
                parent_node = None
                for item in items:
                    nodepath = f"{nodepath}/{item}"
                    if nodepath in nodepath_to_node:
                        node = nodepath_to_node[nodepath]
                    else:
                        node = Node(item, parent=parent_node)
                        nodepath_to_node[nodepath] = node
                    parent_node = node

        root_path = "/" + repo_metadata[0]["file_path"].split("/")[0]
        full_render = ""
        root_node = nodepath_to_node[root_path]
        for pre, fill, node in RenderTree(root_node):
            render = "%s%s\n" % (pre, node.name)
            # Replace special lines with empty strings to save on tokens.
            render = render.replace("└", " ").replace("├", " ").replace("│", " ").replace("─", " ")
            full_render += render
        return full_render

    @staticmethod
    def _fix_filename(filename: str, repo_id: str) -> str:
        """Attempts to "fix" a filename output by the LLM.

        Common issues with LLM-generated filenames:
        - The LLM prepends an extraneous "/".
        - The LLM omits the name of the org (e.g. "transformers/README.md" instead of "huggingface/transformers/README.md").
        - The LLM omits the name of the repo (e.g. "huggingface/README.md" instead of "huggingface/transformers/README.md").
        - The LLM omits the org/repo prefix (e.g. "README.md" instead of "huggingface/transformers/README.md").
        """
        if filename.startswith("/"):
            filename = filename[1:]
        org_name, repo_name = repo_id.split("/")
        items = filename.split("/")
        if filename.startswith(org_name) and not filename.startswith(repo_id):
            new_items = [org_name, repo_name] + items[1:]
            return "/".join(new_items)
        if not filename.startswith(org_name) and filename.startswith(repo_name):
            return f"{org_name}/{filename}"
        if not filename.startswith(org_name) and not filename.startswith(repo_name):
            return f"{org_name}/{repo_name}/{filename}"
        return filename

    @staticmethod
    def _find_closest_filename(filename: str, repo_filenames: List[str], max_edit_distance: int = 10) -> Optional[str]:
        """Returns the path in the repo with smallest edit distance from `filename`. Helpful when the `filename` was
        generated by an LLM and parts of it might have been hallucinated. Returns None if the closest path is more than
        `max_edit_distance` away. In case of a tie, returns an arbitrary closest path.
        """
        distances = [(path, Levenshtein.distance(filename, path)) for path in repo_filenames]
        distances.sort(key=lambda x: x[1])
        if distances[0][1] <= max_edit_distance:
            closest_path = distances[0][0]
            return closest_path
        return None


class RerankerWithErrorHandling(BaseRetriever):
    """Wraps a `ContextualCompressionRetriever` to catch errors during inference.

    In practice, we see occasional `requests.exceptions.ReadTimeout` from the NVIDIA reranker, which crash the entire
    pipeline. This wrapper catches such exceptions by simply returning the documents in the original order.
    """

    def __init__(self, reranker: ContextualCompressionRetriever):
        self.reranker = reranker

    def _get_relevant_documents(self, query: str, *, run_manager=None) -> List[Document]:
        try:
            return self.reranker._get_relevant_documents(query, run_manager=run_manager)
        except Exception as e:
            logging.error(f"Error in reranker; preserving original document order from retriever. {e}")
            return self.reranker.base_retriever._get_relevant_documents(query, run_manager=run_manager)


class NuancedEnhancedRetriever(BaseRetriever):
    """Augments documents from a base retriever with Nuanced call graph data.
    
    For Python code files, this retriever tries to identify functions in the retrieved documents
    and enriches them with call graph information from Nuanced. This helps provide better context
    about function relationships to the LLM.
    """
    
    base_retriever: Optional[BaseRetriever] = None
    repo_path: str = Field(default="")
    external_graph: Optional[Dict] = None
    nuanced_available: bool = Field(default=False)
    project_id: Optional[str] = Field(default=None)
    max_retries: int = Field(default=2)
    
    def __init__(self, base_retriever: Optional[BaseRetriever] = None, repo_path: str = "", external_graph: Optional[Dict] = None):
        """Initialize the Nuanced-enhanced retriever.
        
        Args:
            base_retriever: The underlying retriever to get documents from
            repo_path: Path to the repository with the Nuanced graph
            external_graph: Optional external graph data to use directly instead of loading from disk
        """
        super().__init__()
        self.base_retriever = base_retriever
        self.repo_path = repo_path
        self.external_graph = external_graph
        self.project_id = None
        self.max_retries = 2  # Number of auto-regeneration retries
        
        # Check if Nuanced is available
        self.nuanced_available = NuancedService is not None and NuancedService.is_installed()
        
        # Try to extract project ID from repository path if possible
        if self.repo_path and NuancedService is not None:
            try:
                self.project_id = NuancedService.extract_project_id_from_path(self.repo_path)
            except Exception:
                # If extraction fails, we'll extract it later
                pass
        
        # Log retriever initialization for verification
        if external_graph:
            status = "ENABLED with external graph data"
            graph_format = "flat" if isinstance(external_graph, dict) and "functions" not in external_graph else "traditional"
            function_count = len(external_graph) if graph_format == "flat" else len(external_graph.get("functions", {}))
            logger.info(f"🔍 NuancedEnhancedRetriever initialized with direct graph data: {status}")
            logger.info(f"   - Graph Format: {graph_format}")
            logger.info(f"   - Functions: {function_count}")
        else:
            status = "ENABLED" if self.nuanced_available else "DISABLED (Nuanced not available)"
            logger.info(f"🔍 NuancedEnhancedRetriever initialized: {status}")
            logger.info(f"   - Repo Path: {self.repo_path}")
            logger.info(f"   - Base Retriever: {type(self.base_retriever).__name__ if self.base_retriever else 'None'}")
        
        # Write proof to a file for verification
        try:
            with open('/tmp/nuanced_retriever_proof.txt', 'a') as f:
                f.write(f"NuancedEnhancedRetriever initialized at {time.time()}\n")
                f.write(f"Status: {status}\n")
                f.write(f"Repo Path: {self.repo_path}\n")
                f.write(f"External Graph: {'Yes' if external_graph else 'No'}\n")
                f.write(f"Base Retriever: {type(self.base_retriever).__name__ if self.base_retriever else 'None'}\n")
                f.write("-" * 50 + "\n")
        except Exception as e:
            logger.error(f"Failed to write proof file: {e}")
        
        if not self.nuanced_available and not external_graph:
            logger.warning("⚠️ Nuanced is not available. NuancedEnhancedRetriever will pass through documents without enrichment.")
    
    def _extract_function_names(self, file_path: str, content: str) -> List[str]:
        """Extract function names from Python code using a comprehensive approach.
        
        This method combines multiple techniques:
        1. Using AST for accurate static analysis when possible
        2. Using regex as a fallback for partial code or when AST fails
        3. Optional LLM-based extraction for complex cases
        4. Contextual understanding of code relationships
        
        Args:
            file_path: Path to the file (used for logging and context)
            content: Python code content as string
            
        Returns:
            List of function and method names extracted from the content
        """
        try:
            # Check if content is empty or not valid
            if not content or not isinstance(content, str):
                logger.warning(f"Empty or invalid content for file: {file_path}")
                return []
            
            # Use AST-based approach first for accurate extraction
            functions = self._extract_via_ast(content, file_path)
            
            # If AST extraction worked, that's our primary result
            if functions:
                logger.debug(f"AST extraction found {len(functions)} functions in {file_path}")
                return functions
            
            # If AST extraction failed, use regex as fallback
            functions = self._extract_via_regex(content, file_path)
            if functions:
                logger.debug(f"Regex extraction found {len(functions)} functions in {file_path}")
                return functions
            
            # As a final fallback for complex cases, try LLM-based extraction
            # Only if no functions were found so far and the file is non-trivial in size
            if not functions and len(content) > 1000:
                try:
                    llm_functions = self._extract_via_llm(content, file_path)
                    if llm_functions:
                        logger.info(f"LLM extraction found {len(llm_functions)} functions in {file_path}")
                        return llm_functions
                except Exception as llm_error:
                    logger.warning(f"LLM extraction failed for {file_path}: {str(llm_error)}")
            
            # If all else fails, return what we have
            return functions
            
        except Exception as e:
            logger.error(f"Error extracting function names from {file_path}: {str(e)}")
            import traceback
            logger.error(f"Traceback: {traceback.format_exc()}")
            return []
    
    def _extract_via_ast(self, content: str, file_path: str) -> List[str]:
        """Use Python's AST to accurately extract function and method names.
        
        This approach is more reliable than regex but may fail on partial/invalid code.
        
        Args:
            content: Code content to analyze
            file_path: Path to the file (for logging only)
            
        Returns:
            List of function names extracted via AST
        """
        import ast
        from functools import lru_cache
        
        @lru_cache(maxsize=32)
        def get_all_names(node, class_context=None):
            """Recursively extract function/method names from AST nodes."""
            names = []
            
            # Get function names
            if isinstance(node, ast.FunctionDef):
                func_name = node.name
                # Add qualified name if in a class
                if class_context:
                    names.append(f"{class_context}.{func_name}")
                names.append(func_name)
            
            # Get class names and their methods
            elif isinstance(node, ast.ClassDef):
                class_name = node.name
                names.append(class_name)
                
                # Process all methods in the class
                for item in node.body:
                    if isinstance(item, ast.FunctionDef):
                        method_name = item.name
                        # Skip magic methods to reduce noise
                        if not (method_name.startswith('__') and method_name.endswith('__')):
                            names.append(method_name)  # Add method without class prefix
                            names.append(f"{class_name}.{method_name}")  # Add qualified method name
                
            # Recursively process children
            for child in ast.iter_child_nodes(node):
                names.extend(get_all_names(
                    child, 
                    class_context=node.name if isinstance(node, ast.ClassDef) else class_context
                ))
                
            return names
        
        try:
            # Parse the code with AST
            tree = ast.parse(content)
            
            # Extract all function names
            function_names = get_all_names(tree)
            
            # Add additional analysis for function calls
            function_calls = set()
            class FunctionCallVisitor(ast.NodeVisitor):
                def visit_Call(self, node):
                    if isinstance(node.func, ast.Name):
                        function_calls.add(node.func.id)
                    elif isinstance(node.func, ast.Attribute):
                        # Handle method calls like obj.method()
                        function_calls.add(node.func.attr)  # Method name
                        # Also capture the qualified name if possible
                        if isinstance(node.func.value, ast.Name):
                            function_calls.add(f"{node.func.value.id}.{node.func.attr}")
                    self.generic_visit(node)

            visitor = FunctionCallVisitor()
            visitor.visit(tree)
            
            # Combine function definitions and calls
            all_functions = list(set(function_names) | function_calls)
            
            # Filter out common built-ins and keywords to reduce noise
            common_builtins = {'print', 'len', 'range', 'int', 'str', 'list', 'dict', 'set', 'tuple', 'open'}
            all_functions = [f for f in all_functions if f not in common_builtins]
            
            return all_functions
            
        except SyntaxError:
            # AST parsing failed, likely due to incomplete or invalid code
            logger.debug(f"AST parsing failed for {file_path}, falling back to regex")
            return []
        except Exception as e:
            logger.debug(f"AST extraction error for {file_path}: {str(e)}")
            return []
    
    def _extract_via_regex(self, content: str, file_path: str) -> List[str]:
        """Extract function names using regex patterns as a fallback method.
        
        Args:
            content: Code content to analyze
            file_path: Path to the file (for logging only)
            
        Returns:
            List of function names extracted via regex
        """
        import re
        
        functions = []
        
        # 1. Find regular function definitions (def keyword)
        function_pattern = r'def\s+([a-zA-Z_][a-zA-Z0-9_]*)\s*\('
        functions.extend(re.findall(function_pattern, content))
        
        # 2. Find class method definitions
        class_pattern = r'class\s+([a-zA-Z_][a-zA-Z0-9_]*)'
        classes = re.findall(class_pattern, content)
        
        # For each class, try to find its methods
        for class_name in classes:
            # Add the class name itself as a potential match
            functions.append(class_name)
            
            # Try to find the class block
            class_match = re.search(r'class\s+' + class_name + r'[^\n]*:(.*?)(?:(?:class)|$)', 
                                   content, re.DOTALL)
            if class_match:
                class_content = class_match.group(1)
                # Find methods in this class
                method_pattern = r'def\s+([a-zA-Z_][a-zA-Z0-9_]*)\s*\('
                methods = re.findall(method_pattern, class_content)
                
                # Filter out common magic methods to reduce noise
                methods = [m for m in methods if not (m.startswith('__') and m.endswith('__'))]
                
                # Add methods to the functions list
                functions.extend(methods)
                
                # Also add qualified method names (Class.method)
                functions.extend([f"{class_name}.{method}" for method in methods])
        
        # 3. Find function calls (not just definitions)
        call_pattern = r'([a-zA-Z_][a-zA-Z0-9_]*)\s*\('
        potential_calls = re.findall(call_pattern, content)
        
        # Filter out common Python built-ins and keywords
        common_builtin_functions = {'print', 'len', 'range', 'int', 'str', 'list', 'dict', 'set', 'tuple', 'open', 
                                    'if', 'for', 'while', 'try', 'except', 'with', 'assert'}
        function_calls = [call for call in potential_calls if call not in common_builtin_functions and len(call) > 2]
        functions.extend(function_calls)
        
        # 4. Check for fully qualified function names in comments or docstrings
        qualified_pattern = r'([a-zA-Z_][a-zA-Z0-9_]*\.[a-zA-Z_][a-zA-Z0-9_]*(?:\.[a-zA-Z_][a-zA-Z0-9_]*)*)'
        qualified_names = re.findall(qualified_pattern, content)
        for qualified_name in qualified_names:
            # Add the full qualified name
            functions.append(qualified_name)
            # Also add the last part (just the function name)
            if '.' in qualified_name:
                functions.append(qualified_name.split('.')[-1])
        
        # 5. Find function assignments - another common pattern
        # e.g., my_func = some_module.some_function
        assignment_pattern = r'([a-zA-Z_][a-zA-Z0-9_]*)\s*=\s*([a-zA-Z_][a-zA-Z0-9_]*(?:\.[a-zA-Z_][a-zA-Z0-9_]*)*)'
        assignments = re.findall(assignment_pattern, content)
        for var_name, func_ref in assignments:
            if '.' in func_ref:  # Likely a module.function reference
                functions.append(var_name)  # The variable is likely a function reference
                functions.append(func_ref)  # The original reference
                functions.append(func_ref.split('.')[-1])  # The base function name
            
        # Remove duplicates and empty names
        functions = [f for f in set(functions) if f]
        
        return functions
    
    def _extract_via_llm(self, content: str, file_path: str) -> List[str]:
        """Use LLM to extract function names from complex code that AST and regex might miss.
        
        This is the most expensive extraction method and should be used as a last resort.
        
        Args:
            content: Code content to analyze
            file_path: Path to the file (for logging only)
            
        Returns:
            List of function names extracted via LLM
        """
        import os
        from functools import lru_cache
        from langchain_openai import ChatOpenAI
        from langchain_core.messages import HumanMessage, SystemMessage
        
        # Only use this if OpenAI API is available
        openai_api_key = os.getenv("OPENAI_API_KEY")
        if not openai_api_key:
            logger.debug("OpenAI API key not available for LLM function extraction")
            return []
        
        # For cost efficiency, only send a sample if the content is very large
        MAX_CHARS_FOR_LLM = 12000  # Limit content sent to LLM for cost efficiency
        
        if len(content) > MAX_CHARS_FOR_LLM:
            # Find logical break points to truncate the content
            import re
            
            # Try to find class and function definitions to include a reasonable subset
            def_patterns = re.finditer(r'(class|def)\s+\w+', content)
            start_points = [m.start(0) for m in def_patterns]
            
            if len(start_points) > 10:  # If we have quite a few definitions
                # Take first few definitions and some from the middle
                sample_indices = start_points[:3] + start_points[len(start_points)//2:len(start_points)//2+3]
                
                # Create chunks around these points
                chunks = []
                for idx in sorted(sample_indices):
                    start = max(0, idx - 500)  # Include some context before
                    end = min(len(content), idx + 2000)  # And more content after definition
                    chunks.append(content[start:end])
                
                # Combine chunks with markers
                truncated_content = "\n# ... [code truncated] ...\n".join(chunks)
                
                logger.debug(f"Content truncated from {len(content)} to {len(truncated_content)} chars for LLM extraction")
                content = truncated_content
            else:
                # If we don't have many definitions, take the first part of the file
                content = content[:MAX_CHARS_FOR_LLM] + "\n# ... [remaining code truncated] ..."
                logger.debug(f"Content truncated to first {MAX_CHARS_FOR_LLM} chars for LLM extraction")
        
        # Create system prompt that focuses just on extracting function names
        system_prompt = """
        You are a code analyzer specialized in identifying function and method names in Python code.
        Extract ALL function and method names from the provided code.
        
        Return your response as a JSON array of strings containing only the function and method names.
        Include:
        1. Regular function names (e.g., "calculate_total")
        2. Method names with their class prefix (e.g., "Calculator.add")
        3. Class names (e.g., "Calculator")
        
        For methods, include both the simple name and class-qualified name.
        Your response should be a valid JSON array only, with no other text.
        """
        
        # Create the messages
        messages = [
            SystemMessage(content=system_prompt),
            HumanMessage(content=f"```python\n{content}\n```")
        ]
        
        # Use GPT-3.5 for efficiency (we just need function name extraction)
        @lru_cache(maxsize=16)
        def get_llm():
            return ChatOpenAI(
                model="gpt-3.5-turbo-0125", 
                temperature=0,
                openai_api_key=openai_api_key
            )
            
        llm = get_llm()
        
        # Get response from LLM
        try:
            response = llm.invoke(messages)
            result_text = response.content.strip()
            
            # Extract JSON array from response (handle case where it might include extra text)
            import re
            import json
            
            # Find array pattern in the response
            array_pattern = r'\[.*?\]'
            array_match = re.search(array_pattern, result_text, re.DOTALL)
            
            if array_match:
                array_text = array_match.group(0)
                return json.loads(array_text)
            else:
                # Try to parse the entire response as JSON
                try:
                    return json.loads(result_text)
                except json.JSONDecodeError:
                    logger.warning(f"LLM response for {file_path} is not valid JSON: {result_text[:100]}...")
                    return []
                    
        except Exception as e:
            logger.warning(f"Error in LLM function extraction: {str(e)}")
            return []
    
    def _create_enhanced_relationship_summary(self, call_graph_data: Dict, file_path: str) -> Optional[str]:
        """
        Create a semantically enhanced function relationship summary using advanced graph analysis.
        
        This method analyzes call relationships to:
        1. Group functionally related functions
        2. Identify key entry points and utility functions
        3. Discover important patterns like command patterns, callbacks, etc.
        4. Create a more insightful hierarchy of function relationships
        
        Args:
            call_graph_data: Dictionary of call graph data from Nuanced
            file_path: Path to the source file
            
        Returns:
            Enhanced summary string or None if enhancement failed
        """
        try:
            from collections import defaultdict, Counter
            import os
            
            # Extract all function names and their relationships
            functions = set()
            relationships = []
            
            # Build directed graph of function calls
            graph = nx.DiGraph()
            
            # Track all callees to identify entry points and terminators
            all_callees = set()
            
            # Collect data from call_graph_data
            for func_name, graph_data in call_graph_data.items():
                graph.add_node(func_name)
                functions.add(func_name)
                
                for qualified_name, func_info in graph_data.items():
                    callees = func_info.get("callees", [])
                    for callee in callees:
                        # Add edge for each call relationship
                        graph.add_edge(func_name, callee)
                        graph.add_node(callee)  # Ensure node exists
                        all_callees.add(callee)
                        functions.add(callee)
                        relationships.append((func_name, callee))
            
            # Only proceed if we have enough data for meaningful analysis
            if len(functions) < 3 or len(relationships) < 3:
                logger.debug(f"Not enough data for enhanced analysis: {len(functions)} functions, {len(relationships)} relationships")
                return None
                
            # Begin building the enhanced summary
            summary = "\n\n==============================================\n"
            summary += "ADVANCED FUNCTION CALL RELATIONSHIP ANALYSIS\n"
            summary += "==============================================\n"
            summary += "This data represents the verified call relationships between functions,\n"
            summary += "organized to highlight key patterns and functional groups.\n\n"
            
            # 1. Identify entry points (called by nothing else in this module)
            entry_points = functions - all_callees
            
            if entry_points:
                summary += "## ENTRY POINT FUNCTIONS\n"
                summary += "These functions are not called by other functions and likely serve as entry points or public API:\n\n"
                for entry in sorted(entry_points):
                    # Find what this entry point calls
                    calls = []
                    for source, target in relationships:
                        if source == entry:
                            calls.append(target)
                    
                    # Add entry with its calls
                    if calls:
                        summary += f"- `{entry}` → calls: {', '.join(['`'+c+'`' for c in sorted(calls)])}\n"
                    else:
                        summary += f"- `{entry}` (doesn't call other functions)\n"
                summary += "\n"
            
            # 2. Find hub functions (called by or call many others)
            in_degree = Counter()
            out_degree = Counter()
            
            for source, target in relationships:
                out_degree[source] += 1
                in_degree[target] += 1
            
            # Hub functions called by many others (popular dependencies)
            hub_threshold = max(2, len(functions) // 10)  # Scale with codebase size
            dependency_hubs = [f for f, count in in_degree.items() if count >= hub_threshold]
            
            if dependency_hubs:
                summary += "## UTILITY/HELPER FUNCTIONS\n"
                summary += "These functions are called by many other functions and likely provide shared functionality:\n\n"
                for hub in sorted(dependency_hubs):
                    callers = [source for source, target in relationships if target == hub]
                    summary += f"- `{hub}` ← called by {len(callers)} functions: {', '.join(['`'+c+'`' for c in sorted(callers[:5])])}"
                    if len(callers) > 5:
                        summary += f" and {len(callers)-5} more"
                    summary += "\n"
                summary += "\n"
            
            # 3. Identify functional groups using community detection
            try:
                # Convert to undirected for community detection
                undirected = nx.Graph(graph)
                
                # For small graphs, use greedy modularity maximization
                if len(functions) < 50:
                    communities = nx.community.greedy_modularity_communities(undirected)
                else:
                    # For larger graphs, use label propagation (faster)
                    communities = nx.community.label_propagation_communities(undirected)
                
                # Convert communities to list for easier handling
                community_groups = [list(c) for c in communities if len(c) >= 2]
                
                if community_groups:
                    summary += "## FUNCTIONAL GROUPS\n"
                    summary += "These groups of functions likely work together closely:\n\n"
                    
                    for i, group in enumerate(community_groups, 1):
                        subgraph = graph.subgraph(group)
                        
                        # Find potential "lead" functions - entry points to the group
                        group_entries = [f for f in group if f in entry_points or in_degree[f] < out_degree[f]]
                        
                        summary += f"### Group {i}: {len(group)} related functions\n"
                        
                        if group_entries:
                            summary += f"Main functions: {', '.join(['`'+f+'`' for f in sorted(group_entries[:3])])}\n"
                        
                        # Find the most interconnected functions in this group
                        internal_edges = [(u, v) for u, v in subgraph.edges() if u in group and v in group]
                        if internal_edges:
                            summary += f"Contains {len(internal_edges)} internal call relationships\n"
                        
                        # List all functions in the group
                        summary += "Functions: " + ", ".join([f"`{f}`" for f in sorted(group)])
                        summary += "\n\n"
            except Exception as e:
                logger.warning(f"Error in community detection: {e}")
            
            # 4. Add key statistics
            summary += "## CALL RELATIONSHIP STATISTICS\n"
            summary += f"- Total functions: {len(functions)}\n"
            summary += f"- Total call relationships: {len(relationships)}\n"
            summary += f"- Entry point functions: {len(entry_points)}\n"
            summary += f"- Average calls per function: {len(relationships)/len(functions):.1f}\n"
            
            # Add filename
            file_basename = os.path.basename(file_path)
            summary += f"- File: {file_basename}\n"
            summary += "==============================================\n"
            
            return summary
            
        except ImportError as e:
            logger.warning(f"Missing dependency for enhanced summary: {e}")
            return None
        except Exception as e:
            logger.warning(f"Error creating enhanced relationship summary: {e}")
            return None

    def _enrich_document_with_nuanced(self, doc: Document, external_graph_data: Dict = None) -> Document:
        """
        Add Nuanced call graph data to a document if available.
        
        Args:
            doc: The document to enhance
            external_graph_data: Optional external graph data to use instead of querying Nuanced
        """
        import os  # Import os module to ensure it's available in this scope
        
        if not self.nuanced_available:
            return doc
            
        try:
            # Get file path from metadata
            file_path = doc.metadata.get("file_path")
            if not file_path:
                logger.debug("No file_path in document metadata, skipping Nuanced enrichment")
                return doc
                
            # Check if Python file
            if not file_path.endswith('.py'):
                logger.debug(f"Skipping Nuanced enrichment for non-Python file: {file_path}")
                return doc
                
            # Check if document already has Nuanced data in metadata (from Pinecone)
            if "nuanced_graph_compact" in doc.metadata:
                logger.debug(f"Document already has Nuanced data from compact graph")
                
                # Extract call graph from compact representation
                compact_graph = doc.metadata["nuanced_graph_compact"]
                call_graph_data = {}
                
                # Extract function names from content
                function_names = self._extract_function_names(file_path, doc.page_content)
                
                # Match functions from document with compact graph
                for function_name in function_names:
                    if function_name in compact_graph.get("functions", {}):
                        func_data = compact_graph["functions"][function_name]
                        
                        # Create enrichment data in same format as NuancedService.enrich_function
                        qualified_name = f"{os.path.basename(file_path)}:{function_name}"
                        call_graph_data[function_name] = {
                            qualified_name: {
                                "filepath": func_data.get("path", file_path),
                                "callees": func_data.get("calls", [])
                            }
                        }
                
                # If we extracted data from compact graph, process it
                if call_graph_data:
                    logger.info(f"Enhanced document using compact graph data, found {len(call_graph_data)} functions")
                else:
                    logger.debug(f"No matching functions found in compact graph data")
                
                # Continue to graph summary creation below
                enriched_count = len(call_graph_data)
                
            # Try to use external graph data if repository doesn't exist
            elif external_graph_data and not os.path.exists(self.repo_path):
                logger.debug(f"Using externally provided graph data for enhancement")
                
                # Extract function names from content
                function_names = self._extract_function_names("unknown", doc.page_content)
                logger.debug(f"Found {len(function_names)} function names in document")
                
                # Use external graph data to enhance functions with improved matching
                call_graph_data = {}
                enriched_count = 0
                
                # Add a function for smart function name matching
                def match_function_with_graph(function_name, graph_data):
                    """
                    Use advanced techniques to match function names with graph data.
                    Implements fuzzy matching, namespace resolution, and contextual matching.
                    
                    Args:
                        function_name: Function name to match
                        graph_data: Graph data dictionary
                        
                    Returns:
                        Tuple of (matched_name, function_data) or None if no match
                    """
                    import Levenshtein
                    
                    # 1. First try direct match (exact match)
                    if "functions" in graph_data:
                        # Traditional format
                        for func_id, func_data in graph_data.get("functions", {}).items():
                            db_func_name = func_data.get("name", "")
                            
                            # Exact match
                            if db_func_name == function_name:
                                return (db_func_name, func_data)
                            
                            # Qualified name match (e.g. "module.Class.function")
                            if db_func_name.endswith(f".{function_name}"):
                                return (db_func_name, func_data)
                                
                            # Simple name match (last part matches)
                            if "." in db_func_name and db_func_name.split(".")[-1] == function_name:
                                return (db_func_name, func_data)
                    else:
                        # Flat format where function names are keys
                        
                        # Direct match
                        if function_name in graph_data:
                            return (function_name, graph_data[function_name])
                        
                        # Try to match with qualified names
                        for db_func_name, func_data in graph_data.items():
                            # Extract simple name for comparison
                            simple_db_name = db_func_name.split(".")[-1] if "." in db_func_name else db_func_name
                            
                            # Exact match with simple name
                            if simple_db_name == function_name:
                                return (db_func_name, func_data)
                                
                            # Qualified name ending with function name
                            if db_func_name.endswith(f".{function_name}"):
                                return (db_func_name, func_data)
                    
                    # 2. Try fuzzy matching for near matches (e.g. typos, minor variations)
                    best_match = None
                    best_score = float('inf')
                    FUZZY_THRESHOLD = 2  # Maximum edit distance for fuzzy matching
                    
                    # Different graph formats
                    if "functions" in graph_data:
                        # Traditional format
                        for func_id, func_data in graph_data.get("functions", {}).items():
                            db_func_name = func_data.get("name", "")
                            
                            # Get simple name
                            simple_db_name = db_func_name.split(".")[-1] if "." in db_func_name else db_func_name
                            
                            # Check edit distance between simple names
                            distance = Levenshtein.distance(simple_db_name, function_name)
                            if distance < FUZZY_THRESHOLD and distance < best_score:
                                best_match = (db_func_name, func_data)
                                best_score = distance
                    else:
                        # Flat format
                        for db_func_name, func_data in graph_data.items():
                            # Extract simple name
                            simple_db_name = db_func_name.split(".")[-1] if "." in db_func_name else db_func_name
                            
                            # Check edit distance
                            distance = Levenshtein.distance(simple_db_name, function_name)
                            if distance < FUZZY_THRESHOLD and distance < best_score:
                                best_match = (db_func_name, func_data)
                                best_score = distance
                    
                    # 3. If we have a good fuzzy match, return it
                    if best_match:
                        logger.debug(f"Found fuzzy match for '{function_name}': '{best_match[0]}' (distance: {best_score})")
                        return best_match
                        
                    # 4. Namespace-aware matching (more complex relationships)
                    # Sometimes functions have namespace prefixes in one context but not the other
                    if "." in function_name:
                        # Try matching with the last part of the namespace
                        simple_function_name = function_name.split(".")[-1]
                        
                        # Recursively try matching with the simplified name
                        simple_match = match_function_with_graph(simple_function_name, graph_data)
                        if simple_match:
                            logger.debug(f"Found namespace match for '{function_name}' using simplified name '{simple_function_name}'")
                            return simple_match
                    
                    # No match found
                    return None
                
                # Process based on graph format
                if "functions" in external_graph_data:
                    # Traditional format with functions and modules keys
                    for function_name in function_names:
                        match_result = match_function_with_graph(function_name, external_graph_data)
                        if match_result:
                            db_func_name, func_data = match_result
                            qualified_name = f"external:{function_name}"
                            call_graph_data[function_name] = {
                                qualified_name: {
                                    "filepath": func_data.get("filepath", "unknown"),
                                    "callees": func_data.get("callees", []),
                                    "matched_from": db_func_name  # Store original matched name for debugging
                                }
                            }
                            enriched_count += 1
                else:
                    # Flat format with function names as keys
                    for function_name in function_names:
                        match_result = match_function_with_graph(function_name, external_graph_data)
                        if match_result:
                            db_func_name, func_data = match_result
                            qualified_name = f"external:{function_name}"
                            call_graph_data[function_name] = {
                                qualified_name: {
                                    "filepath": func_data.get("filepath", "unknown"),
                                    "callees": func_data.get("callees", []),
                                    "matched_from": db_func_name  # Store original matched name for debugging
                                }
                            }
                            enriched_count += 1
                
                # Log results of external data enhancement
                logger.info(f"Enhanced {enriched_count}/{len(function_names)} functions using external graph data")
            
            # Local repository exists, use standard approach with NuancedService
            else:
                # Validate file existence
                if not os.path.exists(file_path):
                    # Try to resolve the path relative to repo_path
                    relative_path = os.path.join(self.repo_path, os.path.basename(file_path))
                    if os.path.exists(relative_path):
                        file_path = relative_path
                        logger.debug(f"Resolved file path to: {file_path}")
                    else:
                        logger.warning(f"File not found for Nuanced enrichment: {file_path}")
                        return doc
                
                # Extract function names from content
                function_names = self._extract_function_names(file_path, doc.page_content)
                logger.debug(f"Found {len(function_names)} function names in {file_path}")
                
                if not function_names:
                    logger.debug(f"No functions found in {file_path}, skipping Nuanced enrichment")
                    return doc
                    
                # Get Nuanced data for the functions
                call_graph_data = {}
                enriched_count = 0
                
                for function_name in function_names:
                    try:
                        # Try to enrich the function using NuancedService
                        function_data = NuancedService.enrich_function(
                            self.repo_path, 
                            file_path, 
                            function_name
                        )
                        
                        if function_data:
                            call_graph_data[function_name] = function_data
                            enriched_count += 1
                            logger.debug(f"Successfully enriched function: {function_name}")
                        else:
                            logger.debug(f"No enrichment data for function: {function_name}")
                            
                    except Exception as func_error:
                        # Continue with other functions if one fails
                        logger.warning(f"Error enriching function {function_name}: {str(func_error)}")
                        continue
            
            logger.info(f"Enriched {enriched_count}/{len(function_names)} functions in {file_path}")
            
            if call_graph_data:
                # Add Nuanced data to metadata
                doc.metadata["nuanced_call_graph"] = call_graph_data
                
                # If we have significant call graph data, perform semantic grouping and analysis
                if len(call_graph_data) > 5:
                    # Create a more structured and semantically organized summary
                    try:
                        enhanced_summary = self._create_enhanced_relationship_summary(call_graph_data, file_path)
                        
                        # Try to add advanced AI insights for very complex graphs
                        if len(call_graph_data) > 10:
                            try:
                                # Import the analysis function
                                from utils.retriever_utils import generate_nuanced_insight, generate_nuanced_insight_async
                                
                                # Generate AI-powered insights
                                import asyncio
                                import os as path_os  # Import with different name to avoid shadowing
                                
                                # Get file basename for context
                                file_basename = path_os.path.basename(file_path)
                                
                                # Run insight generation
                                insights = None
                                try:
                                    # Try the synchronous version directly to avoid event loop issues
                                    insights = generate_nuanced_insight(call_graph_data, file_basename)
                                    
                                    # If the synchronous version fails, we can try the async version as a fallback
                                    if insights is None and asyncio.get_event_loop().is_running():
                                        # Use run_coroutine_threadsafe instead of direct await
                                        loop = asyncio.get_event_loop()
                                        future = asyncio.run_coroutine_threadsafe(
                                            generate_nuanced_insight_async(call_graph_data, file_basename),
                                            loop
                                        )
                                        # Get result with timeout
                                        insights = future.result(timeout=10)
                                except Exception as e:
                                    logger.warning(f"Error in insight generation: {e}")
                                    insights = None
                                # Add insights if available
                                if insights:
                                    if enhanced_summary:
                                        enhanced_summary += insights
                                    else:
                                        enhanced_summary = insights
                                    logger.info(f"Added AI-generated architectural insights to document")
                            except Exception as insight_error:
                                logger.warning(f"Failed to generate AI insights: {insight_error}")
                                # Continue without insights
                        
                        if enhanced_summary:
                            # Use the enhanced summary if available
                            doc.page_content += enhanced_summary
                            logger.info(f"Added semantically enhanced call graph summary to document")
                            return doc
                    except Exception as e:
                        logger.warning(f"Error creating enhanced summary: {e}, falling back to basic summary")
                        # Continue with basic summary on error
                
                # Otherwise, create a standard summary
                call_graph_summary = "\n\n==============================================\n"
                call_graph_summary += "FUNCTION CALL RELATIONSHIP DATA (VERIFIED THROUGH CODE ANALYSIS)\n"
                call_graph_summary += "==============================================\n"
                call_graph_summary += "This data shows the actual function call relationships in the code.\n"
                call_graph_summary += "It was generated through static analysis and is factually accurate.\n\n"
                
                # Add summary stats
                total_functions = len(call_graph_data)
                total_callees = 0
                
                for func_name, graph_data in call_graph_data.items():
                    callees = []
                    for qualified_name, func_info in graph_data.items():
                        if "callees" in func_info:
                            callees.extend(func_info["callees"])
                    
                    total_callees += len(callees)
                    
                    if callees:
                        call_graph_summary += f"\n## Function '{func_name}' calls these functions:\n"
                        # Sort callees for consistency
                        for callee in sorted(callees):
                            call_graph_summary += f"- {callee}\n"
                
                # Add total count information
                call_graph_summary += f"\n## Call Relationship Statistics:\n"
                call_graph_summary += f"- Total functions with relationships: {total_functions}\n"
                call_graph_summary += f"- Total call relationships: {total_callees}\n"
                call_graph_summary += "==============================================\n"
                
                # Add the summary to the document
                doc.page_content += call_graph_summary
                
                logger.info(f"Enhanced document with {enriched_count} functions and {total_callees} total callees")
            else:
                logger.debug(f"No call graph data found for any function in {file_path}")
            
            return doc
        except Exception as e:
            logger.error(f"Error enriching document with Nuanced: {str(e)}")
            # Return the original document if enrichment fails
            return doc
    
    def _get_relevant_documents(self, query: str, *, run_manager: CallbackManagerForRetrieverRun = None) -> List[Document]:
        """Get documents from base retriever and enhance them with Nuanced data."""
        # Get documents from the base retriever
        if self.base_retriever:
            docs = self.base_retriever._get_relevant_documents(query, run_manager=run_manager)
        else:
            # In enhancement-only mode without a base retriever, return empty list
            logger.warning("No base retriever provided, returning empty document list")
            return []
        
        # Print clear Nuanced banner to make activity visible in logs
        logger.info("")
        logger.info(f"==== 🔍 NUANCED CALL GRAPH REQUESTED ====")
        logger.info(f"Project ID: {self.project_id}")
        logger.info(f"Documents: {len(docs)}")

        # If Nuanced is not available and no external graph, return the original documents
        if not self.nuanced_available and not self.external_graph:
            logger.warning("⚠️ NUANCED NOT AVAILABLE: Returning unenhanced documents")
            logger.warning("To enable Nuanced, please install it with: pip install nuanced")
            return docs
            
        # Use the external graph data if provided
        graph_data = self.external_graph
        
        # Verify we have a project ID
        if not self.project_id and self.repo_path:
            # Use NuancedService's helper method to extract project ID from path
            try:
                from services.nuanced_service import NuancedService
                extracted_id = NuancedService.extract_project_id_from_path(self.repo_path)
                if extracted_id:
                    self.project_id = extracted_id
                    logger.info(f"Extracted project ID from repo path: {self.project_id}")
            except ImportError:
                logger.warning("Could not import NuancedService, cannot extract project ID")
            except Exception as e:
                logger.warning(f"Error extracting project ID: {str(e)}")
        
        if self.project_id and not graph_data:
            # Check if repository exists
            repo_exists = os.path.exists(self.repo_path)
            logger.info(f"Repository exists: {repo_exists} ({self.repo_path})")
            
            if not repo_exists:
                logger.warning(f"❌ REPOSITORY NOT FOUND: {self.repo_path}")
                
                # Try to get graph from database
                try:
                    from services.nuanced_service import NuancedService
                    logger.info(f"Attempting to retrieve Nuanced graph from database...")
                    
                    graph_data = NuancedService.get_graph_from_db(self.project_id)
                    if graph_data:
                        logger.info(f"✅ Retrieved graph from database with {len(graph_data)} functions")
                    else:
                        logger.warning(f"No Nuanced graph found for project {self.project_id}")
                        
                        # Check if auto-regeneration is enabled
                        retry_attempts = 0
                        if getattr(NuancedService, "AUTO_REGENERATE_GRAPHS", False):
                            while retry_attempts < self.max_retries:
                                retry_attempts += 1
                                logger.info(f"🔄 AUTO-REGENERATION enabled, attempting to regenerate graph from vectorstore (attempt {retry_attempts}/{self.max_retries})")
                                
                                try:
                                    graph_data = NuancedService.regenerate_graph_from_vectorstore(self.project_id)
                                    if graph_data:
                                        logger.info(f"✅ Successfully regenerated graph with {len(graph_data)} functions")
                                        break  # Exit the retry loop on success
                                    else:
                                        logger.warning(f"❌ Regeneration attempt {retry_attempts} failed, no graph data returned")
                                except Exception as regen_error:
                                    logger.warning(f"❌ Regeneration attempt {retry_attempts} failed with error: {str(regen_error)}")
                                
                                # If this wasn't the last attempt, wait briefly before retrying
                                if retry_attempts < self.max_retries:
                                    logger.info(f"⏳ Waiting 1 second before retry {retry_attempts + 1}...")
                                    import time
                                    time.sleep(1)
                            
                            if not graph_data:
                                logger.warning(f"❌ All {self.max_retries} regeneration attempts failed")
                        
                        # If still no graph data, try getting compact graph from document metadata
                        if not graph_data:
                            for doc in docs:
                                if "nuanced_graph_compact" in doc.metadata:
                                    logger.info(f"Found compact graph in document metadata")
                                    # Convert compact format to full graph format
                                    compact_graph = doc.metadata["nuanced_graph_compact"]
                                    
                                    if "functions" in compact_graph:
                                        # Already in a usable format, just use directly
                                        graph_data = compact_graph
                                        function_count = len(compact_graph.get("functions", {}))
                                        logger.info(f"✅ USING COMPACT GRAPH: {function_count} functions")
                                    else:
                                        # Need to convert to a usable format
                                        graph_data = {
                                            "functions": {},
                                            "modules": {}
                                        }
                                        
                                        # Convert functions from compact to full format
                                        for func_name, func_data in compact_graph.get("functions", {}).items():
                                            func_id = f"func_{hash(func_name) % 10000}"
                                            graph_data["functions"][func_id] = {
                                                "name": func_name,
                                                "filepath": func_data.get("path", "unknown"),
                                                "callees": [f"func_{hash(callee) % 10000}" for callee in func_data.get("calls", [])]
                                            }
                                            
                                        function_count = len(graph_data.get("functions", {}))
                                        logger.info(f"✅ CONVERTED COMPACT GRAPH: {function_count} functions")
                                    
                                    # Store the reconstructed graph in the database for future use
                                    if graph_data and not NuancedService.get_graph_from_db(self.project_id):
                                        logger.info(f"Storing reconstructed graph in database for future use")
                                        NuancedService.store_graph_in_db(self.project_id, graph_data=graph_data)
                                    
                                    break
                        
                        # Suggest manual regeneration if still not found and auto-regeneration failed
                        if not graph_data:
                            logger.info(f"💡 TIP: You can regenerate the graph using the API endpoint:")
                            logger.info(f"POST /api/nuanced/regenerate/{self.project_id}")
                except Exception as e:
                    logger.error(f"Error retrieving graph from database: {str(e)}")
        
        if not graph_data and not os.path.exists(self.repo_path):
            # Check for alternative paths
            if self.project_id:
                alt_paths = [
                    f"/tmp/my_local_repo_{self.project_id}",
                    f"/tmp/nuanced_regen_{self.project_id}",
                    f"/tmp/nuanced_test_{self.project_id}"
                ]
                
                for path in alt_paths:
                    if os.path.exists(path):
                        logger.info(f"Found alternative repository path: {path}")
                        self.repo_path = path
                        break
            
            if not os.path.exists(self.repo_path):
                logger.warning("❌ NO REPO FOUND: Could not find any repository for project " + 
                              f"{self.project_id}")
                return docs
        
        # Log Nuanced availability
        try:
            from services.nuanced_service import NuancedService
            logger.info(f"Nuanced installed: {NuancedService.is_installed()}")
            logger.info(f"Repository exists: {os.path.exists(self.repo_path)} ({self.repo_path})")
        except ImportError:
            pass
        
        # Enhance documents with Nuanced data
        enhanced_count = 0
        func_count = 0
        relationships_count = 0
        enhanced_docs = []
        
        logger.info(f"🔄 NUANCED PROCESS STARTING: Enhancing {len(docs)} documents...")
        
        for doc in docs:
            # If we have external graph data from DB/metadata, use it
            if not repo_exists and graph_data:
                enhanced_doc = self._enrich_document_with_nuanced(doc, external_graph_data=graph_data)
            else:
                enhanced_doc = self._enrich_document_with_nuanced(doc)
            
            # Check if enhancement added any data
            was_enhanced = "nuanced_call_graph" in enhanced_doc.metadata
            
            if was_enhanced:
                call_data = enhanced_doc.metadata.get("nuanced_call_graph", {})
                functions = len(call_data)
                
                # Count relationships
                relationships = 0
                for func_name, graph_data in call_data.items():
                    for qualified_name, func_info in graph_data.items():
                        relationships += len(func_info.get("callees", []))
                
                func_count += functions
                relationships_count += relationships
                enhanced_count += 1
                
                logger.info(f"Enhanced document: {enhanced_doc.metadata.get('file_path', 'unknown')}")
                logger.info(f"- Functions: {functions}")
                logger.info(f"- Relationships: {relationships}")
            
            enhanced_docs.append(enhanced_doc)
        
        logger.info(f"")
        logger.info(f"==== 🔍 NUANCED ENHANCEMENT COMPLETE ====")
        logger.info(f"Enhanced {enhanced_count}/{len(docs)} documents")
        logger.info(f"Total functions: {func_count}")
        logger.info(f"Total call relationships: {relationships_count}")
        logger.info(f"==========================================")
        
        return enhanced_docs


class GraphRAGRetriever(BaseRetriever):
    """A Graph RAG-based retriever that implements hierarchical retrieval based on knowledge graphs.
    
    This retriever enhances traditional RAG by creating and using knowledge graphs from code repositories.
    Instead of relying solely on vector similarity, it utilizes structured relationships between code entities
    to provide more contextual and relevant results.
    
    Features:
    - Community-based hierarchical retrieval
    - Support for multiple query modes: global search, local search, and drift search
    - Enhanced reasoning about code relationships
    
    Based on Microsoft's GraphRAG architecture: https://github.com/microsoft/graphrag
    """
    
    base_retriever: Optional[BaseRetriever] = None
    repo_path: str = Field(default="")
    graph_data: Optional[Dict] = None
    project_id: Optional[str] = Field(default=None)
    query_mode: str = Field(default="auto")  # "global", "local", "drift", or "auto"
    
    def __init__(
        self, 
        base_retriever: Optional[BaseRetriever] = None, 
        repo_path: str = "", 
        project_id: Optional[str] = None,
        graph_data: Optional[Dict] = None,
        query_mode: str = "auto"
    ):
        """Initialize the GraphRAG retriever.
        
        Args:
            base_retriever: The underlying retriever to enhance with GraphRAG
            repo_path: Path to the code repository
            project_id: ID of the project for fetching stored graph data
            graph_data: Optional pre-loaded graph data
            query_mode: Which query strategy to use (global, local, drift, or auto)
        """
        super().__init__()
        self.base_retriever = base_retriever
        self.repo_path = repo_path
        self.project_id = project_id
        self.graph_data = graph_data
        self.query_mode = query_mode
        
        # For networkx graph manipulation
        self._nx_graph = None
        self._communities = None
        self._community_summaries = None
        
        # Log initialization
        logger.info(f"🔍 GraphRAGRetriever initialized")
        logger.info(f"   - Repo Path: {self.repo_path}")
        logger.info(f"   - Project ID: {self.project_id}")
        logger.info(f"   - Query Mode: {self.query_mode}")
        logger.info(f"   - Graph Data Provided: {graph_data is not None}")
        logger.info(f"   - Base Retriever: {type(self.base_retriever).__name__ if self.base_retriever else 'None'}")
    
    def _initialize_graph(self):
        """Initialize the knowledge graph from available sources."""
        if self._nx_graph is not None:
            return True  # Graph is already initialized
            
        # 1. First try to get graph data from database using project_id (preferred method)
        if not self.graph_data and self.project_id:
            try:
                logger.info(f"Attempting to retrieve graph data from database for project {self.project_id}")
                from services.nuanced_service import NuancedService
                self.graph_data = NuancedService.get_graph_from_db(self.project_id)
                if self.graph_data:
                    logger.info(f"Successfully retrieved graph data from database for project {self.project_id}")
            except ImportError:
                logger.warning("NuancedService not available for database graph retrieval")
            except Exception as e:
                logger.warning(f"Error retrieving graph data from database: {e}")
                
        # 2. If no graph data yet, try to get repo path from project metadata
        if not self.graph_data and self.project_id and not os.path.exists(self.repo_path):
            try:
                from db import MongoDB
                db = MongoDB()
                project = db.db.projects.find_one({"project_id": self.project_id})
                if project and "graphrag_repo_path" in project:
                    repo_path = project["graphrag_repo_path"]
                    if os.path.exists(repo_path):
                        logger.info(f"Found repository path in project metadata: {repo_path}")
                        self.repo_path = repo_path
            except Exception as e:
                logger.warning(f"Error retrieving repo path from project metadata: {e}")
                
        # 3. If repo path doesn't exist, try common alternative paths
        if not self.graph_data and self.project_id and not os.path.exists(self.repo_path):
            alt_paths = [
                f"/tmp/my_local_repo_{self.project_id}",
                f"/tmp/nia_repo_{self.project_id}",
                f"/tmp/graph_rag_repo_{self.project_id}"
            ]
            
            for alt_path in alt_paths:
                if os.path.exists(alt_path):
                    logger.info(f"Found alternative repository path: {alt_path}")
                    self.repo_path = alt_path
                    break
                    
        # 4. If we have a valid repo path, try to extract graph data from it
        if not self.graph_data and os.path.exists(self.repo_path):
            try:
                from services.nuanced_service import NuancedService
                logger.info(f"Attempting to extract graph data from repository at {self.repo_path}")
                
                # Try looking for Nuanced graph first
                nuanced_path = os.path.join(self.repo_path, ".nuanced", "nuanced-graph.json")
                if os.path.exists(nuanced_path):
                    self.graph_data = NuancedService.get_graph_data(nuanced_path)
                    if self.graph_data:
                        logger.info(f"Successfully extracted graph data from Nuanced graph at {nuanced_path}")
                else:
                    # Try to generate graph on-the-fly using Nuanced
                    if NuancedService.is_installed():
                        try:
                            logger.info(f"Generating graph data on-the-fly from repository")
                            self.graph_data = NuancedService.generate_graph(self.repo_path)
                            if self.graph_data:
                                logger.info(f"Successfully generated graph data from repository")
                                # Store it for future use
                                if self.project_id:
                                    NuancedService.store_graph_in_db(self.project_id, self.graph_data)
                        except Exception as gen_error:
                            logger.warning(f"Error generating graph data: {gen_error}")
            except ImportError:
                logger.warning("NuancedService not available for graph extraction")
            except Exception as e:
                logger.warning(f"Error extracting graph data from repository: {e}")
                
        # 5. Last resort: use our new LLM-based knowledge graph extraction from vectorstore
        if not self.graph_data and self.project_id and self.base_retriever:
            try:
                logger.info(f"Attempting to regenerate graph using LLM-based extraction from vector store for project {self.project_id}")
                # Use asyncio to run the async method in a synchronous context
                loop = asyncio.get_event_loop()
                success = loop.run_until_complete(self.regenerate_graph_from_vectorstore())
                if success:
                    logger.info(f"Successfully regenerated graph using LLM-based extraction from vector store")
                    return True
            except Exception as e:
                logger.error(f"Error regenerating graph using LLM-based extraction: {str(e)}")
                
        # If we still don't have graph data, we can't initialize the graph
        if not self.graph_data:
            logger.warning(f"Could not obtain graph data for project {self.project_id}")
            return False
        
        # Now construct the graph from the data we have
        try:
            # Create a directed graph
            self._nx_graph = nx.DiGraph()
            
            # Check graph format and extract nodes and edges
            if "entities" in self.graph_data:
                # New LLM-extracted format
                for entity_id, entity in self.graph_data.get("entities", {}).items():
                    self._nx_graph.add_node(
                        entity_id, 
                        name=entity.get("name", entity_id),
                        type=entity.get("type", "entity"),
                        description=entity.get("description", "")
                    )
                    
                for rel in self.graph_data.get("relationships", []):
                    source = rel.get("source")
                    target = rel.get("target")
                    if source and target and self._nx_graph.has_node(source) and self._nx_graph.has_node(target):
                        self._nx_graph.add_edge(
                            source,
                            target,
                            type=rel.get("type", "relates_to"),
                            description=rel.get("description", "")
                        )
                
                # Add claims as node attributes
                for claim in self.graph_data.get("claims", []):
                    entity_id = claim.get("entity_id")
                    claim_text = claim.get("text")
                    if entity_id and claim_text and self._nx_graph.has_node(entity_id):
                        if "claims" not in self._nx_graph.nodes[entity_id]:
                            self._nx_graph.nodes[entity_id]["claims"] = []
                        self._nx_graph.nodes[entity_id]["claims"].append(claim_text)
            
            elif "functions" in self.graph_data and "modules" in self.graph_data:
                # Traditional format from Nuanced
                for func_id, func_data in self.graph_data.get("functions", {}).items():
                    func_name = func_data.get("name", func_id)
                    self._nx_graph.add_node(
                        func_name, 
                        type="function",
                        filepath=func_data.get("filepath", ""),
                        id=func_id
                    )
                    
                    # Add edges for function calls
                    for callee_id in func_data.get("callees", []):
                        if callee_id in self.graph_data.get("functions", {}):
                            callee_data = self.graph_data["functions"][callee_id]
                            callee_name = callee_data.get("name", callee_id)
                            self._nx_graph.add_edge(func_name, callee_name)
            else:
                # Flat format (function names as keys)
                for func_name, func_data in self.graph_data.items():
                    self._nx_graph.add_node(
                        func_name,
                        type="function",
                        filepath=func_data.get("filepath", "")
                    )
                    
                    # Add edges for function calls
                    for callee in func_data.get("callees", []):
                        self._nx_graph.add_edge(func_name, callee)
                        # Add callee node if it doesn't exist
                        if not self._nx_graph.has_node(callee):
                            self._nx_graph.add_node(callee, type="function")
            
            logger.info(f"Successfully created graph with {self._nx_graph.number_of_nodes()} nodes and {self._nx_graph.number_of_edges()} edges")
            return True
            
        except ImportError:
            logger.warning("networkx not available, can't create graph")
            return False
        except Exception as e:
            logger.error(f"Error creating graph: {str(e)}")
            return False
    
    async def _get_relevant_documents(
        self, 
        query: str, 
        *, 
        run_manager: Optional[CallbackManagerForRetrieverRun] = None
    ) -> List[Document]:
        """Get relevant documents enhanced with GraphRAG capabilities."""
        logger.info("")
        logger.info(f"==== 🔍 GRAPH RAG RETRIEVAL ====")
        logger.info(f"Query: {query}")
        logger.info(f"Project ID: {self.project_id}")
        logger.info(f"Repo path: {self.repo_path} (exists: {os.path.exists(self.repo_path) if self.repo_path else False})")
        logger.info(f"Graph data available: {self.graph_data is not None}")
        
        # Determine search mode based on query
        search_mode = self._determine_query_mode(query)
        logger.info(f"Using search mode: {search_mode}")
        
        # Check if we have a base retriever
        if not self.base_retriever:
            logger.warning("No base retriever provided, cannot retrieve documents")
            return []
        
        # Try to initialize graph, but continue with base retrieval if it fails
        graph_initialized = self._initialize_graph()
        if not graph_initialized:
            logger.warning("GraphRAG initialization failed, falling back to base retriever")
            try:
                docs = await self.base_retriever.ainvoke(query)
                logger.info(f"Retrieved {len(docs)} documents using base retriever (GraphRAG disabled)")
                logger.info(f"==========================================")
                return docs
            except Exception as e:
                logger.error(f"Error in base retrieval: {e}")
                return []
        
        # Execute search based on mode
        try:
            logger.info(f"🎯 Executing GraphRAG {search_mode} search")
            if search_mode == "global":
                docs = await self._global_search(query)
            elif search_mode == "local":
                docs = await self._local_search(query)
            elif search_mode == "drift":
                docs = await self._drift_search(query)
            else:
                logger.warning(f"Unknown search mode: {search_mode}, using base retriever")
                docs = await self.base_retriever.ainvoke(query)
                
            logger.info(f"Retrieved {len(docs)} documents using {search_mode} GraphRAG search")
            
            # Add GraphRAG marker to all document metadata
            for doc in docs:
                if isinstance(doc.metadata, dict):
                    doc.metadata["graphrag_enhanced"] = True
                    doc.metadata["graphrag_search_mode"] = search_mode
                
            logger.info(f"✅ GRAPHRAG SUCCESS: Enhanced retrieval with {search_mode} mode")
            logger.info(f"==========================================")
            return docs
            
        except Exception as e:
            logger.error(f"Error in GraphRAG retrieval: {e}")
            import traceback
            logger.error(f"Stack trace: {traceback.format_exc()}")
            logger.info(f"==========================================")
            
            # Fallback to base retriever on error
            try:
                logger.warning("GraphRAG retrieval failed, falling back to base retriever")
                docs = await self.base_retriever.ainvoke(query)
                logger.info(f"Retrieved {len(docs)} documents using base retriever (GraphRAG fallback)")
                return docs
            except Exception as base_e:
                logger.error(f"Even base retriever failed: {base_e}")
                return []
    
    def _determine_query_mode(self, query: str) -> str:
        """Determine the most appropriate query mode based on the query content."""
        if self.query_mode != "auto":
            return self.query_mode
            
        # Check if query mentions a specific function or entity (local search)
        import re
        function_patterns = [
            r'function\s+(\w+)',
            r'method\s+(\w+)',
            r'class\s+(\w+)',
            r'module\s+(\w+)',
            r'\b(\w+)\s+function\b',
            r'\b(\w+)\s+method\b',
            r'\b(\w+)\s+class\b',
            r'\b(\w+)\.([\w\.]+)\s*\(', # Function calls
            r'\bdef\s+(\w+)\b'  # Python function definition
        ]
        
        # Check for matches
        for pattern in function_patterns:
            matches = re.search(pattern, query, re.IGNORECASE)
            if matches:
                entity_name = matches.group(1)
                logger.info(f"Detected local search for entity: {entity_name}")
                
                # If query explicitly asks about relationships, use drift search for broader context
                if re.search(r'relate|relationship|connect|call|depend|use', query, re.IGNORECASE):
                    return "drift"
                return "local"
        
        # Check if query is asking for high-level overview (global search)
        global_patterns = [
            r'overview',
            r'summary',
            r'architecture',
            r'system',
            r'structure',
            r'organization',
            r'high(\s|-)?level',
            r'explain the codebase',
            r'main components'
        ]
        
        for pattern in global_patterns:
            if re.search(pattern, query, re.IGNORECASE):
                logger.info(f"Detected global search based on query patterns")
                return "global"
        
        # Default to drift search for most detailed results
        return "drift"
    
    async def _global_search(self, query: str) -> List[Document]:
        """Perform a global search using community summaries."""
        if not await self._generate_community_summaries() or not self._community_summaries:
            logger.warning("Community summaries not available, falling back to base retriever")
            return await self.base_retriever.ainvoke(query)
            
        try:
            # Create a document from each community summary
            community_docs = []
            for community_id, summary in self._community_summaries.items():
                # Get community nodes
                community = self._communities[community_id]
                
                # Create document with community summary
                doc = Document(
                    page_content=f"Community {community_id} Summary:\n{summary}\n\nFunctions: {', '.join(community[:5])}" + 
                               (f" and {len(community) - 5} more" if len(community) > 5 else ""),
                    metadata={
                        "community_id": community_id,
                        "source": f"graph_community_{community_id}",
                        "function_count": len(community),
                        "summary_type": "community",
                        "is_graph_rag": True
                    }
                )
                community_docs.append(doc)
            
            # Also get base results for comparison/combination
            base_docs = await self.base_retriever.ainvoke(query)
            
            # Combine community docs with base docs (prioritize community docs)
            combined_docs = community_docs + base_docs
            
            # Re-rank if possible to ensure most relevant communities come first
            try:
                from backend.reranker import build_reranker, RerankerProvider
                reranker = build_reranker(RerankerProvider.NVIDIA.value, "nvidia/nv-rerankqa-mistral-4b-v3", 10)
                if reranker:
                    combined_docs = await reranker.acompress_documents(combined_docs, query)
            except Exception as e:
                logger.warning(f"Error re-ranking combined docs: {e}")
            
            # Return a limited number of results 
            return combined_docs[:15]  # Limit to 15 for reasonable context
            
        except Exception as e:
            logger.error(f"Error in global search: {e}")
            if self.base_retriever:
                return await self.base_retriever.ainvoke(query)
            return []
    
    async def _local_search(self, query: str, entity_name: Optional[str] = None) -> List[Document]:
        """Perform a local search focused on a specific entity."""
        if not self._initialize_graph() or not self._nx_graph:
            logger.warning("Graph not available, falling back to base retriever")
            return await self.base_retriever.ainvoke(query)
            
        try:
            import re
            
            # Extract entity name from query if not provided
            if not entity_name:
                # Extract entity names from query
                entity_patterns = [
                    r'function\s+(\w+)',
                    r'method\s+(\w+)',
                    r'class\s+(\w+)',
                    r'module\s+(\w+)',
                    r'\b(\w+)\s+function\b',
                    r'\b(\w+)\s+method\b',
                    r'\b(\w+)\s+class\b'
                ]
                
                for pattern in entity_patterns:
                    matches = re.search(pattern, query, re.IGNORECASE)
                    if matches:
                        entity_name = matches.group(1)
                        break
            
            if not entity_name:
                logger.warning("No entity name found for local search, falling back to base retriever")
                return await self.base_retriever.ainvoke(query)
                
            # Try to find this entity in the graph
            matching_nodes = []
            for node in self._nx_graph.nodes():
                # Check for exact match
                if node == entity_name:
                    matching_nodes.append(node)
                # Check for partial match (e.g., class method)
                elif entity_name in node.split('.'):
                    matching_nodes.append(node)
                # Check for substring match
                elif entity_name in node:
                    matching_nodes.append(node)
            
            if not matching_nodes:
                logger.warning(f"Entity {entity_name} not found in graph, falling back to base retriever")
                return await self.base_retriever.ainvoke(query)
                
            # Use the most exact match first
            main_entity = matching_nodes[0]
            
            # Get all neighbors (incoming and outgoing)
            in_neighbors = list(self._nx_graph.predecessors(main_entity))
            out_neighbors = list(self._nx_graph.successors(main_entity))
            
            # Create documents from entity and its relationships
            entity_docs = []
            
            # Main entity document
            entity_info = f"Function: {main_entity}\n\n"
            entity_info += f"Called by: {', '.join(in_neighbors[:10])}" + (f" and {len(in_neighbors) - 10} more" if len(in_neighbors) > 10 else "") + "\n\n"
            entity_info += f"Calls: {', '.join(out_neighbors[:10])}" + (f" and {len(out_neighbors) - 10} more" if len(out_neighbors) > 10 else "")
            
            main_doc = Document(
                page_content=entity_info,
                metadata={
                    "entity_name": main_entity,
                    "filepath": self._nx_graph.nodes[main_entity].get("filepath", "unknown"),
                    "source": f"graph_entity_{main_entity}",
                    "in_neighbors": len(in_neighbors),
                    "out_neighbors": len(out_neighbors),
                    "is_graph_rag": True,
                    "entity_type": "function"
                }
            )
            entity_docs.append(main_doc)
            
            # Also get base results focused on this entity
            # Modify the query to focus on the entity
            entity_focused_query = f"{entity_name} {query}"
            base_docs = await self.base_retriever.ainvoke(entity_focused_query)
            
            # Combine entity docs with base docs (prioritize entity docs)
            return entity_docs + base_docs
            
        except Exception as e:
            logger.error(f"Error in local search: {e}")
            if self.base_retriever:
                return await self.base_retriever.ainvoke(query)
            return []
    
    async def _drift_search(self, query: str, entity_name: Optional[str] = None) -> List[Document]:
        """Perform a drift search that combines local search with community context."""
        if not self._detect_communities() or not self._communities:
            logger.warning("Communities not available, falling back to local search")
            return await self._local_search(query, entity_name)
            
        try:
            # First get local search results
            local_docs = await self._local_search(query, entity_name)
            
            # If no local results, return empty list
            if not local_docs:
                return []
                
            # Extract entity from the first document
            main_entity = local_docs[0].metadata.get("entity_name", entity_name)
            if not main_entity:
                return local_docs  # No entity found, return local results
                
            # Find which community this entity belongs to
            entity_community = None
            for i, community in enumerate(self._communities):
                if main_entity in community:
                    entity_community = i
                    break
            
            if entity_community is None:
                return local_docs  # Entity not in any community, return local results
                
            # Get community summary
            if not await self._generate_community_summaries() or entity_community not in self._community_summaries:
                return local_docs  # No community summary, return local results
                
            # Create document with community context
            community = self._communities[entity_community]
            summary = self._community_summaries[entity_community]
            
            community_doc = Document(
                page_content=f"Community Context for {main_entity}:\n{summary}\n\nRelated functions in same community: " + 
                           f"{', '.join([f for f in community[:7] if f != main_entity])}" + 
                           (f" and {len(community) - 7} more" if len(community) > 7 else ""),
                metadata={
                    "community_id": entity_community,
                    "source": f"graph_community_{entity_community}",
                    "function_count": len(community),
                    "summary_type": "entity_community",
                    "entity_name": main_entity,
                    "is_graph_rag": True
                }
            )
            
            # Insert community doc at the beginning
            enhanced_docs = [community_doc] + local_docs
            
            return enhanced_docs
            
        except Exception as e:
            logger.error(f"Error in drift search: {e}")
            if self.base_retriever:
                return await self._local_search(query, entity_name)
            return []
    
    async def _generate_community_summaries(self):
        """Generate summaries for each community in the graph using LLMs."""
        if self._community_summaries is not None:
            return True  # Summaries already generated
            
        if not self._detect_communities() or not self._communities:
            return False  # Community detection failed
            
        try:
            # Initialize summaries dictionary
            self._community_summaries = {}
            
            # For each community, generate a summary
            for i, community in enumerate(self._communities):
                # Skip communities that are too small
                if len(community) < 3:
                    continue
                    
                # Generate a summary of this community
                summary = await self._generate_summary_for_community(community, i)
                if summary:
                    self._community_summaries[i] = summary
            
            logger.info(f"Generated summaries for {len(self._community_summaries)} communities")
            return True
            
        except Exception as e:
            logger.error(f"Error generating community summaries: {e}")
            return False
    
    async def _generate_summary_for_community(self, community: List[str], community_id: int) -> Optional[str]:
        """Generate an LLM-based summary for a community of entities.
        
        Args:
            community: List of entity IDs in the community
            community_id: ID of the community
            
        Returns:
            A rich summary of the community
        """
        from llm import llm_generate
        
        if not community or not self._nx_graph:
            return None
            
        # Get all nodes in the community
        nodes = [node_id for node_id in community if node_id in self._nx_graph.nodes]
        
        if not nodes:
            return None
            
        # Extract entity information
        entities_info = []
        for node_id in nodes:
            node = self._nx_graph.nodes[node_id]
            
            # Get relationships (outgoing edges)
            relationships = []
            for neighbor in self._nx_graph.neighbors(node_id):
                if neighbor in nodes:  # Only include relationships within the community
                    edge = self._nx_graph.edges[node_id, neighbor]
                    rel_type = edge.get("type", "relates_to")
                    rel_desc = edge.get("description", "")
                    
                    relationships.append({
                        "target": neighbor,
                        "type": rel_type,
                        "description": rel_desc
                    })
            
            # Create entity info
            entities_info.append({
                "id": node_id,
                "name": node.get("name", node_id),
                "type": node.get("type", "entity"),
                "description": node.get("description", ""),
                "claims": node.get("claims", []),
                "relationships": relationships
            })
        
        # Create prompt for summary generation
        prompt = f"""
        System: You are a knowledge graph summarization expert. Your task is to generate a comprehensive summary of a community of related entities.
        
        Analyze the entities, their descriptions, claims, and relationships, then provide:
        1. A concise title for this community (one short phrase)
        2. A comprehensive summary that explains what these entities are and how they relate to each other
        3. Key insights about this community
        
        Your summary should be detailed yet concise, focusing on the most important patterns and relationships.
        
        Community ID: {community_id}
        Number of entities: {len(entities_info)}
        
        Here is the community of entities:
        {json.dumps(entities_info, indent=2)}
        
        User: Please summarize this community of entities.
        
        Assistant:
        """
        
        try:
            # Generate summary
            summary = await llm_generate(prompt, temperature=0.3)
            
            if summary:
                logger.info(f"Generated summary for community {community_id} with {len(entities_info)} entities")
                return summary
            else:
                logger.warning(f"Failed to generate summary for community {community_id}")
                return None
                
        except Exception as e:
            logger.error(f"Error generating summary for community {community_id}: {str(e)}")
            
            # Fallback to a basic summary
            entity_types = [info["type"] for info in entities_info]
            most_common_type = max(set(entity_types), key=entity_types.count)
            
            # Create a basic summary
            basic_summary = f"Community {community_id}: A group of {len(entities_info)} entities, primarily of type '{most_common_type}'."
            return basic_summary
    
    def _detect_communities(self):
        """Detect communities in the code graph using the Leiden algorithm."""
        if self._communities is not None:
            return True  # Communities already detected
            
        if not self._initialize_graph() or not self._nx_graph:
            return False  # Graph initialization failed
            
        try:
            # First try to use the Leiden algorithm through python-igraph
            import igraph as ig
            import leidenalg
            from cdlib import NodeClustering
            
            # Convert networkx graph to igraph
            edgelist = list(self._nx_graph.edges())
            if not edgelist:
                logger.warning("Graph has no edges, can't detect communities")
                return False
                
            # Create igraph from edge list
            g_ig = ig.Graph.TupleList(edgelist, directed=True)
            
            # Run Leiden algorithm for community detection
            partition = leidenalg.find_partition(g_ig, leidenalg.ModularityVertexPartition)
            
            # Convert results to cdlib format for easier processing
            leiden_communities = NodeClustering(
                communities=[list(g_ig.vs[c]["name"]) for c in partition.membership],
                graph=self._nx_graph,
                method_name="leiden"
            )
            
            # Store communities
            self._communities = leiden_communities.communities
            logger.info(f"Detected {len(self._communities)} communities using Leiden algorithm")
            return True
            
        except ImportError:
            # Fallback to networkx's community detection
            logger.warning("Leiden algorithm not available, falling back to networkx")
            
            try:
                import networkx.algorithms.community as nx_comm
                
                # Use Girvan-Newman algorithm as fallback
                communities = list(nx_comm.girvan_newman(self._nx_graph))
                # Take the partition with a moderate number of communities
                best_partition_idx = min(2, len(communities) - 1)  # Choose a reasonable partition
                self._communities = list(communities[best_partition_idx])
                
                logger.info(f"Detected {len(self._communities)} communities using networkx")
                return True
                
            except Exception as e:
                logger.error(f"Error detecting communities with networkx: {e}")
                return False
        except Exception as e:
            logger.error(f"Error detecting communities: {e}")
            return False
    
    async def regenerate_graph_from_documents(self, documents):
        """Regenerate the knowledge graph using LLM-based extraction from documents.
        
        Args:
            documents: List of documents to process
            
        Returns:
            bool: Whether the operation was successful
        """
        try:
            from knowledge_extractor import extract_knowledge_graph
            
            if not documents:
                logger.warning("No documents provided for graph regeneration")
                return False
                
            logger.info(f"Regenerating graph from {len(documents)} documents")
            
            # Extract knowledge graph from documents
            knowledge_graph = await extract_knowledge_graph(documents)
            
            if not knowledge_graph or not knowledge_graph.get("entities"):
                logger.warning("No entities extracted from documents")
                return False
                
            # Convert to NetworkX graph format
            self._nx_graph = nx.DiGraph()
            
            # Add entities as nodes
            for entity_id, entity in knowledge_graph["entities"].items():
                self._nx_graph.add_node(
                    entity_id,
                    name=entity.get("name", entity_id),
                    type=entity.get("type", "entity"),
                    description=entity.get("description", "")
                )
            
            # Add relationships as edges
            for rel in knowledge_graph["relationships"]:
                source = rel.get("source")
                target = rel.get("target")
                if source and target and self._nx_graph.has_node(source) and self._nx_graph.has_node(target):
                    self._nx_graph.add_edge(
                        source,
                        target,
                        type=rel.get("type", "relates_to"),
                        description=rel.get("description", "")
                    )
            
            # Store claims as node attributes
            for claim in knowledge_graph["claims"]:
                entity_id = claim.get("entity_id")
                claim_text = claim.get("text")
                if entity_id and claim_text and self._nx_graph.has_node(entity_id):
                    if "claims" not in self._nx_graph.nodes[entity_id]:
                        self._nx_graph.nodes[entity_id]["claims"] = []
                    self._nx_graph.nodes[entity_id]["claims"].append(claim_text)
            
            # Store the raw knowledge graph
            self.graph_data = knowledge_graph
            
            # Run community detection
            self._detect_communities()
            
            # Generate community summaries
            await self._generate_community_summaries()
            
            # Store graph data in database if project_id is available
            if self.project_id:
                try:
                    await self._store_graph_in_db()
                except Exception as e:
                    logger.warning(f"Failed to store graph in database: {e}")
            
            logger.info(f"Successfully regenerated graph with {self._nx_graph.number_of_nodes()} nodes and {self._nx_graph.number_of_edges()} edges")
            return True
            
        except Exception as e:
            logger.error(f"Error regenerating graph from documents: {str(e)}")
            return False
    
    async def _store_graph_in_db(self):
        """Store the graph data in the database."""
        if not self.project_id or not self.graph_data:
            return False
            
        try:
            from db import MongoDB
            db = MongoDB()
            
            # Convert NetworkX graph to serializable format
            serializable_graph = {}
            
            # Handle different graph formats
            if isinstance(self.graph_data, dict) and "entities" in self.graph_data:
                # Already in our preferred format
                serializable_graph = self.graph_data
            else:
                # Convert NetworkX graph to our format
                serializable_graph = {
                    "entities": {},
                    "relationships": [],
                    "claims": []
                }
                
                # Add nodes
                for node_id in self._nx_graph.nodes:
                    node_data = self._nx_graph.nodes[node_id]
                    serializable_graph["entities"][node_id] = {
                        "id": node_id,
                        "name": node_data.get("name", node_id),
                        "type": node_data.get("type", "entity"),
                        "description": node_data.get("description", "")
                    }
                    
                    # Add claims
                    if "claims" in node_data:
                        for claim_text in node_data["claims"]:
                            serializable_graph["claims"].append({
                                "entity_id": node_id,
                                "text": claim_text
                            })
                
                # Add edges
                for source, target, edge_data in self._nx_graph.edges(data=True):
                    serializable_graph["relationships"].append({
                        "source": source,
                        "target": target,
                        "type": edge_data.get("type", "relates_to"),
                        "description": edge_data.get("description", "")
                    })
            
            # Store in database
            db.db.graph_data.update_one(
                {"project_id": self.project_id},
                {"$set": {
                    "project_id": self.project_id,
                    "graph_data": serializable_graph,
                    "updated_at": datetime.datetime.utcnow()
                }},
                upsert=True
            )
            
            logger.info(f"Successfully stored graph data for project {self.project_id} in database")
            return True
            
        except Exception as e:
            logger.error(f"Error storing graph data in database: {str(e)}")
            return False
            
    async def regenerate_graph_from_vectorstore(self):
        """Regenerate the graph from the vector store data for this project."""
        if not self.project_id:
            logger.warning("No project ID available for graph regeneration from vector store")
            return False
            
        if not self.base_retriever:
            logger.warning("No base retriever available for graph regeneration from vector store")
            return False
            
        try:
            # Query for a representative sample of documents
            questions = [
                "Provide an overview of the entire system",
                "What are the main components of the codebase?",
                "How does the system architecture work?",
                "What are the core functions and modules?",
                "Explain the data flow in the system"
            ]
            
            all_docs = []
            for question in questions:
                logger.info(f"Retrieving documents for question: {question}")
                if hasattr(self.base_retriever, "get_relevant_documents"):
                    docs = self.base_retriever.get_relevant_documents(question)
                    all_docs.extend(docs)
                elif hasattr(self.base_retriever, "_get_relevant_documents"):
                    docs = await self.base_retriever._get_relevant_documents(question)
                    all_docs.extend(docs)
            
            # Deduplicate documents
            unique_docs = {}
            for doc in all_docs:
                if hasattr(doc, "metadata") and "file_path" in doc.metadata:
                    key = doc.metadata["file_path"]
                else:
                    key = doc.page_content[:100]  # Use first 100 chars as key
                unique_docs[key] = doc
                
            unique_doc_list = list(unique_docs.values())
            
            if not unique_doc_list:
                logger.warning("No documents retrieved from vector store")
                return False
                
            logger.info(f"Retrieved {len(unique_doc_list)} unique documents from vector store")
            
            # Regenerate graph from documents
            return await self.regenerate_graph_from_documents(unique_doc_list)
            
        except Exception as e:
            logger.error(f"Error regenerating graph from vector store: {str(e)}")
            return False


def build_retriever_from_args(args, data_manager: Optional[DataManager] = None):
    """Builds a retriever (with optional reranking) from command-line arguments."""
    if args.llm_retriever:
        retriever = LLMRetriever(GitHubRepoManager.from_args(args), top_k=args.retriever_top_k)
    else:
        if args.embedding_provider == "openai":
            embeddings = OpenAIEmbeddings(model=args.embedding_model)
        elif args.embedding_provider == "voyage":
            embeddings = VoyageAIEmbeddings(model=args.embedding_model)
        elif args.embedding_provider == "gemini":
            embeddings = GoogleGenerativeAIEmbeddings(model=args.embedding_model)
        else:
            embeddings = None

        retriever = build_vector_store_from_args(args, data_manager).as_retriever(
            top_k=args.retriever_top_k, embeddings=embeddings, namespace=args.index_namespace
        )

    if args.multi_query_retriever:
        retriever = MultiQueryRetriever.from_llm(
            retriever=retriever, llm=build_llm_via_langchain(args.llm_provider, args.llm_model)
        )

    reranker = build_reranker(args.reranker_provider, args.reranker_model, args.reranker_top_k)
    if reranker:
        retriever = ContextualCompressionRetriever(base_compressor=reranker, base_retriever=retriever)
        
    # Add GraphRAG enhancement if enabled
    # Check if GraphRAG is enabled explicitly or in project metadata
    use_graph_rag = getattr(args, 'use_graph_rag', False)
    force_regenerate = getattr(args, 'force_regenerate_graph', False)
    
    # If not explicitly enabled, check project metadata from database
    if not use_graph_rag and hasattr(args, 'project_id') and args.project_id:
        try:
            # Use the standalone get_project_metadata function instead of expecting it as a DB method
            project_metadata = get_project_metadata(args.project_id)
            if project_metadata:
                use_graph_rag = project_metadata.get('use_graph_rag', False) or project_metadata.get('graphrag_enabled', False)
                if use_graph_rag:
                    logger.info(f"GraphRAG enabled via project metadata for project {args.project_id}")
        except Exception as e:
            logger.warning(f"Failed to check GraphRAG project metadata: {e}")
    
    # Step 1: Enhance with Nuanced if enabled and available
    nuanced_enabled = hasattr(args, 'use_nuanced') and args.use_nuanced 
    if not nuanced_enabled and hasattr(args, 'project_id') and args.project_id:
        try:
            # Use the standalone get_project_metadata function
            project_metadata = get_project_metadata(args.project_id)
            if project_metadata:
                nuanced_enabled = project_metadata.get('use_nuanced', False) or project_metadata.get('nuanced_enabled', False)
                if nuanced_enabled:
                    logger.info(f"Nuanced enabled via project metadata for project {args.project_id}")
        except Exception as e:
            logger.warning(f"Failed to check Nuanced project metadata: {e}")
            
    if nuanced_enabled and hasattr(args, 'local_dir'):
        try:
            from services.nuanced_service import NuancedService
            if NuancedService.is_installed():
                # If GraphRAG is also enabled, we'll create a graph from Nuanced data later
                if not use_graph_rag:
                    # Only add Nuanced enhancement if GraphRAG isn't going to be used
                    retriever = NuancedEnhancedRetriever(retriever, args.local_dir)
                    logger.info("Enhanced retriever with Nuanced call graph data")
        except ImportError:
            logger.warning("Nuanced service not available, skipping retriever enhancement")
        except Exception as e:
            logger.warning(f"Error enhancing retriever with Nuanced: {str(e)}")
    
    # Step 2: Enhance with GraphRAG if enabled
    if use_graph_rag:
        try:
            logger.info("Initializing GraphRAG retriever...")
            
            # Set project ID either from args or extract from repo path
            project_id = getattr(args, 'project_id', None)
            
            # Get graph_data if we have it in args or from DB
            graph_data = getattr(args, 'graph_data', None)
            
            # Check for local repo path (either from args or typical locations)
            local_dir = getattr(args, 'local_dir', "")
            if not os.path.exists(local_dir) and project_id:
                # Check common locations where a persistent copy might exist
                potential_paths = [
                    f"/tmp/my_local_repo_{project_id}",
                    f"/tmp/nia_repo_{project_id}",
                    f"/tmp/nuanced_regen_{project_id}"
                ]
                
                for path in potential_paths:
                    if os.path.exists(path):
                        logger.info(f"Found alternative local repo path: {path}")
                        local_dir = path
                        break
            
            # If not found in common locations, try to get path from project metadata
            if not os.path.exists(local_dir) and project_id:
                try:
                    from db import MongoDB
                    db = MongoDB()
                    project_metadata = db.get_project_metadata(project_id)
                    if project_metadata and "graphrag_repo_path" in project_metadata:
                        repo_path = project_metadata["graphrag_repo_path"]
                        if os.path.exists(repo_path):
                            logger.info(f"Using GraphRAG repository path from metadata: {repo_path}")
                            local_dir = repo_path
                except Exception as e:
                    logger.warning(f"Failed to get GraphRAG repo path from metadata: {e}")
            
            # If still not found, try to get graph data from DB
            if not graph_data and project_id and not force_regenerate:
                try:
                    from services.nuanced_service import NuancedService
                    logger.info(f"Attempting to get graph data from database for project {project_id}")
                    graph_data = NuancedService.get_graph_from_db(project_id)
                    if graph_data:
                        logger.info(f"Successfully retrieved graph data from database for project {project_id}")
                except Exception as e:
                    logger.warning(f"Failed to get graph data from database: {e}")
            
            # Determine query mode for GraphRAG (auto by default)
            query_mode = getattr(args, 'graph_query_mode', "auto")
            
            # Log detailed information about GraphRAG initialization
            logger.info(f"GraphRAG Configuration:")
            logger.info(f"- Project ID: {project_id}")
            logger.info(f"- Local Directory: {local_dir} (exists: {os.path.exists(local_dir)})")
            logger.info(f"- Graph Data Available: {graph_data is not None}")
            logger.info(f"- Query Mode: {query_mode}")
            logger.info(f"- Force Regenerate: {force_regenerate}")
            
            # Initialize the GraphRAG retriever with all available data
            graphrag_retriever = GraphRAGRetriever(
                base_retriever=retriever,
                repo_path=local_dir,
                project_id=project_id,
                graph_data=None if force_regenerate else graph_data,  # Set to None if forcing regeneration
                query_mode=query_mode
            )
            
            # If forcing regeneration, regenerate the graph using LLM-based extraction
            if force_regenerate and project_id:
                logger.info("Force regenerating graph using LLM-based extraction...")
                loop = asyncio.get_event_loop()
                loop.run_until_complete(graphrag_retriever.regenerate_graph_from_vectorstore())
            
            retriever = graphrag_retriever
            logger.info("Successfully initialized GraphRAG retriever")
            
        except Exception as e:
            logger.error(f"Error initializing GraphRAG retriever: {str(e)}")
            logger.info("Falling back to base retriever")
    
    # Add error handling wrapper for reranker
    if reranker:
        retriever = RerankerWithErrorHandling(retriever)

    return retriever


# Add a helper function to get project metadata for retrieval
def get_project_metadata(project_id: str) -> Optional[Dict]:
    """Get project metadata from the database to check for GraphRAG and Nuanced settings.
    
    Args:
        project_id: The project ID to get metadata for
        
    Returns:
        Dict containing project metadata if available, None otherwise
    """
    try:
        from db import MongoDB
        db = MongoDB()
        
        # Get project from database
        project = db.db.projects.find_one({"project_id": project_id})
        if not project:
            return None
            
        # Return project metadata if available
        metadata = {}
        
        # Check for use_* flags
        for flag in ["use_nuanced", "use_graph_rag", "nuanced_enabled", "graph_rag_enabled", 
                    "graphrag_enabled", "graphrag_repo_path"]:
            if flag in project:
                metadata[flag] = project[flag]
                
        # Add any metadata in the details field
        if "details" in project and isinstance(project["details"], dict):
            for flag in ["use_nuanced", "use_graph_rag", "nuanced_enabled", "graph_rag_enabled", 
                        "graphrag_enabled", "graphrag_repo_path"]:
                if flag in project["details"]:
                    metadata[flag] = project["details"][flag]
        
        return metadata
    except Exception as e:
        logger.warning(f"Failed to get project metadata from database: {e}")
        return None

async def build_combined_retriever(project_retriever, user_id: Optional[str] = None, db: Optional['MongoDB'] = None):
    """
    Builds a combined retriever that includes all active data sources 
    along with the project-specific retriever.
    
    Args:
        project_retriever: The base retriever for project-specific data
        user_id: The ID of the user to filter data sources by (for data isolation)
        db: MongoDB instance (if None, a new one will be created)
        
    Returns:
        A combined retriever that searches across all relevant sources
    """
    logger = logging.getLogger(__name__)
    
    # Initialize MongoDB if not provided
    if db is None:
        db = MongoDB()
    
    try:
        # Get all active data sources - using synchronous method
        active_sources = db.get_active_data_sources(user_id)
        
        if not active_sources:
            logger.info("No active data sources found, using only project retriever")
            return project_retriever
        
        # Create retrievers for each active source
        source_retrievers = []
        for source in active_sources:
            try:
                # Skip sources that aren't completed
                if source.get("status") != "completed":
                    logger.info(f"Skipping incomplete source: {source.get('url')} (status: {source.get('status')})")
                    continue
                    
                # Log clear information about the source being added
                logger.info(f"Adding active external source to retrieval: {source.get('url')}")
                
                # Build vector store retriever for this source
                # Using the source's namespace/ID for isolation
                vector_store = build_vector_store_from_args(
                    SimpleNamespace(
                        index_name="web-sources",  # Use dedicated web-sources index
                        index_namespace=f"web-sources_{source.get('user_id', 'unknown')}_{source['id']}",
                        retriever_top_k=3  # Smaller value for each source
                    )
                )
                
                # Log the retrieval configuration
                logger.info(f"Using dedicated web-sources index with namespace: web-sources_{source.get('user_id', 'unknown')}_{source['id']}")
                
                try:
                    source_retriever = vector_store.as_retriever()
                    
                    # Try to get doc count to verify the source is accessible
                    docs = source_retriever.get_relevant_documents("test query")
                    logger.info(f"Successfully connected to source, found {len(docs)} docs for test query")
                except Exception as e:
                    # Try the fallback namespace as well
                    logger.warning(f"Failed to access source with new namespace format: {e}")
                    logger.info(f"Trying fallback to old namespace format: source_{source['id']}")
                    
                    try:
                        fallback_vector_store = build_vector_store_from_args(
                            SimpleNamespace(
                                index_name="nia-app",  # Old index
                                index_namespace=f"source_{source['id']}",
                                retriever_top_k=3
                            )
                        )
                        source_retriever = fallback_vector_store.as_retriever()
                    except Exception as fallback_error:
                        logger.error(f"Failed to access source even with fallback: {fallback_error}")
                        continue  # Skip this source
                
                # Wrap the retriever to add source identification
                class EnhancedRetriever(BaseRetriever):
                    def _get_relevant_documents(self, query, *, run_manager=None):
                        docs = source_retriever._get_relevant_documents(query, run_manager=run_manager)
                        # Add source metadata to each document
                        for doc in docs:
                            if not doc.metadata:
                                doc.metadata = {}
                            doc.metadata["external_source"] = "true"
                            doc.metadata["source_url"] = source.get("url", "unknown")
                            doc.metadata["source_id"] = source["id"]
                            # Set file_path to a clearly identifiable format for display
                            doc.metadata["file_path"] = f"EXTERNAL:{source.get('url', 'unknown')}"
                        return docs
                
                source_retrievers.append(EnhancedRetriever())
                logger.info(f"Added retriever for source: {source['url']} with {source.get('page_count', 0)} pages")
            except Exception as e:
                logger.error(f"Error creating retriever for source {source.get('id')}: {e}")
        
        if not source_retrievers:
            logger.info("No valid source retrievers created, using only project retriever")
            return project_retriever
        
        # Create ensemble retriever with weights
        # Give more weight to project data (0.7) vs external sources (0.3 distributed among sources)
        source_weight = 0.3 / len(source_retrievers)
        weights = [0.7] + [source_weight] * len(source_retrievers)
        
        ensemble = EnsembleRetriever(
            retrievers=[project_retriever] + source_retrievers,
            weights=weights
        )
        
        logger.info(f"Built combined retriever with {len(source_retrievers)} additional sources")
        return ensemble
    except Exception as e:
        logger.error(f"Error building combined retriever: {e}")
        # Fall back to project retriever on error
        return project_retriever