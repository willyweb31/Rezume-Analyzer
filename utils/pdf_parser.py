from pdfminer.high_level import extract_text
from pdfminer.layout import LAParams
import PyPDF2
import io
import os
import re

def extract_text_from_pdf(pdf_path):
    """
    Extracts text from a PDF file using multiple methods for maximum coverage.
    Args:
        pdf_path (str): Path to the PDF file.
    Returns:
        str: Extracted text.
    """
    print(f"=== PDF EXTRACTION DEBUG ===")
    print(f"PDF file size: {os.path.getsize(pdf_path)} bytes")
    
    all_texts = []
    
    # Method 1: PDFMiner with different parameters
    try:
        # Try with default parameters
        text1 = extract_text(pdf_path)
        all_texts.append(("PDFMiner Default", text1))
        print(f"PDFMiner Default: {len(text1)} characters")
        
        # Try with optimized parameters
        laparams = LAParams(
            line_margin=0.5,
            word_margin=0.1,
            char_margin=2.0,
            boxes_flow=0.5,
            detect_vertical=True
        )
        text2 = extract_text(pdf_path, laparams=laparams)
        all_texts.append(("PDFMiner Optimized", text2))
        print(f"PDFMiner Optimized: {len(text2)} characters")
        
    except Exception as e:
        print(f"PDFMiner failed: {e}")
    
    # Method 2: PyPDF2
    try:
        with open(pdf_path, 'rb') as file:
            pdf_reader = PyPDF2.PdfReader(file)
            text_pdf2 = ""
            for i, page in enumerate(pdf_reader.pages):
                page_text = page.extract_text()
                text_pdf2 += f"\n--- PAGE {i+1} ---\n" + page_text + "\n"
            all_texts.append(("PyPDF2", text_pdf2))
            print(f"PyPDF2: {len(text_pdf2)} characters")
    except Exception as e:
        print(f"PyPDF2 failed: {e}")
    
    # Method 3: PyMuPDF (if available) - DISABLED due to linter issues
    # try:
    #     doc = fitz.open(pdf_path)
    #     text_mupdf = ""
    #     for i in range(len(doc)):
    #         page = doc[i]
    #         text_mupdf += f"\n--- PAGE {i+1} ---\n" + page.get_text() + "\n"
    #     doc.close()
    #     all_texts.append(("PyMuPDF", text_mupdf))
    #     print(f"PyMuPDF: {len(text_mupdf)} characters")
    # except Exception as e:
    #     print(f"PyMuPDF failed: {e}")
    
    # Find the method that extracted the most text
    best_text = ""
    best_method = "None"
    best_length = 0
    
    for method, text in all_texts:
        if text and len(text) > best_length:
            best_text = text
            best_method = method
            best_length = len(text)
    
    print(f"Best extraction method: {best_method} ({best_length} characters)")
    
    # Clean up the best text
    if best_text:
        # Remove page markers and excessive formatting
        cleaned_text = best_text
        
        # Remove page markers like "--- PAGE 1 ---"
        cleaned_text = re.sub(r'--- PAGE \d+ ---', '', cleaned_text)
        
        # Remove excessive whitespace but preserve meaningful line breaks
        lines = cleaned_text.split('\n')
        cleaned_lines = []
        for line in lines:
            line = line.strip()
            if line and len(line) > 2:  # Only keep non-empty lines with meaningful content
                cleaned_lines.append(line)
        
        # Join with single spaces, but preserve some structure
        final_text = ' '.join(cleaned_lines)
        
        # Remove common PDF artifacts
        final_text = final_text.replace('\x00', '')  # Remove null characters
        final_text = final_text.replace('\r', ' ')   # Replace carriage returns
        final_text = re.sub(r'\s+', ' ', final_text)  # Normalize whitespace
        
        print(f"Final cleaned text length: {len(final_text)}")
        print(f"Text preview (first 500 chars): {final_text[:500]}...")
        print(f"Text preview (last 200 chars): ...{final_text[-200:]}")
        
        return final_text
    else:
        print("No text could be extracted from PDF using any method")
        return "" 