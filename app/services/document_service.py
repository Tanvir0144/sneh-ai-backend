from fastapi import UploadFile, HTTPException, status
import fitz  # PyMuPDF

def extract_text_from_file(file: UploadFile) -> str:
    """
    Extracts text content from an uploaded file (PDF or TXT).
    """
    # Check for content type
    if file.content_type == "application/pdf":
        try:
            # Read file content into memory
            file_bytes = file.file.read()
            # Open PDF from bytes
            pdf_document = fitz.open(stream=file_bytes, filetype="pdf")
            
            text = ""
            for page_num in range(len(pdf_document)):
                page = pdf_document.load_page(page_num)
                text += page.get_text()
            
            pdf_document.close()
            return text
        except Exception as e:
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=f"Error processing PDF file: {e}")

    elif file.content_type == "text/plain":
        try:
            return file.file.read().decode("utf-8")
        except Exception as e:
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=f"Error reading text file: {e}")
    else:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Unsupported file type. Please upload a PDF or a TXT file."
        )