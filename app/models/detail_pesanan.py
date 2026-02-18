from sqlalchemy import Column, Integer, Float, ForeignKey, String, DateTime
from sqlalchemy.orm import relationship
from datetime import datetime
from app.database import Base


class DetailPesanan(Base):
    __tablename__ = "detail_pesanan"

    id = Column(Integer, primary_key=True, index=True)
    pesanan_id = Column(Integer, ForeignKey("pesanan.id"), nullable=False)
    menu_id = Column(Integer, ForeignKey("menu.id"), nullable=False)
    jumlah = Column(Integer, nullable=False)
    harga_satuan = Column(Float, nullable=False)
    subtotal = Column(Float, nullable=False)
    catatan = Column(String)
    created_at = Column(DateTime, default=datetime.utcnow)

    # Relationships
    pesanan = relationship("Pesanan", back_populates="detail_pesanan")
    menu = relationship("Menu", back_populates="detail_pesanan")
