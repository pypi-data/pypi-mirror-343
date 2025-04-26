import os
import json
import logging
import asyncio
from typing import List, Dict, Any, Optional

from langchain_core.documents import Document

# Setup logging
logger = logging.getLogger(__name__)

async def extract_knowledge_graph(documents: List[Document], llm_provider: str = "openai", model: str = "gpt-4.1-2025-04-14") -> Dict[str, Any]:
    """
    Extract a knowledge graph from documents using an LLM.
    
    Args:
        documents: List of documents to process
        llm_provider: LLM provider to use (openai, anthropic, etc.)
        model: Specific model to use
        
    Returns:
        A knowledge graph with entities, relationships, and claims
    """
    logger.info(f"Extracting knowledge graph from {len(documents)} documents")
    graph = {"entities": {}, "relationships": [], "claims": []}
    
    for i, doc in enumerate(documents):
        logger.info(f"Processing document {i+1}/{len(documents)}")
        try:
            # Extract entities
            entities = await extract_entities(doc, llm_provider, model)
            if not entities:
                logger.warning(f"No entities extracted from document {i+1}")
                continue
                
            # Extract relationships between entities
            relationships = await extract_relationships(doc, entities, llm_provider, model)
            
            # Extract factual claims
            claims = await extract_claims(doc, entities, llm_provider, model)
            
            # Update graph
            for entity in entities:
                entity_id = entity["id"]
                if entity_id not in graph["entities"]:
                    graph["entities"][entity_id] = entity
                else:
                    # Merge descriptions if the entity already exists
                    existing_desc = graph["entities"][entity_id].get("description", "")
                    new_desc = entity.get("description", "")
                    if new_desc and new_desc != existing_desc:
                        graph["entities"][entity_id]["description"] = f"{existing_desc} {new_desc}".strip()
            
            graph["relationships"].extend(relationships)
            graph["claims"].extend(claims)
            
            # Small delay to avoid rate limiting
            await asyncio.sleep(0.1)
            
        except Exception as e:
            logger.error(f"Error processing document {i+1}: {str(e)}")
    
    logger.info(f"Extracted {len(graph['entities'])} entities, {len(graph['relationships'])} relationships, and {len(graph['claims'])} claims")
    return graph

async def extract_entities(document: Document, llm_provider: str, model: str) -> List[Dict[str, Any]]:
    """
    Extract entities from a document using an LLM.
    
    Args:
        document: The document to extract entities from
        llm_provider: LLM provider to use
        model: Specific model to use
        
    Returns:
        List of extracted entities with id, name, type, and description
    """
    from llm import llm_generate
    
    content = document.page_content
    metadata = document.metadata
    
    # Include filepath in context if available
    context = ""
    if "file_path" in metadata:
        context = f"This text is from file: {metadata['file_path']}\n\n"
    
    # Use a sliding window if the document is too large
    MAX_CHUNK_SIZE = 8000
    if len(content) > MAX_CHUNK_SIZE:
        chunks = [content[i:i + MAX_CHUNK_SIZE] for i in range(0, len(content), MAX_CHUNK_SIZE)]
        all_entities = []
        
        for i, chunk in enumerate(chunks):
            logger.info(f"Processing chunk {i+1}/{len(chunks)} for entity extraction")
            chunk_entities = await _extract_entities_from_text(context + chunk, llm_provider, model)
            all_entities.extend(chunk_entities)
            
        # Deduplicate entities based on name
        unique_entities = {}
        for entity in all_entities:
            if entity["name"] not in unique_entities:
                unique_entities[entity["name"]] = entity
        
        return list(unique_entities.values())
    else:
        return await _extract_entities_from_text(context + content, llm_provider, model)

async def _extract_entities_from_text(text: str, llm_provider: str, model: str) -> List[Dict[str, Any]]:
    """Helper function to extract entities from text."""
    from llm import llm_generate
    
    prompt = f"""
    System: You are an expert entity extraction system. Your task is to extract all entities from the provided text.
    
    An entity is a real-world object like a person, organization, location, file, function, class, or concept that has a distinct identity.
    
    For each entity, provide:
    1. A unique ID (a short slug)
    2. The entity name (exactly as it appears in the text)
    3. The entity type (person, organization, location, file, function, class, concept, etc.)
    4. A brief description of the entity based on the text
    
    Format your response as a JSON array of entities with these attributes.
    Example: 
    [
      {{
        "id": "user_class",
        "name": "User",
        "type": "class",
        "description": "A class that represents a user in the system with authentication methods"
      }},
      {{
        "id": "auth_service",
        "name": "AuthService",
        "type": "service",
        "description": "Service responsible for user authentication and authorization"
      }}
    ]
    
    User: {text}
    
    Assistant:
    """
    
    response = await llm_generate(prompt, model=model, provider=llm_provider)
    
    try:
        # Find JSON in the response
        json_start = response.find('[')
        json_end = response.rfind(']') + 1
        
        if json_start >= 0 and json_end > json_start:
            json_str = response[json_start:json_end]
            entities = json.loads(json_str)
            return entities
        else:
            logger.error("No valid JSON found in entity extraction response")
            return []
    except Exception as e:
        logger.error(f"Error parsing entity extraction response: {str(e)}")
        return []

