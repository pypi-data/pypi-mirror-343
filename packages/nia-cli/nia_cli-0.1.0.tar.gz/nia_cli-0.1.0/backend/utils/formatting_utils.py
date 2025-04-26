import re
from typing import List, Dict, Any

def format_context(sources: List[str], contexts: List[str]) -> str:
    """
    Format the context for the system prompt.
    
    Creates a formatted string with sources and their corresponding contexts,
    suitable for inclusion in a system prompt for an LLM.
    
    Args:
        sources: List of source identifiers (typically file paths)
        contexts: List of content snippets corresponding to each source
        
    Returns:
        A formatted string with sources and contexts
    """
    formatted = "Sources:\n"
    for source, context in zip(sources, contexts):
        formatted += f"- {source}\n"
    formatted += "\n"
    formatted += "Content:\n"
    for context in contexts:
        formatted += f"{context}\n\n"
    return formatted

def process_code_blocks(content: str) -> str:
    """
    Process and clean up code blocks in the content.
    
    Identifies code blocks in markdown format (```language...```) and cleans them up
    by removing HTML-like attributes, normalizing line endings, and removing
    invisible characters.
    
    Args:
        content: The text content containing code blocks
        
    Returns:
        The processed content with cleaned code blocks
    """
    def clean_code_block(match):
        full_block = match.group(0)
        language = match.group(1) if match.group(1) else ""
        code = match.group(2)
        
        # Clean up the code
        code = code.strip()
        # Remove any HTML-like attributes
        code = re.sub(r'\s+data-[a-zA-Z-]+=["]([^"]*)["]', '', code)
        # Normalize line endings
        code = code.replace('\r\n', '\n')
        # Remove invisible characters
        code = re.sub(r'[\u200B-\u200D\uFEFF]', '', code)
        
        return f"```{language}\n{code}\n```"
    
    # Find all code blocks and process them
    pattern = r"```(\w*)\n([\s\S]*?)```"
    processed_content = re.sub(pattern, clean_code_block, content)
    
    return processed_content

def normalize_indentation(code: str) -> str:
    """
    Normalize indentation in code by finding the minimum indentation level
    and removing it from all lines.
    
    Args:
        code: The code string to normalize
        
    Returns:
        Code with normalized indentation
    """
    # Split into lines
    lines = code.split('\n')
    non_empty_lines = [line for line in lines if line.strip()]
    
    if not non_empty_lines:
        return ""
    
    # Find minimum indentation
    min_indent = min(len(line) - len(line.lstrip()) for line in non_empty_lines)
    
    # Remove that indentation from all lines
    normalized_lines = []
    for line in lines:
        if line.strip():  # Only process non-empty lines
            normalized_lines.append(line[min_indent:] if len(line) >= min_indent else line)
        else:
            normalized_lines.append("")
    
    return '\n'.join(normalized_lines)

def format_markdown_for_display(markdown: str) -> str:
    """
    Format markdown content for display, ensuring proper rendering
    of code blocks, lists, and other markdown elements.
    
    Args:
        markdown: The markdown content to format
        
    Returns:
        Formatted markdown ready for display
    """
    # Process code blocks
    markdown = process_code_blocks(markdown)
    
    # Ensure proper spacing for lists
    markdown = re.sub(r'(\n[*-]\s.*\n)(?=[*-]\s)', r'\1\n', markdown)
    
    # Ensure headers have space before them
    markdown = re.sub(r'(\n)(?=#{1,6}\s)', r'\n\n', markdown)
    
    return markdown.strip()

def truncate_text(text: str, max_length: int = 1000, add_ellipsis: bool = True) -> str:
    """
    Truncate text to a maximum length, optionally adding an ellipsis.
    
    Args:
        text: The text to truncate
        max_length: Maximum length of the truncated text
        add_ellipsis: Whether to add "..." at the end of truncated text
        
    Returns:
        Truncated text
    """
    if len(text) <= max_length:
        return text
    
    truncated = text[:max_length]
    if add_ellipsis:
        truncated += "..."
    
    return truncated 