from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.database.database import get_db
from app.models.document import Document
from app.models.user import User
from app.schemas.document import DocumentCreate, DocumentResponse
from app.services.auth_dependency import get_current_user
from app.services.document_extractor import extract_text

import hashlib
import shutil
from pathlib import Path

from fastapi import (
    APIRouter,
    Depends,
    HTTPException,
    UploadFile,
    File
)

router = APIRouter(
    prefix="/api/documents",
    tags=["Documents"]
)


@router.post(
    "/",
    response_model=DocumentResponse
)
def create_document(
    data: DocumentCreate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    # Create document for the authenticated user
    new_document = Document(
        user_id=current_user.id,
        title=data.title,
        filename=data.filename,
        file_type=data.file_type,
        file_path=data.file_path
    )

    db.add(new_document)
    db.commit()
    db.refresh(new_document)

    return new_document

@router.post("/upload")
def upload_document(
    file: UploadFile = File(...),
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    # Allowed file types
    allowed_extensions = {
        ".pdf",
        ".docx",
        ".txt"
    }

    # Make sure filename exists
    if not file.filename:
        raise HTTPException(
            status_code=400,
            detail="Filename is required"
        )

    original_filename = file.filename

    # Get file extension
    file_extension = Path(
        original_filename
    ).suffix.lower()

    # Validate file type
    if file_extension not in allowed_extensions:
        raise HTTPException(
            status_code=400,
            detail="Only PDF, DOCX, and TXT files are allowed"
        )

    # Read file contents
    file_contents = file.file.read()

    # Generate SHA-256 hash
    file_hash = hashlib.sha256(
        file_contents
    ).hexdigest()

    # Check whether this exact file already exists
    # for the current user
    existing_document = (
        db.query(Document)
        .filter(
            Document.user_id == current_user.id,
            Document.file_hash == file_hash
        )
        .first()
    )

    if existing_document:
        raise HTTPException(
            status_code=409,
            detail="This file has already been uploaded"
        )

    # Create user-specific upload directory
    upload_directory = Path(
        f"uploads/{current_user.id}"
    )

    upload_directory.mkdir(
        parents=True,
        exist_ok=True
    )

    # Generate unique stored filename
    stored_filename = (
        f"{file_hash}{file_extension}"
    )

    file_path = (
        upload_directory /
        stored_filename
    )

    # Save actual uploaded file
    with open(file_path, "wb") as buffer:
        buffer.write(file_contents)

    # Extract text from the saved document
    try:
        extracted_text = extract_text(
            str(file_path),
            file_extension.replace(".", "")
        )
    except Exception as e:
        # Remove the file if text extraction fails
        if file_path.exists():
            file_path.unlink()

        raise HTTPException(
            status_code=500,
            detail=f"Failed to extract document text: {str(e)}"
        )

    # Create database record
    new_document = Document(
        user_id=current_user.id,
        title=Path(original_filename).stem,
        filename=original_filename,
        file_type=file_extension.replace(".", ""),
        file_path=str(file_path),
        file_hash=file_hash,
        extracted_text=extracted_text
    )

    db.add(new_document)
    db.commit()
    db.refresh(new_document)

    return {
        "message": "Document uploaded successfully",
        "document_id": new_document.id,
        "user_id": new_document.user_id,
        "filename": new_document.filename,
        "file_type": new_document.file_type,
        "file_path": new_document.file_path,
        "file_hash": new_document.file_hash,
        "text_length": len(extracted_text)
    }