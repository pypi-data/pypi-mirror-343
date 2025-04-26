import os
import re
import json
import asyncio
from typing import AsyncGenerator, Optional, Dict, Any, List, Union
from enum import Enum

from langchain_anthropic import ChatAnthropic
from langchain_ollama import ChatOllama
from langchain_openai import ChatOpenAI
import requests
import logging

logger = logging.getLogger(__name__)

def build_llm_via_langchain(provider: str, model: str):
    """Builds a language model via LangChain."""
    if provider == "openai":
        if "OPENAI_API_KEY" not in os.environ:
            raise ValueError("Please set the OPENAI_API_KEY environment variable.")
        return ChatOpenAI(model=model or "gpt-4.1-2025-04-14")
    elif provider == "anthropic":
        if "ANTHROPIC_API_KEY" not in os.environ:
            raise ValueError("Please set the ANTHROPIC_API_KEY environment variable.")
        return ChatAnthropic(model=model or "claude-3-7-sonnet-20250219")
    elif provider == "ollama":
        return ChatOllama(model=model or "llama3.1")
    elif provider == "gemini":
        if "GEMINI_API_KEY" not in os.environ:
            raise ValueError("Please set the GEMINI_API_KEY environment variable.")
        import google.generativeai as genai
        genai.configure(api_key=os.environ["GEMINI_API_KEY"])
        return genai.GenerativeModel(model or "gemini-2.5-pro-exp-03-25")
    elif provider == "deepseek":
        if "DEEPSEEK_API_KEY" not in os.environ:
            raise ValueError("Please set the DEEPSEEK_API_KEY environment variable.")
        
        class DeepSeekChat:
            def __init__(self, model: str):
                self.model = model or "deepseek-chat"
                self.api_key = os.environ["DEEPSEEK_API_KEY"]
                self.base_url = "https://api.deepseek.com/v1"

            def chat(self, messages):
                response = requests.post(
                    f"{self.base_url}/chat/completions",
                    headers={
                        "Authorization": f"Bearer {self.api_key}",
                        "Content-Type": "application/json"
                    },
                    json={
                        "model": self.model,
                        "messages": messages,
                        "temperature": 0.7,
                        "max_tokens": 4096
                    }
                )
                response.raise_for_status()
                return response.json()["choices"][0]["message"]["content"]

        return DeepSeekChat(model)
    else:
        raise ValueError(f"Unrecognized LLM provider {provider}. Contributions are welcome!")

# Available models for each provider
AVAILABLE_MODELS = {
    "openai": ["gpt-4.1-2025-04-14"],
    "anthropic": ["claude-3-7-sonnet-20250219"],
    "gemini": ["gemini-2.5-pro-exp-03-25"],
    "deepseek": ["deepseek-chat"]
}

def get_available_models():
    """Returns the available models for each provider."""
    return AVAILABLE_MODELS

async def llm_generate(
    prompt: str,
    model: str = "gpt-4.1-2025-04-14", 
    provider: str = "openai",
    stream: bool = False,
    temperature: float = 0.7,
    max_tokens: Optional[int] = None
) -> Union[AsyncGenerator[str, None], str]:
    """
    Generate text using the specified LLM.
    
    Args:
        prompt: The input prompt
        model: The model to use
        provider: The provider (openai, anthropic, etc.)
        stream: Whether to stream the response
        temperature: The temperature to use
        max_tokens: Maximum tokens to generate
        
    Returns:
        If stream=True, returns an AsyncGenerator yielding strings
        If stream=False, returns the complete string response
    """
    # For OpenAI
    if provider == "openai":
        api_key = os.environ.get("OPENAI_API_KEY")
        if not api_key:
            raise ValueError("OPENAI_API_KEY environment variable not set")
        
        openai_client = ChatOpenAI(
            api_key=api_key,
            model=model,
            temperature=temperature,
            max_tokens=max_tokens,
            streaming=stream
        )
        
        messages = parse_prompt_to_messages(prompt)
        
        if stream:
            async def stream_response():
                try:
                    async for chunk in openai_client.astream(messages):
                        content = chunk.content
                        if content:
                            yield content
                        # Small delay to prevent overwhelming the client
                        await asyncio.sleep(0.01)
                except Exception as e:
                    logger.error(f"Error during streaming: {str(e)}")
                    # Yield a fallback message if streaming fails
                    yield "I apologize, but I encountered an error during processing. Please try again."
            
            return stream_response()
        else:
            response = await openai_client.ainvoke(messages)
            return response.content
    
    # For Anthropic
    elif provider == "anthropic":
        api_key = os.environ.get("ANTHROPIC_API_KEY")
        if not api_key:
            raise ValueError("ANTHROPIC_API_KEY environment variable not set")
        
        anthropic_client = ChatAnthropic(
            api_key=api_key,
            model=model or "claude-3-7-sonnet-20250219",
            temperature=temperature,
            max_tokens=max_tokens,
            streaming=stream
        )
        
        messages = parse_prompt_to_messages(prompt)
        
        if stream:
            async def stream_response():
                async for chunk in await anthropic_client.astream(messages):
                    content = chunk.content
                    if content:
                        yield content
            
            return stream_response()
        else:
            response = await anthropic_client.ainvoke(messages)
            return response.content
    
    # For other providers, implement as needed
    else:
        # Fallback to non-streaming for other providers
        llm = build_llm_via_langchain(provider, model)
        
        # Convert prompt to messages format if needed
        messages = parse_prompt_to_messages(prompt, provider)
        
        # Handle Gemini specifically
        if provider == "gemini":
            try:
                if stream:
                    async def stream_response():
                        response_stream = llm.generate_content(
                            messages,
                            stream=True,
                            generation_config={
                                "max_output_tokens": max_tokens or 1024,
                                "temperature": temperature
                            }
                        )
                        
                        for chunk in response_stream:
                            if hasattr(chunk, 'text') and chunk.text:
                                yield chunk.text
                                await asyncio.sleep(0.01)
                    
                    return stream_response()
                else:
                    response = llm.generate_content(
                        messages,
                        generation_config={
                            "max_output_tokens": max_tokens or 1024,
                            "temperature": temperature
                        }
                    )
                    return response.text
            except Exception as e:
                logger.error(f"Error with Gemini API: {str(e)}")
                raise
        # For other providers
        elif hasattr(llm, "ainvoke"):
            response = await llm.ainvoke(messages)
            return response.content
        elif hasattr(llm, "chat"):
            # For custom implementations like DeepSeek
            response = llm.chat(messages)
            return response
        else:
            raise ValueError(f"Unsupported LLM implementation for provider {provider}")