async def extract_relationships(document: Document, entities: List[Dict[str, Any]], llm_provider: str, model: str) -> List[Dict[str, Any]]:
    """
    Extract relationships between entities in a document using an LLM.
    
    Args:
        document: The document to extract relationships from
        entities: List of entities extracted from the document
        llm_provider: LLM provider to use
        model: Specific model to use
        
    Returns:
        List of extracted relationships with source, target, type, and description
    """
    from llm import llm_generate
    
    if not entities or len(entities) < 2:
        return []  # Need at least 2 entities to form a relationship
    
    content = document.page_content
    metadata = document.metadata
    
    # Include filepath in context if available
    context = ""
    if "file_path" in metadata:
        context = f"This text is from file: {metadata['file_path']}\n\n"
    
    # Create a list of entity names for the prompt
    entity_list = "\n".join([f"- {entity['name']} ({entity['type']}): {entity['description']}" for entity in entities])
    
    prompt = f"""
    System: You are an expert relationship extraction system. Your task is to identify relationships between the entities that appear in the provided text.
    
    I'll provide you with a list of entities that were found in the text and the text itself. Please identify any relationships between these entities.
    
    For each relationship, provide:
    1. The source entity ID
    2. The target entity ID
    3. The relationship type (e.g., calls, imports, contains, references, depends_on, etc.)
    4. A brief description of the relationship
    
    Format your response as a JSON array of relationships.
    Example:
    [
      {{
        "source": "auth_service",
        "target": "user_class",
        "type": "uses",
        "description": "AuthService uses the User class for authentication"
      }},
      {{
        "source": "login_controller",
        "target": "auth_service",
        "type": "depends_on",
        "description": "LoginController depends on the AuthService for user authentication"
      }}
    ]
    
    Only include relationships that are explicitly mentioned or strongly implied in the text. Do not invent relationships.
    
    Entities:
    {entity_list}
    
    User: {context + content}
    
    Assistant:
    """
    
    response = await llm_generate(prompt, model=model, provider=llm_provider)
    
    try:
        # Find JSON in the response
        json_start = response.find('[')
        json_end = response.rfind(']') + 1
        
        if json_start >= 0 and json_end > json_start:
            json_str = response[json_start:json_end]
            relationships = json.loads(json_str)
            
            # Validate relationships
            valid_relationships = []
            entity_ids = {entity["id"] for entity in entities}
            
            for rel in relationships:
                if rel["source"] in entity_ids and rel["target"] in entity_ids:
                    valid_relationships.append(rel)
                else:
                    logger.warning(f"Invalid relationship: {rel} - entities not found in extracted entities")
            
            return valid_relationships
        else:
            logger.error("No valid JSON found in relationship extraction response")
            return []
    except Exception as e:
        logger.error(f"Error parsing relationship extraction response: {str(e)}")
        return []

async def extract_claims(document: Document, entities: List[Dict[str, Any]], llm_provider: str, model: str) -> List[Dict[str, Any]]:
    """
    Extract factual claims about entities from a document using an LLM.
    
    Args:
        document: The document to extract claims from
        entities: List of entities extracted from the document
        llm_provider: LLM provider to use
        model: Specific model to use
        
    Returns:
        List of extracted claims with entity_id and text
    """
    from llm import llm_generate
    
    if not entities:
        return []
    
    content = document.page_content
    metadata = document.metadata
    
    # Include filepath in context if available
    context = ""
    if "file_path" in metadata:
        context = f"This text is from file: {metadata['file_path']}\n\n"
    
    # Create a list of entity names for the prompt
    entity_list = "\n".join([f"- {entity['name']} ({entity['id']}): {entity['type']}" for entity in entities])
    
    prompt = f"""
    System: You are an expert claim extraction system. Your task is to extract factual claims about the provided entities from the text.
    
    A claim is a statement that asserts something about an entity that can be verified as true or false.
    
    For each claim, provide:
    1. The entity ID the claim is about
    2. The claim text (a concise factual statement)
    
    Format your response as a JSON array of claims.
    Example:
    [
      {{
        "entity_id": "user_class",
        "text": "The User class has authentication methods"
      }},
      {{
        "entity_id": "auth_service",
        "text": "AuthService uses JWT tokens for authentication"
      }}
    ]
    
    Only include claims that are explicitly stated in the text. Do not invent or infer claims beyond what is directly supported by the text.
    
    Entities:
    {entity_list}
    
    User: {context + content}
    
    Assistant:
    """
    
    response = await llm_generate(prompt, model=model, provider=llm_provider)
    
    try:
        # Find JSON in the response
        json_start = response.find('[')
        json_end = response.rfind(']') + 1
        
        if json_start >= 0 and json_end > json_start:
            json_str = response[json_start:json_end]
            claims = json.loads(json_str)
            
            # Validate claims
            valid_claims = []
            entity_ids = {entity["id"] for entity in entities}
            
            for claim in claims:
                if claim["entity_id"] in entity_ids:
                    valid_claims.append(claim)
                else:
                    logger.warning(f"Invalid claim: {claim} - entity not found in extracted entities")
            
            return valid_claims
        else:
            logger.error("No valid JSON found in claim extraction response")
            return []
    except Exception as e:
        logger.error(f"Error parsing claim extraction response: {str(e)}")
        return [] 