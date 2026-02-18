from sqlalchemy import Column, Integer, Float, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from datetime import datetime
from app.database import Base


class Transaksi(Base):
    __tablename__ = "transaksi"

    id = Column(Integer, primary_key=True, index=True)
    pesanan_id = Column(Integer, ForeignKey("pesanan.id"), unique=True, nullable=False)
    total_harga = Column(Float, nullable=False)
    pajak = Column(Float, default=0)
    diskon = Column(Float, default=0)
    total_bayar = Column(Float, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Relationships
    pesanan = relationship("Pesanan", back_populates="transaksi")
    pembayaran = relationship("Pembayaran", back_populates="transaksi", uselist=False)
