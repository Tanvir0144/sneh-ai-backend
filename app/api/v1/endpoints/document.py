from fastapi import APIRouter, Depends, UploadFile, File
from sqlalchemy.orm import Session

from app.db import models
from app.schemas.document import DocumentResponse
from app.api.v1 import deps
from app.services import document_service

router = APIRouter()

@router.post("/extract", response_model=DocumentResponse)
def extract_document_text(
    *,
    current_user: models.User = Depends(deps.get_current_user),
    file: UploadFile = File(...)
):
    """
    Extracts all text from an uploaded PDF or TXT file.
    """
    extracted_text = document_service.extract_text_from_file(file)
    return DocumentResponse(extracted_text=extracted_text, filename=file.filename)