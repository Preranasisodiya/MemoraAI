from datetime import datetime

from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Text
from sqlalchemy.orm import relationship

from app.database.database import Base


class Document(Base):
    __tablename__ = "documents"

    id = Column(Integer, primary_key=True, index=True)

    user_id = Column(
        Integer,
        ForeignKey("users.id"),
        nullable=False
    )

    title = Column(String(255), nullable=False)

    filename = Column(String(255), nullable=False)

    file_type = Column(String(50), nullable=False)

    file_path = Column(String(500), nullable=False)

    file_hash = Column(String(64), nullable=False, index=True)

    extracted_text = Column(Text, nullable=True)

    created_at = Column(
        DateTime,
        default=datetime.utcnow
    )

    updated_at = Column(
        DateTime,
        default=datetime.utcnow,
        onupdate=datetime.utcnow
    )

    user = relationship("User", back_populates="documents")