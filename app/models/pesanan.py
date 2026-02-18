from sqlalchemy import Column, Integer, String, ForeignKey, DateTime, Enum as SQLEnum
from sqlalchemy.orm import relationship
from datetime import datetime
import enum
from app.database import Base


class StatusPesanan(str, enum.Enum):
    PENDING = "pending"
    PROCESSING = "processing"
    COMPLETED = "completed"
    CANCELLED = "cancelled"


class Pesanan(Base):
    __tablename__ = "pesanan"

    id = Column(Integer, primary_key=True, index=True)
    meja_id = Column(Integer, ForeignKey("meja.id"), nullable=False)
    karyawan_id = Column(Integer, ForeignKey("karyawan.id"), nullable=False)
    nama_pelanggan = Column(String, nullable=True)
    status = Column(SQLEnum(StatusPesanan), default=StatusPesanan.PENDING)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Relationships
    meja = relationship("Meja", back_populates="pesanan")
    karyawan = relationship("Karyawan", back_populates="pesanan")
    detail_pesanan = relationship("DetailPesanan", back_populates="pesanan", cascade="all, delete-orphan")
    transaksi = relationship("Transaksi", back_populates="pesanan", uselist=False)
