from sqlalchemy import Column, Integer, String, Boolean, DateTime, Enum as SQLEnum
from sqlalchemy.orm import relationship
from datetime import datetime
import enum
from app.database import Base


class StatusMeja(str, enum.Enum):
    TERSEDIA = "tersedia"
    TERISI = "terisi"
    RESERVED = "reserved"


class Meja(Base):
    __tablename__ = "meja"

    id = Column(Integer, primary_key=True, index=True)
    nomor_meja = Column(String, unique=True, nullable=False)
    kapasitas = Column(Integer, nullable=False)
    status = Column(SQLEnum(StatusMeja), default=StatusMeja.TERSEDIA)
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Relationships
    pesanan = relationship("Pesanan", back_populates="meja")
