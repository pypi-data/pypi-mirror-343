import os
import logging
import asyncio
import traceback
from typing import List, Dict, Any, Tuple, Optional
from uuid import UUID

from langchain_openai import OpenAIEmbeddings, ChatOpenAI
from langchain.retrievers import MultiQueryRetriever, ContextualCompressionRetriever

from data_manager import GitHubRepoManager
from retriever import LLMRetriever
from vector_store import PineconeVectorStore
from reranker import build_reranker, RerankerProvider

from .validation_utils import validate_safe_path

def build_advanced_retriever(local_dir: str, top_k: int = 10) -> LLMRetriever:
    """
    Build an LLMRetriever from a local GitHub repo.
    Includes secure path validation to prevent LFI.
    
    Args:
        local_dir: Path to the local repository directory
        top_k: Number of top documents to retrieve
        
    Returns:
        LLMRetriever instance configured for the repository
        
    Raises:
        ValueError: If the repository path is invalid or not found
    """
    # Validate the local directory path
    base_tmp_dir = "/tmp"
    is_valid, safe_path, error = validate_safe_path(base_tmp_dir, local_dir)
    if not is_valid:
        raise ValueError(f"Invalid repository path: {error}")
        
    if not os.path.exists(safe_path):
        raise ValueError(f"Local repo directory {safe_path} not found")
        
    # Use the validated path
    repo_manager = GitHubRepoManager(local_dir=safe_path, repo_id="placeholder/placeholder")
    return LLMRetriever(repo_manager=repo_manager, top_k=top_k)

def is_call_relationship_query(query: str) -> bool:
    """
    Enhanced detector for queries about function call relationships in code.
    
    Uses a combination of embedding similarity and prompt classification with LLM
    to better understand the semantic intent of the query.
    
    Args:
        query: The user query string
        
    Returns:
        True if the query appears to be about call relationships
    """
    import os
    import asyncio
    import numpy as np
    from functools import lru_cache
    
    # 1. First try a fast embedding-based approach to avoid unnecessary LLM calls
    @lru_cache(maxsize=128)
    def get_call_relationship_embeddings():
        """Create embeddings for common call relationship queries."""
        try:
            from langchain_openai import OpenAIEmbeddings
            
            # Representative examples of call relationship queries
            call_relationship_examples = [
                "Which functions call the main() function?",
                "Show me the function call graph",
                "How are functions connected in this codebase?",
                "What's the call hierarchy in this module?",
                "Who calls this method?",
                "Trace the execution flow",
                "What functions depend on this one?",
                "Count the number of function calls",
                "List all function relationships",
                "How many functions are called by this one?",
                "Which parts of the code use this function?",
                "Show the call dependencies"
            ]
            
            # Create embeddings for the examples
            try:
                # Use smallest embedding model for speed and cost efficiency
                embeddings_model = OpenAIEmbeddings(
                    model="text-embedding-3-small", 
                    openai_api_key=os.getenv("OPENAI_API_KEY")
                )
                
                # Get embeddings for all examples
                embeds = embeddings_model.embed_documents(call_relationship_examples)
                
                # Calculate the mean embedding to use as a reference
                mean_embedding = np.mean(embeds, axis=0)
                return mean_embedding, embeddings_model
                
            except Exception as e:
                logging.warning(f"Error creating embeddings: {e}")
                return None, None
                
        except ImportError:
            logging.warning("OpenAI embeddings not available, falling back to regex")
            return None, None
    
    # Fast path: first try regex for common obvious patterns
    import re
    query_lower = query.lower()
    
    # Check for obvious patterns that are clear indicators
    obvious_patterns = [
        r"call\s+graph",
        r"call\s+relationships?",
        r"who\s+calls",
        r"called\s+by",
        r"function\s+dependencies",
        r"call\s+hierarchy",
        r"execution\s+flow"
    ]
    
    for pattern in obvious_patterns:
        if re.search(pattern, query_lower):
            logging.info(f"✅ Detected obvious call relationship query via regex: '{query}'")
            return True
    
    # Try embedding similarity approach if OpenAI API is available
    mean_embedding, embeddings_model = get_call_relationship_embeddings()
    
    if mean_embedding is not None and embeddings_model is not None:
        try:
            # Get embedding for the current query
            query_embedding = embeddings_model.embed_query(query)
            
            # Calculate cosine similarity with the mean embedding
            similarity = np.dot(mean_embedding, query_embedding) / (
                np.linalg.norm(mean_embedding) * np.linalg.norm(query_embedding)
            )
            
            # Set a threshold for considering it a call relationship query
            SIMILARITY_THRESHOLD = 0.78  # Adjusted based on empirical testing
            
            if similarity >= SIMILARITY_THRESHOLD:
                logging.info(f"✅ Detected call relationship query via embedding similarity: '{query}' (score: {similarity:.3f})")
                return True
                
            # For borderline cases, use LLM classification
            if similarity >= 0.6:  # Borderline cases
                return classify_with_llm(query)
                
        except Exception as e:
            logging.warning(f"Error in embedding comparison: {e}")
            # Fall back to LLM classification
            return classify_with_llm(query)
    else:
        # If embeddings are not available, fall back to LLM classification
        return classify_with_llm(query)
    
    return False

