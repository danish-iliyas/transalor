"""
Azure AI Translator Integration Module

This module provides a reusable function to translate text using
Azure Cognitive Services Translator API.

Authentication: API Key (Ocp-Apim-Subscription-Key + Region header)
Region: Central India
"""

import os
import requests
import uuid
from dotenv import load_dotenv
from typing import Optional

# Load environment variables
load_dotenv()


def translate_text(
    text: str,
    source_lang: str,
    target_lang: str,
    api_key: Optional[str] = None,
    region: Optional[str] = None,
    endpoint: Optional[str] = None
) -> dict:
    """
    Translate text from source language to target language using Azure Translator.
    
    Args:
        text: The text to translate
        source_lang: Source language code (e.g., 'en', 'hi', 'fr')
        target_lang: Target language code (e.g., 'hi', 'en', 'es')
        api_key: Optional API key (defaults to env variable)
        region: Optional region (defaults to env variable)
        endpoint: Optional endpoint (defaults to env variable)
    
    Returns:
        dict containing:
            - success: bool indicating if translation succeeded
            - original_text: the input text
            - translated_text: the translated text (if successful)
            - source_language: detected/specified source language
            - target_language: target language
            - error: error message (if failed)
    
    Example:
        >>> result = translate_text("Hello, world!", "en", "hi")
        >>> print(result['translated_text'])
    """
    
    # Get configuration from environment or parameters
    api_key = api_key or os.getenv("AZURE_TRANSLATOR_KEY")
    region = region or os.getenv("AZURE_TRANSLATOR_REGION", "centralindia")
    endpoint = endpoint or os.getenv("AZURE_TRANSLATOR_ENDPOINT", "https://api.cognitive.microsofttranslator.com/")
    
    # Validate configuration
    if not api_key:
        return {
            "success": False,
            "error": "Missing AZURE_TRANSLATOR_KEY. Please set it in .env file.",
            "original_text": text,
            "translated_text": None,
            "source_language": source_lang,
            "target_language": target_lang
        }
    
    # Build the API URL
    path = "/translate"
    api_version = "3.0"
    url = f"{endpoint.rstrip('/')}{path}"
    
    # Query parameters
    params = {
        "api-version": api_version,
        "from": source_lang,
        "to": target_lang
    }
    
    # Request headers
    headers = {
        "Ocp-Apim-Subscription-Key": api_key,
        "Ocp-Apim-Subscription-Region": region,
        "Content-Type": "application/json",
        "X-ClientTraceId": str(uuid.uuid4())
    }
    
    # Request body
    body = [{"text": text}]
    
    try:
        # Make the API request
        response = requests.post(url, params=params, headers=headers, json=body, timeout=30)
        response.raise_for_status()
        
        # Parse response
        result = response.json()
        
        if result and len(result) > 0:
            translation = result[0]
            translated_text = translation["translations"][0]["text"]
            
            return {
                "success": True,
                "original_text": text,
                "translated_text": translated_text,
                "source_language": source_lang,
                "target_language": target_lang,
                "detected_language": translation.get("detectedLanguage", {}).get("language"),
                "error": None
            }
        else:
            return {
                "success": False,
                "error": "Empty response from Translator API",
                "original_text": text,
                "translated_text": None,
                "source_language": source_lang,
                "target_language": target_lang
            }
            
    except requests.exceptions.HTTPError as e:
        error_msg = f"HTTP Error: {e.response.status_code}"
        try:
            error_detail = e.response.json()
            if "error" in error_detail:
                error_msg = f"{error_msg} - {error_detail['error'].get('message', '')}"
        except:
            pass
        
        return {
            "success": False,
            "error": error_msg,
            "original_text": text,
            "translated_text": None,
            "source_language": source_lang,
            "target_language": target_lang
        }
        
    except requests.exceptions.RequestException as e:
        return {
            "success": False,
            "error": f"Request failed: {str(e)}",
            "original_text": text,
            "translated_text": None,
            "source_language": source_lang,
            "target_language": target_lang
        }


def get_supported_languages() -> dict:
    """
    Get list of supported languages from Azure Translator.
    
    Returns:
        dict containing supported languages for translation
    """
    endpoint = os.getenv("AZURE_TRANSLATOR_ENDPOINT", "https://api.cognitive.microsofttranslator.com/")
    url = f"{endpoint.rstrip('/')}/languages?api-version=3.0&scope=translation"
    
    try:
        response = requests.get(url, timeout=30)
        response.raise_for_status()
        return {"success": True, "languages": response.json().get("translation", {})}
    except Exception as e:
        return {"success": False, "error": str(e), "languages": {}}


# Quick test when run directly
if __name__ == "__main__":
    print("Testing Azure Translator...")
    print("-" * 50)
    
    # Test translation
    result = translate_text("Hello, how are you today?", "en", "hi")
    
    if result["success"]:
        print(f"✓ Original ({result['source_language']}): {result['original_text']}")
        print(f"✓ Translated ({result['target_language']}): {result['translated_text']}")
    else:
        print(f"✗ Translation failed: {result['error']}")
