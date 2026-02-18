from sqlalchemy import Column, Integer, String, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from datetime import datetime
from app.database import Base


class Karyawan(Base):
    __tablename__ = "karyawan"

    id = Column(Integer, primary_key=True, index=True)
    nama = Column(String, nullable=False)
    alamat = Column(String)
    no_telepon = Column(String)
    posisi = Column(String, nullable=False)
    user_id = Column(Integer, ForeignKey("users.id"), unique=True, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Relationships
    user = relationship("User", back_populates="karyawan")
    pesanan = relationship("Pesanan", back_populates="karyawan")
