from sqlalchemy import Column, Integer, Float, String, ForeignKey, DateTime, Enum as SQLEnum
from sqlalchemy.orm import relationship
from datetime import datetime
import enum
from app.database import Base


class MetodePembayaran(str, enum.Enum):
    CASH = "cash"
    DEBIT = "debit"
    CREDIT = "credit"
    QRIS = "qris"
    TRANSFER = "transfer"


class Pembayaran(Base):
    __tablename__ = "pembayaran"

    id = Column(Integer, primary_key=True, index=True)
    transaksi_id = Column(Integer, ForeignKey("transaksi.id"), unique=True, nullable=False)
    metode_pembayaran = Column(SQLEnum(MetodePembayaran), nullable=False)
    jumlah_bayar = Column(Float, nullable=False)
    kembalian = Column(Float, default=0)
    created_at = Column(DateTime, default=datetime.utcnow)

    # Relationships
    transaksi = relationship("Transaksi", back_populates="pembayaran")
