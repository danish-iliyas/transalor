"""
Azure AI Integration - Main Application

This module demonstrates the integration of Azure AI Translator and Azure OpenAI
services in a practical workflow:

Flow: Input Data -> Azure OpenAI (summary) -> Azure Translator (language conversion) -> Final Output
"""

import sys
import json
from translator import translate_text
from openai_client import generate_ai_response, summarize_text

# Fix Windows console encoding
if sys.platform == "win32":
    sys.stdout.reconfigure(encoding='utf-8', errors='replace')


def process_and_translate(
    input_text: str,
    target_language: str = "hi",
    summary_style: str = "concise"
) -> dict:
    """
    Process text through the complete AI pipeline:
    1. Summarize using Azure OpenAI
    2. Translate the summary using Azure Translator
    
    Args:
        input_text: The input text to process
        target_language: Target language code for translation (default: Hindi 'hi')
        summary_style: Style of summary - "concise", "detailed", or "bullet_points"
    
    Returns:
        dict containing all processing results
    """
    print("\n" + "=" * 60)
    print(">>> AZURE AI INTEGRATION PIPELINE")
    print("=" * 60)
    
    result = {
        "input": input_text,
        "target_language": target_language,
        "stages": {}
    }
    
    # Stage 1: Summarize with Azure OpenAI
    print("\n[STAGE 1] Generating Summary with Azure OpenAI...")
    print("-" * 40)
    
    summary_result = summarize_text(input_text, style=summary_style)
    result["stages"]["openai_summary"] = summary_result
    
    if not summary_result["success"]:
        print(f"[ERROR] Summary generation failed: {summary_result['error']}")
        result["success"] = False
        result["error"] = f"OpenAI stage failed: {summary_result['error']}"
        return result
    
    summary = summary_result["response"]
    print(f"[OK] Summary Generated:")
    print(f"   {summary[:200]}..." if len(summary) > 200 else f"   {summary}")
    print(f"   (Tokens used: {summary_result['usage']['total_tokens']})")
    
    # Stage 2: Translate with Azure Translator
    print(f"\n[STAGE 2] Translating to {target_language.upper()} with Azure Translator...")
    print("-" * 40)
    
    translation_result = translate_text(summary, "en", target_language)
    result["stages"]["translator"] = translation_result
    
    if not translation_result["success"]:
        print(f"[ERROR] Translation failed: {translation_result['error']}")
        result["success"] = False
        result["error"] = f"Translator stage failed: {translation_result['error']}"
        return result
    
    translated_text = translation_result["translated_text"]
    print(f"[OK] Translation Complete:")
    print(f"   {translated_text[:200]}..." if len(translated_text) > 200 else f"   {translated_text}")
    
    # Final result
    result["success"] = True
    result["final_output"] = {
        "original_text": input_text,
        "english_summary": summary,
        "translated_summary": translated_text,
        "target_language": target_language
    }
    
    return result


def demo_translator_only():
    """Demonstrate Azure Translator standalone usage."""
    print("\n" + "=" * 60)
    print(">>> AZURE TRANSLATOR DEMO")
    print("=" * 60)
    
    test_texts = [
        ("Hello, how are you today?", "en", "hi"),
        ("Welcome to Azure AI services!", "en", "fr"),
        ("Machine learning is transforming industries.", "en", "es"),
    ]
    
    for text, source, target in test_texts:
        print(f"\n[*] Translating: '{text}'")
        print(f"   From: {source} -> To: {target}")
        
        result = translate_text(text, source, target)
        
        if result["success"]:
            print(f"   [OK] Result: {result['translated_text']}")
        else:
            print(f"   [ERROR] {result['error']}")


def demo_openai_only():
    """Demonstrate Azure OpenAI standalone usage."""
    print("\n" + "=" * 60)
    print(">>> AZURE OPENAI DEMO")
    print("=" * 60)
    
    # Test 1: Simple question
    print("\n[*] Test 1: Simple Question")
    result = generate_ai_response("What are the three primary colors?")
    if result["success"]:
        print(f"   [OK] Response: {result['response']}")
    else:
        print(f"   [ERROR] {result['error']}")
    
    # Test 2: Summarization
    print("\n[*] Test 2: Text Summarization")
    sample_text = """
    Artificial intelligence (AI) is transforming how we live and work. 
    From virtual assistants that help us manage our daily tasks to advanced 
    systems that can diagnose diseases, AI is becoming an integral part of 
    modern life. Machine learning, a subset of AI, allows computers to learn 
    from data without being explicitly programmed. This has led to breakthroughs 
    in image recognition, natural language processing, and autonomous vehicles.
    """
    result = summarize_text(sample_text, style="concise")
    if result["success"]:
        print(f"   [OK] Summary: {result['response']}")
    else:
        print(f"   [ERROR] {result['error']}")


def main():
    """Main function demonstrating the complete Azure AI integration."""
    
    print("\n" + "*" * 60)
    print("    AZURE AI INTEGRATION APPLICATION")
    print("*" * 60)
    
    # Example input text for the full pipeline
    sample_article = """
    Climate change is one of the most pressing challenges facing our planet today. 
    Rising global temperatures are causing widespread environmental changes, including 
    melting ice caps, rising sea levels, and more frequent extreme weather events. 
    Scientists agree that human activities, particularly the burning of fossil fuels, 
    are the primary drivers of these changes. Addressing climate change requires 
    global cooperation and a transition to renewable energy sources. Individuals can 
    also make a difference by reducing their carbon footprint through sustainable 
    practices like using public transportation, conserving energy, and supporting 
    eco-friendly policies.
    """
    
    # Run the full pipeline: OpenAI -> Translator
    print("\n" + ">" * 40)
    print("  RUNNING FULL PIPELINE: OpenAI -> Translator")
    print(">" * 40)
    
    result = process_and_translate(
        input_text=sample_article,
        target_language="hi",  # Translate to Hindi
        summary_style="concise"
    )
    
    # Print final results
    print("\n" + "=" * 60)
    print(">>> FINAL RESULTS")
    print("=" * 60)
    
    if result["success"]:
        print(f"\n[SUCCESS] Pipeline completed successfully!")
        print(f"\n[Original Text (English)]:")
        print(f"   {result['final_output']['original_text'][:150]}...")
        print(f"\n[AI Summary (English)]:")
        print(f"   {result['final_output']['english_summary']}")
        print(f"\n[Translated Summary ({result['final_output']['target_language']})]:")
        print(f"   {result['final_output']['translated_summary']}")
    else:
        print(f"\n[FAILED] Pipeline failed: {result['error']}")
        print("\n[Troubleshooting Tips]:")
        print("   1. Check that your .env file has valid API keys")
        print("   2. Verify the Azure OpenAI endpoint URL is correct")
        print("   3. Ensure the deployment name matches your Azure portal")
    
    # Uncomment to run individual demos:
    # demo_translator_only()
    # demo_openai_only()
    
    return result


if __name__ == "__main__":
    main()
