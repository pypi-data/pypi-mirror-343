#!/usr/bin/env python
"""
Utility script to regenerate knowledge graphs for projects using LLM-based extraction.

Usage:
  python -m utils.regenerate_graph --project_id <PROJECT_ID> [--force]
"""

import os
import sys
import asyncio
import argparse
import logging
from pathlib import Path

# Add the parent directory to sys.path to allow importing backend modules
sys.path.append(str(Path(__file__).parent.parent))

from db import MongoDB
from retriever import GraphRAGRetriever, build_retriever_from_args
from vector_store import build_vector_store_from_args
from langchain_openai import OpenAIEmbeddings

# Setup logging
logging.basicConfig(level=logging.INFO, 
                   format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

async def regenerate_graph_for_project(project_id, force=False):
    """Regenerate the knowledge graph for a specific project.
    
    Args:
        project_id: ID of the project
        force: Whether to force regeneration even if a graph already exists
    
    Returns:
        bool: Whether the operation was successful
    """
    logger.info(f"Regenerating knowledge graph for project {project_id} (force={force})")
    
    try:
        # Connect to the database
        db = MongoDB()
        
        # Get project metadata
        project = db.db.projects.find_one({"project_id": project_id})
        if not project:
            logger.error(f"Project {project_id} not found in database")
            return False
        
        # Create args object
        class Args:
            pass
        
        args = Args()
        args.project_id = project_id
        args.force_regenerate_graph = force
        args.use_graph_rag = True
        args.embedding_provider = "openai"
        args.embedding_model = "text-embedding-3-small"
        args.retriever_top_k = 20
        args.index_namespace = f"ns_{project_id}"
        args.reranker_provider = None
        args.reranker_model = None
        args.reranker_top_k = None
        args.multi_query_retriever = False
        args.llm_provider = "openai"
        args.llm_model = "gpt-4.1-2025-04-14"
        
        # Get local_dir if available
        args.local_dir = project.get("local_dir", "")
        if not args.local_dir or not os.path.exists(args.local_dir):
            potential_paths = [
                f"/tmp/my_local_repo_{project_id}",
                f"/tmp/nia_repo_{project_id}",
                f"/tmp/graph_rag_repo_{project_id}"
            ]
            
            for path in potential_paths:
                if os.path.exists(path):
                    logger.info(f"Found alternative repository path: {path}")
                    args.local_dir = path
                    break
        
        # Create vector store for retrieval
        embeddings = OpenAIEmbeddings(model=args.embedding_model)
        base_retriever = build_vector_store_from_args(args).as_retriever(
            top_k=args.retriever_top_k, 
            embeddings=embeddings, 
            namespace=args.index_namespace
        )
        
        # Initialize GraphRAG retriever
        graphrag_retriever = GraphRAGRetriever(
            base_retriever=base_retriever,
            repo_path=args.local_dir,
            project_id=project_id,
            graph_data=None,  # Force regeneration
            query_mode="auto"
        )
        
        # Regenerate the graph
        success = await graphrag_retriever.regenerate_graph_from_vectorstore()
        
        if success:
            logger.info(f"Successfully regenerated knowledge graph for project {project_id}")
            return True
        else:
            logger.error(f"Failed to regenerate knowledge graph for project {project_id}")
            return False
            
    except Exception as e:
        logger.error(f"Error regenerating knowledge graph for project {project_id}: {str(e)}")
        return False

async def main():
    parser = argparse.ArgumentParser(description="Regenerate knowledge graphs for projects")
    parser.add_argument("--project_id", required=True, help="Project ID to regenerate graph for")
    parser.add_argument("--force", action="store_true", help="Force regeneration even if a graph already exists")
    
    args = parser.parse_args()
    
    success = await regenerate_graph_for_project(args.project_id, args.force)
    
    if success:
        print(f"✅ Successfully regenerated knowledge graph for project {args.project_id}")
        sys.exit(0)
    else:
        print(f"❌ Failed to regenerate knowledge graph for project {args.project_id}")
        sys.exit(1)

if __name__ == "__main__":
    asyncio.run(main()) 