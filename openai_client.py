"""
Azure OpenAI Integration Module

This module provides a reusable function to generate AI responses using
Azure OpenAI Chat Completions API.

Authentication: API Key
Model: gpt-4o-mini
"""

import os
from openai import AzureOpenAI
from dotenv import load_dotenv
from typing import Optional, List, Dict

# Load environment variables
load_dotenv()


def get_openai_client(
    api_key: Optional[str] = None,
    endpoint: Optional[str] = None,
    api_version: Optional[str] = None
) -> AzureOpenAI:
    """
    Create and return an Azure OpenAI client.
    
    Args:
        api_key: Optional API key (defaults to env variable)
        endpoint: Optional endpoint (defaults to env variable)
        api_version: Optional API version (defaults to env variable)
    
    Returns:
        AzureOpenAI client instance
    """
    return AzureOpenAI(
        api_key=api_key or os.getenv("AZURE_OPENAI_API_KEY"),
        api_version=api_version or os.getenv("AZURE_OPENAI_API_VERSION", "2024-02-15-preview"),
        azure_endpoint=endpoint or os.getenv("AZURE_OPENAI_ENDPOINT")
    )


def generate_ai_response(
    prompt: str,
    system_message: Optional[str] = None,
    temperature: float = 0.7,
    max_tokens: int = 1000,
    api_key: Optional[str] = None,
    endpoint: Optional[str] = None,
    deployment_name: Optional[str] = None
) -> dict:
    """
    Generate an AI response using Azure OpenAI Chat Completions API.
    
    Args:
        prompt: The user prompt/question to send to the model
        system_message: Optional system message to set context
        temperature: Controls randomness (0-1, default 0.7)
        max_tokens: Maximum tokens in response (default 1000)
        api_key: Optional API key (defaults to env variable)
        endpoint: Optional endpoint (defaults to env variable)
        deployment_name: Optional deployment name (defaults to env variable)
    
    Returns:
        dict containing:
            - success: bool indicating if generation succeeded
            - prompt: the input prompt
            - response: the generated response text (if successful)
            - usage: token usage statistics
            - error: error message (if failed)
    
    Example:
        >>> result = generate_ai_response("Summarize the benefits of AI")
        >>> print(result['response'])
    """
    
    # Get configuration from environment or parameters
    api_key = api_key or os.getenv("AZURE_OPENAI_API_KEY")
    endpoint = endpoint or os.getenv("AZURE_OPENAI_ENDPOINT")
    deployment_name = deployment_name or os.getenv("AZURE_OPENAI_DEPLOYMENT_NAME", "gpt-4o-mini")
    
    # Validate configuration
    if not api_key:
        return {
            "success": False,
            "error": "Missing AZURE_OPENAI_API_KEY. Please set it in .env file.",
            "prompt": prompt,
            "response": None,
            "usage": None
        }
    
    if not endpoint:
        return {
            "success": False,
            "error": "Missing AZURE_OPENAI_ENDPOINT. Please set it in .env file.",
            "prompt": prompt,
            "response": None,
            "usage": None
        }
    
    try:
        # Create client
        client = get_openai_client(api_key, endpoint)
        
        # Build messages
        messages: List[Dict[str, str]] = []
        
        if system_message:
            messages.append({"role": "system", "content": system_message})
        else:
            messages.append({
                "role": "system",
                "content": "You are a helpful AI assistant. Provide clear, concise, and accurate responses."
            })
        
        messages.append({"role": "user", "content": prompt})
        
        # Make the API call
        response = client.chat.completions.create(
            model=deployment_name,
            messages=messages,
            temperature=temperature,
            max_tokens=max_tokens
        )
        
        # Extract response
        response_text = response.choices[0].message.content
        
        # Extract usage statistics
        usage = {
            "prompt_tokens": response.usage.prompt_tokens,
            "completion_tokens": response.usage.completion_tokens,
            "total_tokens": response.usage.total_tokens
        }
        
        return {
            "success": True,
            "prompt": prompt,
            "response": response_text,
            "usage": usage,
            "model": deployment_name,
            "error": None
        }
        
    except Exception as e:
        error_message = str(e)
        
        # Extract more details if available
        if hasattr(e, 'message'):
            error_message = e.message
        elif hasattr(e, 'body') and e.body:
            if isinstance(e.body, dict) and 'message' in e.body:
                error_message = e.body['message']
        
        return {
            "success": False,
            "error": f"OpenAI API Error: {error_message}",
            "prompt": prompt,
            "response": None,
            "usage": None
        }


def summarize_text(
    text: str,
    style: str = "concise",
    **kwargs
) -> dict:
    """
    Summarize text using Azure OpenAI.
    
    Args:
        text: The text to summarize
        style: Summary style - "concise", "detailed", or "bullet_points"
        **kwargs: Additional arguments passed to generate_ai_response
    
    Returns:
        dict with summary response
    """
    style_prompts = {
        "concise": "Provide a brief, concise summary of the following text in 2-3 sentences:",
        "detailed": "Provide a comprehensive summary of the following text, covering all key points:",
        "bullet_points": "Summarize the following text as bullet points highlighting the key information:"
    }
    
    system_message = "You are an expert summarizer. Create clear and accurate summaries."
    prompt = f"{style_prompts.get(style, style_prompts['concise'])}\n\n{text}"
    
    return generate_ai_response(prompt, system_message=system_message, **kwargs)


def explain_text(
    text: str,
    audience: str = "general",
    **kwargs
) -> dict:
    """
    Explain or simplify text using Azure OpenAI.
    
    Args:
        text: The text to explain
        audience: Target audience - "general", "technical", or "beginner"
        **kwargs: Additional arguments passed to generate_ai_response
    
    Returns:
        dict with explanation response
    """
    audience_prompts = {
        "general": "Explain the following in simple, everyday language:",
        "technical": "Provide a technical explanation of the following:",
        "beginner": "Explain the following as if teaching a complete beginner:"
    }
    
    system_message = "You are a skilled teacher who explains complex topics clearly."
    prompt = f"{audience_prompts.get(audience, audience_prompts['general'])}\n\n{text}"
    
    return generate_ai_response(prompt, system_message=system_message, **kwargs)


# Quick test when run directly
if __name__ == "__main__":
    print("Testing Azure OpenAI...")
    print("-" * 50)
    
    # Test basic response
    result = generate_ai_response("What is artificial intelligence in one sentence?")
    
    if result["success"]:
        print(f"✓ Prompt: {result['prompt']}")
        print(f"✓ Response: {result['response']}")
        print(f"✓ Tokens used: {result['usage']['total_tokens']}")
    else:
        print(f"✗ Generation failed: {result['error']}")
