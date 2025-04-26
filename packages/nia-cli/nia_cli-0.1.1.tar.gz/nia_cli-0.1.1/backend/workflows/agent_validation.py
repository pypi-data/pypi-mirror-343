import logging
import asyncio
import time
from datetime import datetime
from typing import Dict, List, Any, Optional, Callable, Tuple

from hatchet_sdk import Hatchet, Context

from utils.retriever_utils import fallback_pinecone_retrieval, is_call_relationship_query
from llm import build_llm_via_langchain
from utils.logging_utils import setup_logger
from workflows.utils import handle_workflow_errors

logger = setup_logger(__name__)

@Hatchet.workflow()
class AgentValidationWorkflow:
    """
    Workflow for validating and enhancing retrieval results using an agent.
    This can be used for deeper searches that would be too slow for synchronous API responses.
    """
    
    @Hatchet.step(timeout="10m")
    @handle_workflow_errors
    async def validate_and_enhance(self, context: Context):
        """
        Validate retrieval results and enhance with deeper searches if needed.
        
        Args:
            context: Workflow context containing input parameters
            
        Returns:
            Dictionary with enhanced results
        """
        # Get input parameters
        input_data = context.workflow_input()
        query = input_data["query"]
        user_id = input_data["user_id"]
        project_configs = input_data.get("project_configs", [])
        initial_results = input_data.get("initial_results", {})
        
        # Extract initial retrieval data
        initial_docs = initial_results.get("docs", [])
        initial_contexts = initial_results.get("contexts", [])
        initial_sources = initial_results.get("sources", [])
        
        # Log workflow started
        logger.info(f"Starting agent validation workflow for user {user_id}, projects {[p.get('project_id') for p in project_configs]}")
        
        # Validate results
        validation_result = await self._validate_results(query, initial_contexts, initial_sources)
        
        # If results are sufficient or if score is borderline, return them with validation info
        # This prevents unnecessary processing for scores close to the threshold
        if validation_result["sufficient"] or validation_result["score"] > 0.7:
            logger.info(f"Results deemed sufficient by agent (score: {validation_result['score']:.2f})")
            return {
                "status": "complete",
                "docs": initial_docs,
                "contexts": initial_contexts,
                "sources": initial_sources,
                "validation": validation_result,
                "enhanced": False
            }
        
        # If results are insufficient, perform deeper search
        logger.info(f"Results deemed insufficient by agent (score: {validation_result['score']}), performing enhanced search")
        
        # Construct enhanced queries based on missing information
        missing_info = validation_result.get("missing_info", [])
        enhanced_queries = [query]  # Always include the original query
        if missing_info:
            for info in missing_info:
                # Create a focused query for each missing information point
                enhanced_query = f"{query} related to {info}"
                enhanced_queries.append(enhanced_query)
        
        # Perform enhanced searches with each query
        enhanced_docs = []
        enhanced_contexts = []
        enhanced_sources = []
        
        # Determine if this is a call relationship query to optimize search settings
        use_nuanced = is_call_relationship_query(query)
        
        for enhanced_query in enhanced_queries:
            try:
                logger.info(f"Running enhanced search with query: '{enhanced_query}'")
                
                # Perform enhanced retrieval with potentially different parameters
                docs, contexts, sources = await fallback_pinecone_retrieval(
                    prompt=enhanced_query, 
                    project_configs=project_configs,
                    use_nuanced=use_nuanced,
                    include_external_sources=True,
                    user_id=user_id,
                    use_graph_rag=True,  # Enable GraphRAG for better code understanding
                    graph_query_mode="auto"  # Auto-detect the best graph mode
                )
                
                if docs:
                    logger.info(f"Enhanced search found {len(docs)} documents for query '{enhanced_query}'")
                    
                    # Add results to our enhanced collections
                    enhanced_docs.extend(docs)
                    enhanced_contexts.extend(contexts)
                    enhanced_sources.extend(sources)
                else:
                    logger.warning(f"Enhanced search found no documents for query '{enhanced_query}'")
                
            except Exception as e:
                logger.error(f"Error in enhanced search for query '{enhanced_query}': {e}")
                import traceback
                logger.error(f"Stack trace: {traceback.format_exc()}")
        
        # Combine original and enhanced results, removing duplicates
        if enhanced_docs:
            # Create sets for tracking seen sources to avoid duplicates
            seen_sources = set(initial_sources)
            
            # Find unique documents from enhanced search
            unique_docs = []
            unique_contexts = []
            unique_sources = []
            
            for doc, context, source in zip(enhanced_docs, enhanced_contexts, enhanced_sources):
                if source not in seen_sources:
                    seen_sources.add(source)
                    unique_docs.append(doc)
                    unique_contexts.append(context)
                    unique_sources.append(source)
            
            logger.info(f"Found {len(unique_docs)} unique documents from enhanced search")
            
            # Combine original and unique enhanced results
            all_docs = initial_docs + unique_docs
            all_contexts = initial_contexts + unique_contexts
            all_sources = initial_sources + unique_sources
            
            # Optionally rerank the combined results
            try:
                from reranker import build_reranker, RerankerProvider
                
                # Use highest quality reranker available for final results
                reranker = build_reranker(
                    provider=RerankerProvider.NVIDIA.value,
                    model="nvidia/nv-rerankqa-mistral-4b-v3",
                    top_k=len(all_docs)  # Keep all docs but reorder them
                )
                
                if reranker:
                    from langchain_core.documents import Document
                    
                    # Convert to Document objects for reranking
                    doc_objects = [
                        Document(page_content=context, metadata={"file_path": source})
                        for context, source in zip(all_contexts, all_sources)
                    ]
                    
                    # Rerank the documents
                    reranked_docs = await reranker.acompress_documents(doc_objects, query)
                    logger.info(f"Reranked {len(reranked_docs)} documents")
                    
                    # Extract reordered docs, contexts, and sources
                    all_docs = [doc for i, doc in enumerate(all_docs) if i < len(reranked_docs)]
                    all_contexts = [doc.page_content for doc in reranked_docs]
                    all_sources = [doc.metadata.get("file_path", "unknown") for doc in reranked_docs]
            except Exception as e:
                logger.error(f"Error reranking combined results: {e}")
                # Continue with the simple combined results if reranking fails
            
            # Re-validate combined results
            final_validation = await self._validate_results(query, all_contexts, all_sources)
            
            logger.info(f"Enhanced search complete. Original: {len(initial_docs)}, Enhanced: {len(unique_docs)}, "
                      f"Final score: {final_validation['score']}")
            
            return {
                "status": "complete",
                "docs": all_docs,
                "contexts": all_contexts,
                "sources": all_sources,
                "validation": final_validation,
                "enhanced": True,
                "original_count": len(initial_docs),
                "enhanced_count": len(unique_docs)
            }
        else:
            # If enhanced search found nothing, return original results
            logger.warning("Enhanced search found no additional documents, returning original results")
            return {
                "status": "complete",
                "docs": initial_docs,
                "contexts": initial_contexts,
                "sources": initial_sources,
                "validation": validation_result,
                "enhanced": True,
                "original_count": len(initial_docs),
                "enhanced_count": 0
            }
    
    async def _validate_results(self, query: str, contexts: List[str], sources: List[str]) -> Dict[str, Any]:
        """
        Use an LLM to validate if the retrieved results are sufficient to answer the query.
        
        Args:
            query: The user query
            contexts: The retrieved document contents
            sources: The source file paths
            
        Returns:
            Dictionary with validation results
        """
        try:
            # Limit the validation to a reasonable number of documents
            max_docs_to_validate = 10  # Balance between thoroughness and speed
            
            # Format results for validation
            formatted_context = ""
            for i, (context, source) in enumerate(zip(contexts[:max_docs_to_validate], sources[:max_docs_to_validate])):
                formatted_context += f"Document {i+1} (from {source}):\n{context}\n\n---\n\n"
            
            # Add a summary of additional documents if there are more than max_docs_to_validate
            if len(contexts) > max_docs_to_validate:
                additional_count = len(contexts) - max_docs_to_validate
                file_types = set([s.split('.')[-1] for s in sources[max_docs_to_validate:] if '.' in s])
                formatted_context += f"Note: There are {additional_count} additional documents not shown here"
                if file_types:
                    formatted_context += f" (file types: {', '.join(file_types)})"
                formatted_context += ".\n"
            
            # Create validation prompt
            from langchain_core.prompts import ChatPromptTemplate
            validation_prompt = ChatPromptTemplate.from_messages([
                ("system", """You are an expert code assistant tasked with evaluating retrieved context for a code-related question.
Your job is to determine if the retrieved context is sufficient to answer the query accurately and completely.

Analyze the retrieved context and the query, then provide:
1. A score from 0.0 to 1.0 indicating how sufficient the context is (where 1.0 is perfectly sufficient)
2. A brief explanation of your reasoning
3. Specific suggestions for what additional information is needed if the context is insufficient

For code-related queries, consider these specific aspects:
- Do we have the actual implementation/definition of relevant functions/classes?
- Do we have enough context about how different components interact?
- Are there important imports or dependencies missing?
- Do we have examples of usage if the query asks about how to use something?

Your response must be valid JSON with these keys:
- "score": float between 0.0 and 1.0
- "reasoning": short string explanation
- "missing_info": list of strings describing specific missing information
- "sufficient": boolean (true if score > 0.7)"""),
                ("human", """Query: {query}

Retrieved Context:
{context}

Evaluate the sufficiency of this context for answering the query accurately and completely.""")
            ])
            
            # Get validation response using Claude
            import json
            validation_llm = build_llm_via_langchain("anthropic", "claude-3-haiku-20240307")
            validation_response = await validation_llm.ainvoke(
                validation_prompt.format(
                    query=query, 
                    context=formatted_context
                )
            )
            
            # Extract validation result
            validation_text = validation_response.content
            
            # Try to parse the JSON response
            try:
                # Extract JSON from text if it's wrapped in backticks
                if "```json" in validation_text:
                    import re
                    json_match = re.search(r'```json\n(.*?)\n```', validation_text, re.DOTALL)
                    if json_match:
                        validation_text = json_match.group(1)
                    else:
                        # Try without the language specifier
                        json_match = re.search(r'```\n(.*?)\n```', validation_text, re.DOTALL)
                        if json_match:
                            validation_text = json_match.group(1)
                
                validation_json = json.loads(validation_text)
                
                # Ensure all required fields are present
                if "score" not in validation_json:
                    validation_json["score"] = 0.5
                
                if "missing_info" not in validation_json:
                    validation_json["missing_info"] = []
                
                if "reasoning" not in validation_json:
                    validation_json["reasoning"] = "No reasoning provided by the model."
                
                # Calculate "sufficient" based on score if not provided
                # Use a threshold of 0.7 for validation
                if "sufficient" not in validation_json:
                    # The example in the logs had a score of 0.7 but still triggered enhancement
                    # Let's use strict comparison to ensure 0.7 triggers enhancement
                    validation_json["sufficient"] = float(validation_json["score"]) > 0.7
                
                # Log the validation agent's reasoning for transparency
                validation_result = {
                    "score": float(validation_json.get("score", 0.0)),
                    "reasoning": validation_json.get("reasoning", ""),
                    "missing_info": validation_json.get("missing_info", []),
                    "sufficient": validation_json.get("sufficient", False) 
                }
                
                # Create detailed log of the agent's reasoning
                logger.info("")
                logger.info("=" * 40)
                logger.info("📝 VALIDATION AGENT REASONING")
                logger.info(f"Query: '{query}'")
                logger.info(f"Documents analyzed: {len(contexts)} (showing first {max_docs_to_validate})")
                logger.info(f"Sufficiency score: {validation_result['score']:.2f}/1.0")
                logger.info(f"Sufficient? {'✅ YES' if validation_result['sufficient'] else '❌ NO'}")
                logger.info(f"Reasoning: {validation_result['reasoning']}")
                
                if validation_result['missing_info']:
                    logger.info("Missing information:")
                    for i, info in enumerate(validation_result['missing_info']):
                        logger.info(f"  {i+1}. {info}")
                logger.info("=" * 40)
                logger.info("")
                
                return validation_result
            except json.JSONDecodeError:
                logger.error(f"Failed to parse validation response as JSON: {validation_text}")
                # Try to extract a score from the text directly
                import re
                score_match = re.search(r'score["\s:]+([0-9.]+)', validation_text, re.IGNORECASE)
                score = float(score_match.group(1)) if score_match else 0.5
                
                sufficient_match = re.search(r'sufficient["\s:]+(\w+)', validation_text, re.IGNORECASE)
                sufficient = sufficient_match.group(1).lower() == "true" if sufficient_match else (score > 0.7)
                
                return {
                    "score": score,
                    "reasoning": "Error parsing JSON response from validation model",
                    "missing_info": [],
                    "sufficient": sufficient
                }
        except Exception as e:
            logger.error(f"Error in validation: {e}")
            import traceback
            logger.error(f"Validation error details: {traceback.format_exc()}")
            
            # Default to sufficient to avoid blocking the workflow on validation errors
            return {
                "score": 0.71,
                "reasoning": f"Error in validation process: {str(e)}",
                "missing_info": [],
                "sufficient": True
            }

