"""Utility functions for the backend application."""

# Import all utility functions from validation_utils
from .validation_utils import (
    validate_github_url,
    validate_safe_path,
    validate_file_path,
    validate_api_request,
)

# Import all utility functions from formatting_utils
from .formatting_utils import (
    format_context,
    process_code_blocks,
    normalize_indentation,
    format_markdown_for_display,
    truncate_text,
)

# Import all utility functions from retriever_utils
from .retriever_utils import (
    build_advanced_retriever,
    fallback_pinecone_retrieval,
    is_call_relationship_query,
    generate_nuanced_insight,
)

# Import all utility functions from logging_utils
from .logging_utils import (
    setup_logger,
    log_to_keywords_ai,
    safe_json_dumps
)
