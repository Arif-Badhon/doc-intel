from sqlalchemy import Column, Integer, String, Text, DateTime, Float, ForeignKey
from sqlalchemy.orm import relationship
from datetime import datetime
from src.config.database import Base

# For pgvector support - use the correct import
try:
    from pgvector.sqlalchemy import Vector
except ImportError:
    # Fallback if pgvector not installed
    from sqlalchemy import LargeBinary as Vector

class Document(Base):
    __tablename__ = "documents"
    
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(255), nullable=False)
    content = Column(Text, nullable=False)
    file_path = Column(String(500))
    file_type = Column(String(50))
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    embeddings = relationship("DocumentEmbedding", back_populates="document", cascade="all, delete-orphan")
    classifications = relationship("Classification", back_populates="document", cascade="all, delete-orphan")
    ner_results = relationship("NERResult", back_populates="document", cascade="all, delete-orphan")


class DocumentEmbedding(Base):
    __tablename__ = "document_embeddings"
    
    id = Column(Integer, primary_key=True, index=True)
    document_id = Column(Integer, ForeignKey("documents.id"), nullable=False)
    chunk_index = Column(Integer)
    text = Column(Text)
    embedding = Column(Vector(1536))  # Use Vector from pgvector
    created_at = Column(DateTime, default=datetime.utcnow)
    
    document = relationship("Document", back_populates="embeddings")


class Classification(Base):
    __tablename__ = "classifications"
    
    id = Column(Integer, primary_key=True, index=True)
    document_id = Column(Integer, ForeignKey("documents.id"), nullable=False)
    category = Column(String(100))
    confidence = Column(Float)
    model_version = Column(String(50))
    created_at = Column(DateTime, default=datetime.utcnow)
    
    document = relationship("Document", back_populates="classifications")


class NERResult(Base):
    __tablename__ = "ner_results"
    
    id = Column(Integer, primary_key=True, index=True)
    document_id = Column(Integer, ForeignKey("documents.id"), nullable=False)
    entity_type = Column(String(50))
    entity_text = Column(String(500))
    start_pos = Column(Integer)
    end_pos = Column(Integer)
    confidence = Column(Float)
    created_at = Column(DateTime, default=datetime.utcnow)
    
    document = relationship("Document", back_populates="ner_results")