class ValidationAgent:
    """
    Agent that validates if retrieved documents are sufficient to answer a query,
    and enhances retrieval if needed.
    
    This is a synchronous wrapper around the async workflow that can be used
    directly in API endpoints.
    """
    
    @staticmethod
    async def validate_and_enhance(
        query: str,
        docs: List[Any],
        contexts: List[str],
        sources: List[str],
        project_configs: List[Dict[str, Any]],
        user_id: str
    ) -> Tuple[List[Any], List[str], List[str]]:
        """
        Validate if the retrieved documents are sufficient and enhance if needed.
        
        Args:
            query: The user query
            docs: The retrieved documents
            contexts: The retrieved document contents
            sources: The source file paths
            project_configs: List of project configurations
            user_id: The user ID
            
        Returns:
            Tuple of (docs, contexts, sources) - either original or enhanced
        """
        try:
            # Check if the workflow should run or if we should skip validation
            # Skip for very simple queries or when there are many results already
            if len(query.split()) <= 3 or len(docs) >= 15:
                logger.info(f"Skipping validation for short query or large result set (query: '{query}', results: {len(docs)})")
                return docs, contexts, sources
            
            # For immediate validation without Hatchet, use the validator directly
            workflow = AgentValidationWorkflow()
            validator = workflow._validate_results
            
            # Validate the initial results
            validation_result = await validator(query, contexts, sources)
            
            # If sufficient or borderline, return original results
            if validation_result.get("sufficient", False) or validation_result.get("score", 0.0) > 0.7:
                logger.info(f"Documents deemed sufficient (score: {validation_result.get('score', 0.0):.2f}/1.0)")
                return docs, contexts, sources
                
            # If insufficient, need to enhance
            logger.info(f"🔎 Documents deemed INSUFFICIENT (score: {validation_result.get('score', 0.0):.2f}/1.0)")
            logger.info(f"🔍 ENHANCEMENT PROCESS STARTING")
            
            # Get missing information points
            missing_info = validation_result.get("missing_info", [])
            
            # Prepare enhanced queries
            enhanced_queries = [query]  # Always include original
            if missing_info:
                logger.info(f"📋 Creating targeted queries based on missing information:")
                for i, info in enumerate(missing_info[:3]):  # Limit to 3 additional queries
                    enhanced_query = f"{query} related to {info}"
                    enhanced_queries.append(enhanced_query)
                    logger.info(f"  Query {i+1}: '{enhanced_query}'")
            
            # Get additional results for each enhanced query
            enhanced_docs = []
            enhanced_contexts = []
            enhanced_sources = []
            
            # Handle code relationship queries specially
            use_nuanced = is_call_relationship_query(query)
            
            # Determine if we should use GraphRAG - only use it for certain query types
            # Use it only for code structure related queries to avoid unnecessary overhead
            should_use_graphrag = len(query.split()) > 5 and any(term in query.lower() for term in 
                                        ['function', 'code', 'class', 'method', 'structure', 'architecture'])
            
            # Limit the number of enhanced queries to reduce load
            if len(enhanced_queries) > 3:
                logger.info(f"Limiting enhanced queries from {len(enhanced_queries)} to 3")
                enhanced_queries = enhanced_queries[:3]
                
            # Use concurrent processing with limits to avoid event loop issues
            async def process_enhanced_query(query_idx, enhanced_query):
                try:
                    logger.info(f"Running enhanced search {query_idx+1}/{len(enhanced_queries)}: '{enhanced_query}'")
                    
                    # Only use GraphRAG for the first query to avoid event loop issues
                    # Use a more targeted approach for subsequent queries
                    use_graph_for_this_query = should_use_graphrag and query_idx == 0
                    
                    # Run enhanced search with more aggressive parameters
                    e_docs, e_contexts, e_sources = await fallback_pinecone_retrieval(
                        prompt=enhanced_query,
                        project_configs=project_configs,
                        use_nuanced=use_nuanced and query_idx < 2,  # Only use Nuanced for first two queries
                        include_external_sources=True,
                        user_id=user_id,
                        use_graph_rag=use_graph_for_this_query,
                        graph_query_mode="drift" if use_graph_for_this_query else "auto",
                        skip_validation=True  # Important: prevent recursive validation
                    )
                    
                    # Return the results
                    return e_docs, e_contexts, e_sources
                except Exception as e:
                    logger.error(f"Error in enhanced search for query '{enhanced_query}': {e}")
                    logger.error(f"Stack trace: {traceback.format_exc()}")
                    # Return empty results on error
                    return [], [], []
            
            # Process enhanced queries with concurrency limits
            import traceback
            
            # Process the original query first, then do the enhanced queries
            tasks = []
            for i, eq in enumerate(enhanced_queries):
                task = asyncio.create_task(process_enhanced_query(i, eq))
                tasks.append(task)
                
                # Add a small delay between starting tasks to avoid overwhelming the event loop
                if i < len(enhanced_queries) - 1:
                    await asyncio.sleep(0.5)
            
            # Wait for all tasks to complete and gather results
            results = await asyncio.gather(*tasks, return_exceptions=True)
            
            # Process results and filter out exceptions
            for result in results:
                if isinstance(result, Exception):
                    logger.error(f"Task failed with exception: {result}")
                    continue
                    
                if not result or len(result) != 3:
                    continue
                    
                e_docs, e_contexts, e_sources = result
                enhanced_docs.extend(e_docs)
                enhanced_contexts.extend(e_contexts)
                enhanced_sources.extend(e_sources)
            
            # Deduplicate results based on sources
            seen_sources = set(sources)
            unique_docs = []
            unique_contexts = []
            unique_sources = []
            
            for doc, context, source in zip(enhanced_docs, enhanced_contexts, enhanced_sources):
                if source not in seen_sources:
                    seen_sources.add(source)
                    unique_docs.append(doc)
                    unique_contexts.append(context)
                    unique_sources.append(source)
            
            # Combine original and unique enhanced results
            all_docs = docs + unique_docs
            all_contexts = contexts + unique_contexts
            all_sources = sources + unique_sources
            
            logger.info("")
            logger.info("=" * 40)
            logger.info("📊 ENHANCEMENT RESULTS")
            logger.info(f"Original documents: {len(docs)}")
            logger.info(f"New unique documents: {len(unique_docs)}")
            logger.info(f"Total documents: {len(all_docs)}")
            
            if unique_docs:
                logger.info("New document sources:")
                for i, source in enumerate(unique_sources[:5]):  # Show first 5
                    logger.info(f"  {i+1}. {source}")
                if len(unique_sources) > 5:
                    logger.info(f"  ... and {len(unique_sources) - 5} more")
            logger.info("=" * 40)
            logger.info("")
            
            # Attach validation result to the last document's metadata for frontend display
            if all_docs and len(all_docs) > 0:
                last_doc = all_docs[-1]
                if not hasattr(last_doc, "metadata") or last_doc.metadata is None:
                    from langchain_core.documents import Document
                    if isinstance(last_doc, Document):
                        last_doc.metadata = {}
                    else:
                        # If it's not a Document type or doesn't have metadata, create a new one
                        last_doc = Document(page_content=last_doc.page_content if hasattr(last_doc, "page_content") else str(last_doc),
                                          metadata={})
                        all_docs[-1] = last_doc
                
                # Add validation results to document metadata
                if hasattr(last_doc, "metadata"):
                    last_doc.metadata["validation_reasoning"] = validation_result["reasoning"]
                    last_doc.metadata["validation_score"] = validation_result["score"]
                    last_doc.metadata["validation_sufficient"] = validation_result["sufficient"]
                    last_doc.metadata["validation_missing_info"] = validation_result["missing_info"]
            
            return all_docs, all_contexts, all_sources
        
        except Exception as e:
            logger.error(f"Error in validation agent: {e}")
            # Return original results on error
            return docs, contexts, sources