def classify_with_llm(query: str) -> bool:
    """
    Classify a query as call relationship related using LLM.
    This provides more accurate semantic understanding compared to regex.
    
    Args:
        query: The query to classify
        
    Returns:
        True if the query is about call relationships
    """
    try:
        import os
        from langchain_openai import ChatOpenAI
        from langchain_core.messages import HumanMessage, SystemMessage
        
        # Only use LLM if API key is available
        openai_api_key = os.getenv("OPENAI_API_KEY")
        if not openai_api_key:
            logging.warning("OpenAI API key not available for LLM classification")
            return fallback_regex_classification(query)
        
        # Use GPT-3.5 for cost efficiency as this is just classification
        llm = ChatOpenAI(
            model="gpt-3.5-turbo-0125",
            temperature=0,
            openai_api_key=openai_api_key
        )
        
        system_prompt = """
        You are a query classifier for code analysis. Your task is to determine if a user's query is asking about function call relationships in code.
        
        Function call relationship queries include:
        - Questions about which functions call other functions
        - Requests to show call graphs or hierarchies
        - Questions about dependencies between functions
        - Inquiries about execution flow or call stacks
        - Questions about how functions interact with each other
        - Requests for counting or statistics about function calls
        
        Respond with ONLY "Yes" if the query is about function call relationships, or "No" if it is not.
        """
        
        # Create the message
        messages = [
            SystemMessage(content=system_prompt),
            HumanMessage(content=f"Query: {query}\n\nIs this query about function call relationships?")
        ]
        
        # Get response from LLM
        response = llm.invoke(messages)
        
        # Process response
        result_text = response.content.strip().lower()
        is_relationship_query = "yes" in result_text
        
        if is_relationship_query:
            logging.info(f"✅ Detected call relationship query via LLM classification: '{query}'")
        
        return is_relationship_query
        
    except Exception as e:
        logging.warning(f"Error in LLM classification: {e}")
        # Fall back to regex as a last resort
        return fallback_regex_classification(query)

def fallback_regex_classification(query: str) -> bool:
    """
    Legacy regex-based classification as a fallback method.
    
    Args:
        query: The query to classify
        
    Returns:
        True if the query is about call relationships
    """
    import re
    
    # Convert to lowercase for case-insensitive matching
    query_lower = query.lower()
    
    # Keywords and phrases that indicate relationship queries
    call_relationship_keywords = [
        r"calls?\s+(what|which)",
        r"(what|which)\s+functions?\s+(call|calls|invokes)",
        r"(what|which)\s+methods?\s+(call|calls|invoke)",
        r"called\s+by",
        r"invoked\s+by",
        r"call\s+relationships?",
        r"call\s+graph",
        r"function\s+relationships?",
        r"method\s+relationships?",
        r"execution\s+flow",
        r"call\s+hierarchy",
        r"calls?\s+tree",
        r"who\s+calls",
        r"function\s+dependencies",
        r"method\s+dependencies",
        r"how\s+many\s+(calls|call\s+relationships)",
        r"count\s+of\s+(calls|call\s+relationships)",
        r"total\s+(calls|call\s+relationships)",
        r"number\s+of\s+(calls|call\s+relationships)",
        r"call\s+stack",
        r"functions?\s+interaction"
    ]
    
    # Check for keyword presence
    for pattern in call_relationship_keywords:
        if re.search(pattern, query_lower):
            logging.info(f"✅ Detected call relationship query via regex fallback: '{query}' (matched pattern: '{pattern}')")
            return True
    
    # Check for more advanced patterns
    advanced_patterns = [
        r"how\s+(does|do)\s+.+\s+(function|method)\s+.+\s+(work|interact)",
        r"what\s+happens\s+when\s+.+\s+(calls?|invokes?)",
        r"show\s+me\s+.+\s+call\s+.+\s+relationships",
        r"list\s+(all|the)\s+functions\s+that\s+.*call",
        r"which\s+parts\s+of\s+the\s+code\s+(use|call|depend\s+on)",
        r"relationship\s+between\s+.+\s+functions",
        r"how\s+are\s+functions\s+.+\s+connected",
        r"which\s+function\s+is\s+called\s+by",
        r"is\s+.+\s+called\s+by\s+.+",
        r"does\s+.+\s+call\s+.+"
    ]
    
    for pattern in advanced_patterns:
        if re.search(pattern, query_lower):
            logging.info(f"✅ Detected advanced call relationship query via regex fallback: '{query}' (matched pattern: '{pattern}')")
            return True
    
    # Specific checks for counting/statistics questions
    counting_patterns = [
        r"how\s+many",
        r"count\s+of",
        r"total\s+number\s+of",
        r"number\s+of"
    ]
    
    relationship_terms = [
        r"relationships?",
        r"connections?",
        r"dependencies",
        r"calls?",
        r"invocations?"
    ]
    
    # Check combinations of counting patterns and relationship terms
    for count_pattern in counting_patterns:
        for rel_term in relationship_terms:
            combined_pattern = f"{count_pattern}.*{rel_term}"
            if re.search(combined_pattern, query_lower):
                logging.info(f"✅ Detected statistical call relationship query via regex fallback: '{query}' (matched pattern: '{combined_pattern}')")
                return True
    
    return False

