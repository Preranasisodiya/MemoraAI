from app.database.database import SessionLocal
from app.models.user import User
from app.models.document import Document
from app.models.document_chunk import DocumentChunk
from app.services.text_chunker import chunk_text


db = SessionLocal()

try:
    document = (
        db.query(Document)
        .filter(Document.id == 3)
        .first()
    )

    if not document:
        print("Document not found")
        raise SystemExit

    chunks = chunk_text(
        document.extracted_text,
        chunk_size=1000,
        overlap=200
    )

    for index, content in enumerate(chunks):

        chunk = DocumentChunk(
            document_id=document.id,
            chunk_index=index,
            content=content
        )

        db.add(chunk)

    db.commit()

    print("Chunks stored successfully")
    print("Total chunks:", len(chunks))

finally:
    db.close()