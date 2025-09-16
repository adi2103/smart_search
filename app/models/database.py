from sqlalchemy import Column, Integer, String, Text, DateTime, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.sql import func
from pgvector.sqlalchemy import Vector

Base = declarative_base()

class Tenant(Base):
    __tablename__ = "tenants"
    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)

class Client(Base):
    __tablename__ = "clients"
    id = Column(Integer, primary_key=True)
    tenant_id = Column(Integer, ForeignKey("tenants.id"), nullable=False)
    first_name = Column(String)
    last_name = Column(String)
    email = Column(String, unique=True)

class Document(Base):
    __tablename__ = "documents"
    id = Column(Integer, primary_key=True)
    tenant_id = Column(Integer, ForeignKey("tenants.id"), nullable=False)
    client_id = Column(Integer, ForeignKey("clients.id"), nullable=False)
    title = Column(String, nullable=False)
    content = Column(Text, nullable=False)
    summary = Column(Text)
    created_at = Column(DateTime, server_default=func.now())
    content_embedding = Column(Vector(384))

class MeetingNote(Base):
    __tablename__ = "meeting_notes"
    id = Column(Integer, primary_key=True)
    tenant_id = Column(Integer, ForeignKey("tenants.id"), nullable=False)
    client_id = Column(Integer, ForeignKey("clients.id"), nullable=False)
    content = Column(Text, nullable=False)
    summary = Column(Text)
    created_at = Column(DateTime, server_default=func.now())
    content_embedding = Column(Vector(384))