def generate_nuanced_insight(call_graph_data: Dict, filename: str) -> Optional[str]:
    """
    Use LLM to generate higher-level insights about function relationships.
    
    This synchronous approach uses LLM to analyze complex call graphs and extract
    architectural patterns, potential optimizations, and functional insights.
    
    Args:
        call_graph_data: The call graph data from Nuanced
        filename: Name of the file for context
        
    Returns:
        String with insights or None if generation failed
    """
    try:
        import os
        import json
        from langchain_openai import ChatOpenAI
        from langchain_core.messages import HumanMessage, SystemMessage
        
        # Only attempt this if we have an API key and enough data
        openai_api_key = os.getenv("OPENAI_API_KEY")
        if not openai_api_key:
            logging.debug("OpenAI API key not available for insight generation")
            return None
            
        # Only generate insights for sufficiently complex graphs
        function_count = len(call_graph_data)
        relationship_count = 0
        
        # Count relationships
        for func_name, graph_data in call_graph_data.items():
            for qualified_name, func_info in graph_data.items():
                relationship_count += len(func_info.get("callees", []))
        
        # Skip if not enough data for meaningful analysis
        if function_count < 7 or relationship_count < 10:
            logging.debug(f"Not enough data for insight generation: {function_count} functions, {relationship_count} relationships")
            return None
            
        # Prepare call graph data
        simplified_graph = {}
        for func_name, graph_data in call_graph_data.items():
            callees = []
            for qualified_name, func_info in graph_data.items():
                callees.extend(func_info.get("callees", []))
            
            # Only include functions with relationships
            if callees:
                simplified_graph[func_name] = sorted(callees)
        
        # Create the prompt
        system_prompt = """
        You are a code architecture expert analyzing function call relationships.
        Examine the provided function call graph and generate insights about:
        
        1. Architectural patterns (like MVC, observer, command pattern)
        2. Potential optimizations (like refactoring opportunities)
        3. Key entry points and their purposes
        4. Functional groupings and their responsibilities
        
        IMPORTANT: Focus ONLY on the structural relationships between functions.
        DO NOT make assumptions about what the functions actually do based on their names.
        Limit your analysis to what can be inferred from the call graph structure alone.
        
        Keep your response concise, under 200 words, formatted in markdown.
        """
        
        # Format the function call data
        graph_summary = f"# Call Graph from {filename}\n\n"
        for func, callees in simplified_graph.items():
            if callees:
                graph_summary += f"- `{func}` calls: {', '.join(['`'+c+'`' for c in callees])}\n"
        
        # Add statistics
        graph_summary += f"\n**Statistics**: {function_count} functions, {relationship_count} call relationships"
        
        # Create messages
        messages = [
            SystemMessage(content=system_prompt),
            HumanMessage(content=graph_summary)
        ]
        
        # Use GPT-4 for best quality insights
        llm = ChatOpenAI(
            model="gpt-4.1-2025-04-14",  # Use fastest GPT-4 variant
            temperature=0.2,  # Low temperature for more factual/analytical response
            openai_api_key=openai_api_key
        )
        
        # Get response (ensure we're not using async here)
        response = llm.invoke(messages)
        insights = response.content.strip()
        
        if insights:
            # Format the final output
            formatted_insights = "\n\n## AI-Generated Code Architecture Insights\n\n"
            formatted_insights += insights
            formatted_insights += "\n\n"
            
            logging.info(f"Generated {len(insights)} chars of architectural insights for {filename}")
            return formatted_insights
            
        return None
        
    except Exception as e:
        logging.warning(f"Error generating call graph insights: {e}")
        return None
        
        
# Async wrapper around the synchronous version for backward compatibility
async def generate_nuanced_insight_async(call_graph_data: Dict, filename: str) -> Optional[str]:
    """
    Async wrapper around the synchronous insight generator.
    This wrapper helps avoid the "event loop already running" error by ensuring
    the LLM call happens in a way that doesn't conflict with the existing event loop.
    
    Args:
        call_graph_data: The call graph data from Nuanced
        filename: Name of the file for context
        
    Returns:
        String with insights or None if generation failed
    """
    import asyncio
    import concurrent.futures
    try:
        # Use thread pool to run synchronous function without blocking the event loop
        with concurrent.futures.ThreadPoolExecutor() as pool:
            return await asyncio.get_event_loop().run_in_executor(
                pool, generate_nuanced_insight, call_graph_data, filename
            )
    except RuntimeError as e:
        if "this event loop is already running" in str(e):
            logging.warning("Error in async insight generation: this event loop is already running.")
            # Fall back to synchronous version directly in this case
            return generate_nuanced_insight(call_graph_data, filename)
        else:
            logging.warning(f"Error in async insight generation: {e}")
            return None

# Function to generate multi-queries 
async def generate_multi_queries(query: str):
    """Generate alternative queries for more comprehensive search.
    
    Args:
        query: The original user query
        
    Returns:
        List of alternative query strings
    """
    try:
        # Use GPT-4 for better query understanding
        from langchain_openai import ChatOpenAI
        
        llm = ChatOpenAI(
            model="gpt-4.1-2025-04-14",
            temperature=0.0
        )
        
        from langchain_core.prompts import ChatPromptTemplate
        
        # Create a prompt to generate alternative queries
        query_prompt = ChatPromptTemplate.from_messages([
            ("system", """You are an AI language model assistant that helps to create alternative search queries based on the initial query. 
            Your task is to create different versions of the given query to help retrieve more relevant information.
            
            Given the original query, generate 3 alternative versions of the query that could help to find more relevant information.
            Each query should be on a separate line without any numbering or explanation."""),
            ("human", "{query}")
        ])
        
        # Direct LLM call to generate alternative queries
        query_response = await llm.ainvoke(
            query_prompt.format(query=query)
        )
        
        # Extract the generated queries
        generated_queries = [
            line.strip() for line in query_response.content.split("\n") 
            if line.strip() and not line.strip().startswith(("1.", "2.", "3.", "-", "•"))
        ]
        
        # Add original query if we have room
        if len(generated_queries) < 3:
            generated_queries.append(query)
            
        # Limit to at most 3 queries
        generated_queries = generated_queries[:3]
        
        logging.info(f"Generated alternative queries: {generated_queries}")
        return generated_queries
    except Exception as e:
        logging.error(f"Error generating alternative queries: {e}")
        logging.error(f"Traceback: {traceback.format_exc()}")
        return [query]  # Fall back to just the original query

