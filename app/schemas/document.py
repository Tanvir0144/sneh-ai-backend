from pydantic import BaseModel

class DocumentResponse(BaseModel):
    extracted_text: str
    filename: str