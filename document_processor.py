"""
Document Processor Module

Extracts text from PDF and DOCX files for translation.
"""

import os
from typing import Optional


def extract_text_from_pdf(file_path: str) -> dict:
    """
    Extract text from a PDF file.
    
    Args:
        file_path: Path to the PDF file
    
    Returns:
        dict with success status and extracted text
    """
    try:
        import pdfplumber
        
        text_content = []
        
        with pdfplumber.open(file_path) as pdf:
            for page_num, page in enumerate(pdf.pages, 1):
                page_text = page.extract_text()
                if page_text:
                    text_content.append(f"--- Page {page_num} ---\n{page_text}")
        
        full_text = "\n\n".join(text_content)
        
        return {
            "success": True,
            "text": full_text,
            "page_count": len(text_content),
            "file_type": "pdf",
            "error": None
        }
        
    except Exception as e:
        return {
            "success": False,
            "text": None,
            "error": f"Failed to extract PDF text: {str(e)}"
        }


def extract_text_from_docx(file_path: str) -> dict:
    """
    Extract text from a DOCX file.
    
    Args:
        file_path: Path to the DOCX file
    
    Returns:
        dict with success status and extracted text
    """
    try:
        from docx import Document
        
        doc = Document(file_path)
        paragraphs = [para.text for para in doc.paragraphs if para.text.strip()]
        full_text = "\n\n".join(paragraphs)
        
        return {
            "success": True,
            "text": full_text,
            "paragraph_count": len(paragraphs),
            "file_type": "docx",
            "error": None
        }
        
    except Exception as e:
        return {
            "success": False,
            "text": None,
            "error": f"Failed to extract DOCX text: {str(e)}"
        }


def extract_text_from_txt(file_path: str) -> dict:
    """
    Read text from a plain text file.
    
    Args:
        file_path: Path to the text file
    
    Returns:
        dict with success status and text content
    """
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            text = f.read()
        
        return {
            "success": True,
            "text": text,
            "file_type": "txt",
            "error": None
        }
        
    except Exception as e:
        return {
            "success": False,
            "text": None,
            "error": f"Failed to read text file: {str(e)}"
        }


def extract_text(file_path: str, file_type: Optional[str] = None) -> dict:
    """
    Extract text from a document based on file type.
    
    Args:
        file_path: Path to the document
        file_type: Optional file type override ('pdf', 'docx', 'txt')
    
    Returns:
        dict with extracted text or error
    """
    if not os.path.exists(file_path):
        return {
            "success": False,
            "text": None,
            "error": f"File not found: {file_path}"
        }
    
    # Determine file type from extension if not provided
    if not file_type:
        _, ext = os.path.splitext(file_path)
        file_type = ext.lower().lstrip('.')
    
    # Route to appropriate extractor
    extractors = {
        'pdf': extract_text_from_pdf,
        'docx': extract_text_from_docx,
        'txt': extract_text_from_txt,
        'text': extract_text_from_txt,
    }
    
    extractor = extractors.get(file_type)
    
    if not extractor:
        return {
            "success": False,
            "text": None,
            "error": f"Unsupported file type: {file_type}. Supported: pdf, docx, txt"
        }
    
    return extractor(file_path)


# Quick test when run directly
if __name__ == "__main__":
    print("Document Processor Module")
    print("Supported formats: PDF, DOCX, TXT")