async def fallback_pinecone_retrieval(
    prompt: str, 
    project_configs: List[dict],
    use_nuanced: bool = False,
    include_external_sources: bool = True,  # Parameter to control external sources
    user_id: Optional[str] = None,  # New parameter for user filtering
    use_graph_rag: bool = False,    # Enable GraphRAG for enhanced retrieval
    graph_query_mode: str = "auto",  # GraphRAG query mode (auto, global, local, drift)
    skip_validation: bool = False   # Skip validation agent step (to prevent recursion)
) -> Tuple[List[Any], List[str], List[str]]:
    """
    Fallback retrieval using Pinecone when other retrievers fail.
    
    Args:
        prompt: The user query
        project_configs: List of project configurations
        use_nuanced: Whether to use Nuanced data
        include_external_sources: Whether to include external data sources
        user_id: User ID for filtering data sources (for data isolation)
        use_graph_rag: Whether to use GraphRAG for enhanced retrieval
        graph_query_mode: GraphRAG query mode (auto, global, local, drift)
        
    Returns:
        Tuple of (documents, contexts, source_names)
    """
    max_retries = 3
    retry_delay = 2  # seconds
    
    # Auto-enable Nuanced for call relationship queries
    if is_call_relationship_query(prompt) and not use_nuanced and not use_graph_rag:
        logging.info("🔍 AUTOMATICALLY ENABLING NUANCED for call relationship query")
        use_nuanced = True
        
    # When GraphRAG is enabled, it takes precedence over Nuanced
    if use_graph_rag:
        logging.info("")
        logging.info("🔍 GRAPH RAG ENHANCEMENT REQUESTED")
        logging.info(f"Query mode: {graph_query_mode}")
        # GraphRAG will handle Nuanced data internally, so we don't need both
        use_nuanced = False
    # Debug log for Nuanced usage
    elif use_nuanced:
        logging.info("")
        logging.info("🔍 NUANCED ENHANCEMENT REQUESTED for retrieval")
        try:
            # Import here to avoid import errors if Nuanced isn't installed
            from services.nuanced_service import NuancedService
            # Generate detailed debug logs
            NuancedService.debug_logs()
        except Exception as e:
            logging.error(f"Error generating Nuanced debug logs: {str(e)}")
    
    for attempt in range(max_retries):
        try:
            openai_api_key = os.getenv("OPENAI_API_KEY")
            # Use text-embedding-3-small as it performs best according to research
            embeddings = OpenAIEmbeddings(
                model="text-embedding-3-small",
                openai_api_key=openai_api_key,
                chunk_size=800  # Optimal chunk size from research
            )

            # Query each project namespace and combine results
            all_docs = []
            all_contexts = []
            all_sources = []
            
            # Get MongoDB instance for data sources access
            # Don't import db globally - use MongoDB class directly
            from db import MongoDB
            db_instance = MongoDB()
            
            for config in project_configs:
                # Get index and namespace based on project config
                index_name = config["index_name"]
                retrieval_user_id = config["user_id"]
                project_id = config["project_id"]
                
                logging.info(f"Using Pinecone index: {index_name} for project {project_id} (community: {config['is_community']})")
                
                store = PineconeVectorStore(
                    index_name=index_name,
                    dimension=1536,
                    alpha=1.0  # Pure dense retrieval, no hybrid/sparse as per research
                )
                
                # Always use user_id/project_id format for namespace
                namespace = f"{retrieval_user_id}/{project_id}"
                logging.info(f"Using namespace: {namespace}")
                
                # Build base retriever for this project
                base_retriever = store.as_retriever(
                    top_k=25,  # Optimal from research
                    embeddings=embeddings,
                    namespace=namespace
                )
                
                # Also fetch associated data sources if enabled
                external_source_docs = []
                if include_external_sources:
                    try:
                        # Get associated data source IDs for this project
                        source_ids = db_instance.get_associated_data_sources(project_id)
                        if source_ids:
                            logging.info(f"Found {len(source_ids)} external data sources for project {project_id}")
                            
                            # Get data source details
                            for source_id in source_ids:
                                # Get the data source details
                                data_source = db_instance.get_data_source_by_id(source_id)
                                if data_source and data_source.get("status") == "completed":
                                    # Verify the user has access to this data source
                                    source_user_id = data_source.get("user_id")
                                    current_user_id = config["user_id"]
                                    
                                    # Skip sources that don't belong to this user for proper isolation
                                    if source_user_id and source_user_id != current_user_id:
                                        logging.info(f"🔒 PRIVACY: Skipping project source {source_id} as it belongs to user {source_user_id}, not current user {current_user_id}")
                                        continue
                                    
                                    # Use the new dedicated namespace format for web sources
                                    primary_namespace = f"web-sources_{current_user_id}_{source_id}"
                                    # Keep old format for backward compatibility
                                    fallback_namespace = f"web_{project_id}_{source_id}"
                                    
                                    logging.info(f"Adding external data source: {data_source.get('url')}")
                                    logging.info(f"Using namespaces: primary={primary_namespace}, fallback={fallback_namespace}")
                                    
                                    # Try primary namespace first
                                    try:
                                        web_retriever = store.as_retriever(
                                            top_k=10,
                                            embeddings=embeddings,
                                            namespace=primary_namespace
                                        )
                                        
                                        web_docs = await web_retriever.ainvoke(prompt)
                                        if not web_docs or len(web_docs) == 0:
                                            # Try fallback namespace
                                            logging.warning(f"No docs found in primary namespace, trying fallback: {fallback_namespace}")
                                            web_retriever = store.as_retriever(
                                                top_k=10,
                                                embeddings=embeddings,
                                                namespace=fallback_namespace
                                            )
                                    except Exception as e:
                                        # On error, fall back to the old namespace
                                        logging.warning(f"Error with primary namespace: {str(e)}. Trying fallback.")
                                        web_retriever = store.as_retriever(
                                            top_k=10,
                                            embeddings=embeddings,
                                            namespace=fallback_namespace
                                        )
                                    
                                    # Get documents from external source
                                    try:
                                        web_docs = await web_retriever.ainvoke(prompt)
                                        if web_docs:
                                            for doc in web_docs:
                                                # Add a source marker to distinguish in the UI
                                                if hasattr(doc, "metadata") and isinstance(doc.metadata, dict):
                                                    doc.metadata["is_external_source"] = True
                                                    doc.metadata["source_url"] = data_source.get("url", "")
                                                    doc.metadata["source_title"] = data_source.get("title", "")
                                                    
                                            external_source_docs.extend(web_docs)
                                            logging.info(f"Retrieved {len(web_docs)} documents from external source {data_source.get('url')}")
                                    except Exception as e:
                                        logging.error(f"Error retrieving from external source {data_source.get('url')}: {e}")
                    except Exception as e:
                        logging.error(f"Error processing external data sources: {e}")

                # Build multi-query retriever with GPT-4 for better query expansion
                llm_for_multiquery = ChatOpenAI(
                    model="gpt-4.1-2025-04-14",  # Use latest GPT-4 for better query understanding
                    temperature=0.0  # Keep deterministic
                )

                # We don't need to capture queries here anymore.
                # We'll generate them in a separate function below so they can be streamed earlier
                generated_queries = []

                # Create the multi-query retriever without callbacks
                multi_retriever = MultiQueryRetriever.from_llm(
                    retriever=base_retriever,
                    llm=llm_for_multiquery
                )

                # Use NVIDIA's reranker as it outperforms others according to research
                reranker = build_reranker(
                    provider=RerankerProvider.NVIDIA.value,
                    model="nvidia/nv-rerankqa-mistral-4b-v3",
                    top_k=5
                )
                
                if not reranker:
                    # fallback without reranker
                    docs = await multi_retriever.ainvoke(prompt)
                else:
                    combined_retriever = ContextualCompressionRetriever(
                        base_compressor=reranker,
                        base_retriever=multi_retriever
                    )
                    docs = await combined_retriever.ainvoke(prompt)
                
                # Add the generated queries to the document metadata for frontend display
                if generated_queries:
                    # Add to the metadata of the first document
                    if docs and len(docs) > 0:
                        if not hasattr(docs[0], "metadata") or docs[0].metadata is None:
                            from langchain_core.documents import Document
                            if isinstance(docs[0], Document):
                                docs[0].metadata = {}
                        if hasattr(docs[0], "metadata"):
                            docs[0].metadata["multi_queries"] = generated_queries
                            logging.info(f"Added {len(generated_queries)} multi-queries to document metadata")
                            for i, q in enumerate(generated_queries):
                                logging.info(f"  Query {i+1}: {q}")
                    
                # Add external source documents and rerank the combined set
                if external_source_docs:
                    docs.extend(external_source_docs)
                    # Re-rank the combined set if we have a reranker
                    if reranker:
                        try:
                            docs = await reranker.acompress_documents(docs, prompt)
                            logging.info(f"Re-ranked combined repository and external sources documents")
                        except Exception as e:
                            logging.error(f"Error re-ranking combined documents: {e}")
                
                # Either use GraphRAG or Nuanced enhancement (GraphRAG takes precedence)
                if use_graph_rag:
                    try:
                        from retriever import GraphRAGRetriever
                        
                        # Print clear banner in logs
                        logging.info(f"")
                        logging.info(f"==== 🔍 GRAPH RAG ENHANCEMENT ====")
                        logging.info(f"Project ID: {project_id}")
                        logging.info(f"Documents: {len(docs)}")
                        
                        # Setup GraphRAG enhancement - use path from config if available
                        repo_path = config.get("repo_path", f"/tmp/my_local_repo_{project_id}")
                        repo_exists = os.path.exists(repo_path)
                        
                        # Try alternative paths if the repository doesn't exist at the default path
                        if not repo_exists and not config.get("repo_path"):
                            logging.info(f"GraphRAG: Repository not found at {repo_path}, trying alternatives...")
                            
                            # Try standard paths first
                            standard_paths = [
                                f"/tmp/my_local_repo_{project_id}",
                                f"/tmp/nuanced_debug_{project_id}",
                                f"/tmp/nia_repo_{project_id}"
                            ]
                            
                            for alt_path in standard_paths:
                                if os.path.exists(alt_path) and alt_path != repo_path:
                                    repo_path = alt_path
                                    repo_exists = True
                                    logging.info(f"GraphRAG: Found repository at alternative path: {repo_path}")
                                    break
                                    
                            # For community repositories, try special paths
                            if not repo_exists and config.get("is_community", False):
                                admin_id = os.getenv("ADMIN_USER_ID", "admin")
                                community_paths = [
                                    f"/tmp/my_local_repo_community_{project_id}",
                                    f"/tmp/community_{project_id}",
                                    f"/tmp/community_{admin_id}_{project_id}"
                                ]
                                
                                for comm_path in community_paths:
                                    if os.path.exists(comm_path):
                                        repo_path = comm_path
                                        repo_exists = True
                                        logging.info(f"GraphRAG: Found community repository at: {repo_path}")
                                        break
                        
                        if repo_exists:
                            logging.info(f"GraphRAG: Using repository at: {repo_path}")
                        else:
                            logging.warning(f"GraphRAG: No repository found for project {project_id}")
                        
                        # Try to get graph data from database even if repo doesn't exist
                        try:
                            from services.nuanced_service import NuancedService
                            graph_data = NuancedService.get_graph_from_db(project_id)
                            if graph_data:
                                logging.info(f"Retrieved graph data from database for project {project_id}")
                        except Exception as e:
                            graph_data = None
                            logging.warning(f"Error retrieving graph data: {e}")
                        
                        # Create base retriever for GraphRAG
                        if combined_retriever:
                            base_for_graph = combined_retriever
                        else:
                            base_for_graph = multi_retriever
                        
                        # Initialize GraphRAG retriever
                        graph_retriever = GraphRAGRetriever(
                            base_retriever=base_for_graph,
                            repo_path=repo_path if repo_exists else "",
                            project_id=project_id,
                            graph_data=graph_data,
                            query_mode=graph_query_mode
                        )
                        
                        # Get enhanced results using GraphRAG
                        graph_docs = await graph_retriever._get_relevant_documents(prompt)
                        
                        if graph_docs:
                            docs = graph_docs
                            logging.info(f"✅ GRAPH RAG ENHANCEMENT COMPLETE: {len(docs)} documents processed")
                        else:
                            logging.warning(f"❌ GRAPH RAG ENHANCEMENT FAILED, using original documents")
                        
                        logging.info(f"==========================================")
                    except Exception as e:
                        logging.error(f"❌ GRAPH RAG ERROR: {str(e)}")
                        logging.error(f"Continuing with regular documents")
                        # Keep original docs
                elif use_nuanced:
                    # Only use Nuanced if GraphRAG is not used
                    try:
                        from services.nuanced_service import NuancedService
                        from retriever import NuancedEnhancedRetriever
                        
                        # Print clear banner in logs
                        logging.info(f"")
                        logging.info(f"==== 🔍 NUANCED CALL GRAPH REQUESTED ====")
                        logging.info(f"Project ID: {project_id}")
                        logging.info(f"Documents: {len(docs)}")
                        
                        # First try to get graph from database
                        graph_data = NuancedService.get_graph_from_db(project_id)
                        if graph_data:
                            # Use in-memory graph data directly
                            logging.info(f"✅ USING GRAPH FROM DATABASE: {len(graph_data) if isinstance(graph_data, dict) and 'functions' not in graph_data else len(graph_data.get('functions', {}))} functions")
                            
                            # Enhance each document directly using the _enrich_document_with_nuanced method
                            enhanced_docs = []
                            try:
                                # Create an instance just for document enhancement
                                graph_retriever = NuancedEnhancedRetriever(
                                    base_retriever=None, 
                                    repo_path="", 
                                    external_graph=graph_data
                                )
                                
                                # Process each document
                                for doc in docs:
                                    # Pass the graph data directly to avoid field access issues
                                    enhanced_doc = graph_retriever._enrich_document_with_nuanced(
                                        doc, 
                                        external_graph_data=graph_data
                                    )
                                    enhanced_docs.append(enhanced_doc)
                                
                                docs = enhanced_docs
                                logging.info(f"✅ ENHANCEMENT COMPLETE: {len(enhanced_docs)} documents processed")
                            except Exception as e:
                                logging.error(f"❌ NUANCED ENHANCEMENT ERROR: {str(e)}")
                                import traceback
                                logging.error(f"Stack trace: {traceback.format_exc()}")
                                # Continue with unenhanced documents if enhancement fails
                                logging.info(f"Continuing with unenhanced documents")
                        else:
                            # Fall back to local repository search
                            logging.info(f"No graph found in database, trying local repository...")
                        
                            # Get repo path from config if available, otherwise use default path
                            repo_path = config.get("repo_path", f"/tmp/my_local_repo_{project_id}")
                            repo_exists = os.path.exists(repo_path)
                            
                            # If not found, try alternative paths
                            if not repo_exists:
                                logging.info(f"Repository not found at {repo_path}, searching for alternatives...")
                                
                                # First check standard paths derived from project_id
                                standard_paths = [
                                    f"/tmp/my_local_repo_{project_id}",
                                    f"/tmp/nuanced_debug_{project_id}",
                                    f"/tmp/nia_repo_{project_id}"
                                ]
                                
                                for std_path in standard_paths:
                                    if os.path.exists(std_path) and std_path != repo_path:
                                        repo_path = std_path
                                        repo_exists = True
                                        logging.info(f"Found standard repository path: {repo_path}")
                                        break
                                        
                                # If still not found, try glob patterns
                                if not repo_exists:
                                    possible_formats = [
                                        f"my_local_repo_{project_id}*",
                                        f"nuanced_debug_{project_id}*",
                                        f"nia_repo_{project_id}*",
                                        f"*{project_id}*"  # Last resort - any path containing project ID
                                    ]
                                    
                                    for pattern in possible_formats:
                                        import glob
                                        matches = glob.glob(f"/tmp/{pattern}")
                                        if matches:
                                            repo_path = matches[0]
                                            repo_exists = True
                                            logging.info(f"Found alternative repository path via glob: {repo_path}")
                                            break
                                
                                if not repo_exists:
                                    # For community repos, try looking at namespace format paths
                                    if config.get("is_community", False):
                                        logging.info(f"Checking community-specific paths for project {project_id}")
                                        admin_id = os.getenv("ADMIN_USER_ID", "admin")
                                        community_paths = [
                                            f"/tmp/my_local_repo_community_{project_id}",
                                            f"/tmp/community_{project_id}",
                                            f"/tmp/community_{admin_id}_{project_id}"
                                        ]
                                        
                                        for comm_path in community_paths:
                                            if os.path.exists(comm_path):
                                                repo_path = comm_path
                                                repo_exists = True
                                                logging.info(f"Found community repository path: {repo_path}")
                                                break
                                                
                                if not repo_exists:
                                    logging.warning(f"❌ NO REPO FOUND: Could not find any repository for project {project_id}")
                                    # Continue without Nuanced enhancement
                            
                            # Check Nuanced availability
                            nuanced_installed = NuancedService.is_installed()
                            
                            logging.info(f"Nuanced installed: {nuanced_installed}")
                            logging.info(f"Repository exists: {repo_exists} ({repo_path})")
                            
                            if repo_exists and nuanced_installed:
                                # Create temporary retriever just for enhancement
                                logging.info(f"✅ INITIALIZING NUANCED with repo path: {repo_path}")
                                try:
                                    nuanced_retriever = NuancedEnhancedRetriever(
                                        base_retriever=None, 
                                        repo_path=repo_path
                                    )
                                    
                                    # Check if .nuanced directory exists
                                    nuanced_dir = os.path.join(repo_path, ".nuanced")
                                    graph_file = os.path.join(nuanced_dir, "nuanced-graph.json")
                                    
                                    if os.path.exists(nuanced_dir):
                                        logging.info(f"✅ NUANCED DIRECTORY found: {nuanced_dir}")
                                        if os.path.exists(graph_file):
                                            graph_size = os.path.getsize(graph_file) / 1024
                                            logging.info(f"✅ NUANCED GRAPH found: {graph_file} ({graph_size:.2f} KB)")
                                        else:
                                            logging.warning(f"❌ NUANCED GRAPH MISSING: {graph_file}")
                                    else:
                                        logging.warning(f"❌ NUANCED DIRECTORY MISSING: {nuanced_dir}")
                                        
                                    # Enhance each document
                                    enhanced_docs = []
                                    for doc in docs:
                                        enhanced_doc = nuanced_retriever._enrich_document_with_nuanced(doc)
                                        enhanced_docs.append(enhanced_doc)
                                    
                                    docs = enhanced_docs
                                    logging.info(f"✅ ENHANCEMENT COMPLETE: {len(enhanced_docs)} documents processed")
                                except Exception as e:
                                    logging.error(f"❌ NUANCED LOCAL ENHANCEMENT ERROR: {str(e)}")
                                    import traceback
                                    logging.error(f"Stack trace: {traceback.format_exc()}")
                                    # Continue with unenhanced documents if enhancement fails
                                    logging.info(f"Continuing with unenhanced documents")
                            else:
                                if not nuanced_installed:
                                    logging.warning(f"❌ NUANCED NOT INSTALLED: Install with 'pip install nuanced'")
                                if not repo_exists:
                                    logging.warning(f"❌ REPOSITORY NOT FOUND: {repo_path}")
                        
                        logging.info(f"==========================================")
                    except Exception as e:
                        logging.error(f"❌ NUANCED ERROR: {str(e)}")
                        logging.error(f"Stack trace: {e.__traceback__}")
                        logging.info(f"==========================================")
                        # Continue with original docs if enhancement fails
                
                # Add results to combined lists
                if docs:
                    all_docs.extend(docs)
                    all_contexts.extend([doc.page_content for doc in docs])
                    all_sources.extend([doc.metadata.get("file_path", "unknown") for doc in docs])

            # Also get any active data sources (globally enabled)
            try:
                active_sources = db_instance.get_active_data_sources(user_id)
                if active_sources and include_external_sources:
                    logging.info(f"Found {len(active_sources)} globally active data sources for user {user_id}")
                    
                    # For external web sources, use a completely separate index
                    web_sources_index_name = "web-sources"  # Use dedicated index instead of nia-app
                    logging.info(f"Using dedicated index for web sources: {web_sources_index_name}")
                    
                    # Create a separate Pinecone instance for web sources
                    try:
                        web_store = PineconeVectorStore(
                            index_name=web_sources_index_name,
                            dimension=1536,
                            alpha=1.0
                        )
                        logging.info(f"Successfully connected to {web_sources_index_name} index")
                    except Exception as e:
                        logging.error(f"Error connecting to {web_sources_index_name} index: {e}")
                        logging.error(f"Falling back to standard index: {config['index_name']}")
                        web_store = store  # Fall back to regular store if dedicated index unavailable
                    
                    # Get current user ID from project configs to enforce privacy
                    current_user_id = None
                    if project_configs and len(project_configs) > 0:
                        current_user_id = project_configs[0].get("user_id")
                        logging.info(f"Current request user ID: {current_user_id}")
                    
                    for active_source in active_sources:
                        if active_source and active_source.get("status") == "completed":
                            source_id = active_source["id"]
                            source_url = active_source.get('url', 'unknown')
                            source_owner = active_source.get('user_id', None)
                            
                            # CRITICAL: Privacy check - only retrieve sources that belong to the current user
                            if source_owner and current_user_id and source_owner != current_user_id:
                                logging.info(f"⚠️ PRIVACY FILTER: Skipping source {source_id} owned by {source_owner} (current user: {current_user_id})")
                                continue
                            
                            # Use the new namespace format that includes user isolation
                            # Format: web-sources_{user_id}_{source_id}
                            source_namespace = f"web-sources_{source_owner}_{source_id}"
                            logging.info(f"Adding globally active data source: {source_url} (namespace: {source_namespace})")
                            
                            # Create a retriever for the active data source using the web-sources index
                            source_retriever = web_store.as_retriever(
                                top_k=5,  # Smaller result set for external sources
                                embeddings=embeddings,
                                namespace=source_namespace
                            )
                            
                            logging.info(f"Running retrieval for external source: {source_url}")
                            
                            # Run retrieval with the same prompt
                            try:
                                source_docs = source_retriever.invoke(prompt)
                                logging.info(f"Retrieval returned {len(source_docs) if source_docs else 0} docs from {source_url}")
                                
                                if not source_docs or len(source_docs) == 0:
                                    # Try the old namespace format as a fallback
                                    old_namespace = f"source_{source_id}"
                                    logging.info(f"No results with new namespace, trying legacy namespace: {old_namespace}")
                                    
                                    fallback_retriever = web_store.as_retriever(
                                        top_k=5,
                                        embeddings=embeddings,
                                        namespace=old_namespace
                                    )
                                    
                                    source_docs = fallback_retriever.invoke(prompt)
                                    logging.info(f"Legacy namespace retrieval returned {len(source_docs) if source_docs else 0} docs")
                                    
                                    if not source_docs or len(source_docs) == 0:
                                        logging.warning(f"No documents found for external source: {source_url} in any namespace. Skipping.")
                                        continue
                                
                                # Tag documents with source info for clear identification in UI
                                for doc in source_docs:
                                    if not doc.metadata:
                                        doc.metadata = {}
                                    # Add external source tags
                                    doc.metadata["external_source"] = "true"
                                    doc.metadata["source_url"] = source_url
                                    doc.metadata["source_id"] = source_id
                                    doc.metadata["source_owner"] = source_owner
                                    # Set a consistent file_path format that the frontend can parse
                                    doc.metadata["file_path"] = f"EXTERNAL:{source_url}"
                                    
                                # Add to results
                                if source_docs:
                                    logging.info(f"Retrieved {len(source_docs)} docs from external source: {source_url}")
                                    # Create external source paths with EXTERNAL: prefix
                                    source_paths = [f"EXTERNAL:{source_url}" for _ in range(len(source_docs))]
                                    
                                    # Debug logs for tracking external sources
                                    logging.info(f"Adding external source paths: {source_paths}")
                                    
                                    # Actually add the documents and sources to the result collections
                                    all_docs.extend(source_docs)
                                    all_sources.extend(source_paths)
                                    all_contexts.extend([doc.page_content for doc in source_docs])
                                    
                                    # Add extra logging to confirm successful addition to results
                                    logging.info(f"✅ EXTERNAL SOURCE ADDED: {source_url} with {len(source_docs)} documents")
                                    # Log the first few characters of the first doc to confirm content
                                    if source_docs:
                                        first_doc_preview = source_docs[0].page_content[:100] + "..." if len(source_docs[0].page_content) > 100 else source_docs[0].page_content
                                        logging.info(f"Sample content: {first_doc_preview}")
                                
                            except Exception as e:
                                logging.error(f"Error retrieving from active data source {source_url}: {str(e)}")
                                logging.error(f"Stack trace: {traceback.format_exc()}")
                                # Continue with next source

            except Exception as e:
                logging.error(f"Error retrieving from active data sources: {str(e)}")
                logging.error(f"Stack trace: {traceback.format_exc()}")
                # Continue with just project sources

            # If we got no documents and this isn't our last retry, wait and try again
            if not all_docs and attempt < max_retries - 1:
                logging.info(f"No documents retrieved on attempt {attempt + 1}, waiting {retry_delay} seconds before retry...")
                await asyncio.sleep(retry_delay)
                continue

            # Log the sources we found
            logging.info(f"Retrieved {len(all_docs)} documents across {len(project_configs)} projects")
            logging.info(f"Source files: {all_sources}")
            
            # Log external sources specifically 
            external_sources = [s for s in all_sources if s.startswith("EXTERNAL:")]
            if external_sources:
                logging.info(f"FOUND {len(external_sources)} EXTERNAL SOURCES: {external_sources}")
            else:
                logging.info("NO EXTERNAL SOURCES found in final results")
            
            # Extract the content for the return value
            contexts = all_contexts
            sources = all_sources
            docs = all_docs
            
            # Ensure we're not returning empty results
            if not contexts:
                logging.warning("No contexts found across any projects, returning empty arrays")
                return [], [], []
            
            # Final check of sources before returning
            logging.info(f"RETURNING {len(sources)} SOURCES: {sources}")
            
            # Add another check for external sources
            external_sources = [s for s in sources if s.startswith("EXTERNAL:")]
            if external_sources:
                logging.info(f"SUCCESS: Including {len(external_sources)} external sources in final results")
                for i, src in enumerate(external_sources):
                    logging.info(f"  External source {i+1}: {src}")
            else:
                logging.warning("WARNING: No external sources found in final results despite retrieval attempts")
                
                # Check if we lost external sources somewhere
                active_sources = db_instance.get_active_data_sources(user_id)
                if active_sources:
                    logging.warning(f"Database has {len(active_sources)} active sources for user {user_id} that should have been included")
                    
            # Apply validation agent if not skipped and if there are enough docs
            if not skip_validation:
                # Skip validation if we already have a solid number of results
                if len(docs) >= 15:
                    logging.info(f"Skipping validation agent because we already have {len(docs)} documents")
                else:
                    try:
                        # Import here to avoid circular imports
                        from workflows.agent_validation import ValidationAgent
                        
                        # Make sure time is imported
                        import time
                        logging.info(f"🔍 APPLYING VALIDATION AGENT to assess document sufficiency")
                        start_time = time.perf_counter()
                        
                        # Add timeout protection to prevent hanging
                        import asyncio
                        try:
                            # Create task with timeout
                            validation_task = asyncio.create_task(
                                ValidationAgent.validate_and_enhance(
                                    query=prompt,
                                    docs=docs,
                                    contexts=contexts,
                                    sources=sources,
                                    project_configs=project_configs,
                                    user_id=user_id
                                )
                            )
                            
                            # Wait for task with timeout
                            docs, contexts, sources = await asyncio.wait_for(validation_task, timeout=60.0)  # 1 minute timeout
                            
                            duration = time.perf_counter() - start_time
                            logging.info(f"⏱️ Validation completed in {duration:.2f} seconds")
                            logging.info(f"📊 Final document count: {len(docs)}")
                            
                        except asyncio.TimeoutError:
                            logging.error(f"Validation agent timed out after 60 seconds")
                            # Continue with original results if validation times out
                            
                    except Exception as e:
                        logging.error(f"Error in validation agent, proceeding with original results: {e}")
                        import traceback
                        logging.error(f"Validation agent error details: {traceback.format_exc()}")
                        # Continue with original results if validation fails
            
            # Return the extracted contexts and sources
            return docs, contexts, sources

        except Exception as e:
            if attempt < max_retries - 1:
                logging.warning(f"Retrieval attempt {attempt + 1} failed: {str(e)}, retrying in {retry_delay} seconds...")
                # Make sure we import asyncio in this scope for proper error handling
                import asyncio
                await asyncio.sleep(retry_delay)
            else:
                logging.error(f"All retrieval attempts failed: {str(e)}")
                logging.error(f"Traceback: {traceback.format_exc()}")
                raise