def parse_prompt_to_messages(prompt: str, provider: str = None) -> List[Dict[str, Any]]:
    """
    Parse a formatted prompt into a list of messages for LLM API.
    
    Example prompt format:
    "System: You are an AI assistant.
    
    User: Hello, how are you?
    
    Assistant: I'm doing well, thank you!"
    
    Args:
        prompt: The formatted prompt to parse
        provider: Optional provider name to format messages specifically for that provider
    """
    messages = []
    current_role = None
    current_content = []
    
    # Split by lines
    lines = prompt.split('\n')
    
    for line in lines:
        if line.startswith("System:"):
            # If we have content from a previous role, add it
            if current_role and current_content:
                messages.append({
                    "role": current_role,
                    "content": "\n".join(current_content).strip()
                })
                current_content = []
            
            current_role = "system"
            current_content.append(line[len("System:"):].strip())
        
        elif line.startswith("User:"):
            # If we have content from a previous role, add it
            if current_role and current_content:
                messages.append({
                    "role": current_role,
                    "content": "\n".join(current_content).strip()
                })
                current_content = []
            
            current_role = "user"
            current_content.append(line[len("User:"):].strip())
        
        elif line.startswith("Assistant:"):
            # If we have content from a previous role, add it
            if current_role and current_content:
                messages.append({
                    "role": current_role,
                    "content": "\n".join(current_content).strip()
                })
                current_content = []
            
            current_role = "assistant"
            current_content.append(line[len("Assistant:"):].strip())
        
        elif line.startswith("Context from repositories:"):
            # This is a special case - add it to the system message or create one if none exists
            if not any(msg.get("role") == "system" for msg in messages):
                messages.append({
                    "role": "system",
                    "content": f"You have access to the following context from code repositories:\n{line[len('Context from repositories:'):].strip()}"
                })
            else:
                # Find the system message and append to it
                for msg in messages:
                    if msg.get("role") == "system":
                        msg["content"] += f"\n\nYou have access to the following context from code repositories:\n{line[len('Context from repositories:'):].strip()}"
                        break
        
        elif current_role is not None:
            # Continue with current role
            current_content.append(line)
    
    # Add the last message if there's any
    if current_role and current_content:
        messages.append({
            "role": current_role,
            "content": "\n".join(current_content).strip()
        })
    
    # If no messages were created, treat the entire prompt as a user message
    if not messages:
        messages.append({
            "role": "user",
            "content": prompt.strip()
        })
    
    # Convert messages to provider-specific format if needed
    if provider == "gemini":
        # Convert to Gemini message format
        gemini_messages = []
        
        # Handle system message specially for Gemini (as user message with model response)
        system_content = None
        for msg in messages:
            if msg["role"] == "system":
                system_content = msg["content"]
                break
        
        if system_content:
            gemini_messages.append({"role": "user", "parts": [{"text": system_content}]})
            gemini_messages.append({"role": "model", "parts": [{"text": "I'll follow these instructions."}]})
        
        # Add other messages
        for msg in messages:
            if msg["role"] != "system":  # Skip system as we already handled it
                role = "user" if msg["role"] == "user" else "model"
                gemini_messages.append({"role": role, "parts": [{"text": msg["content"]}]})
        
        return gemini_messages
    
    return messages