def validate_safe_path(base_dir: str, user_path: str) -> Tuple[bool, Optional[str], Optional[str]]:
    """
    Securely validates and normalizes file paths to prevent directory traversal.
    Returns (is_valid, normalized_path, error_message).
    
    Security measures:
    - Prevents directory traversal attacks
    - Ensures paths stay within base directory
    - Validates path components
    - Normalizes path separators
    
    Args:
        base_dir: The base directory that should contain the path
        user_path: The user-provided path to validate
        
    Returns:
        Tuple of (is_valid, normalized_path, error_message)
    """
    try:
        # Convert paths to absolute and normalize
        base_dir = os.path.abspath(base_dir)
        full_path = os.path.abspath(os.path.join(base_dir, user_path))
        
        # Check if the full path starts with base_dir
        if not full_path.startswith(base_dir):
            return False, None, "Path would escape base directory"
            
        # Validate path components
        path_parts = full_path.split(os.sep)
        for part in path_parts:
            # Skip empty parts
            if not part:
                continue
                
            # Allow standard path components
            if part in ('.', '..'):
                return False, None, "Invalid path component"
                
            # Check for dangerous characters
            if any(c in part for c in ['\\', '/', ':', '*', '?', '"', '<', '>', '|']):
                return False, None, "Invalid path component"
                
            # Special handling for my_local_repo_ prefix
            if part.startswith('my_local_repo_'):
                try:
                    # Extract and validate UUID
                    potential_uuid = part.replace('my_local_repo_', '')
                    UUID(potential_uuid)
                except ValueError:
                    return False, None, "Invalid project ID format"
        
        return True, full_path, None
        
    except Exception as e:
        return False, None, f"Path validation error: {str(e)}" 