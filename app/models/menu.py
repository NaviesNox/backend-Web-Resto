from sqlalchemy import Column, Integer, String, Float, ForeignKey, Boolean, DateTime
from sqlalchemy.orm import relationship
from datetime import datetime
from app.database import Base


class Menu(Base):
    __tablename__ = "menu"

    id = Column(Integer, primary_key=True, index=True)
    nama = Column(String, nullable=False)
    deskripsi = Column(String)
    harga = Column(Float, nullable=False)
    kategori_id = Column(Integer, ForeignKey("kategori_menu.id"), nullable=False)
    gambar_url = Column(String)
    is_available = Column(Boolean, default=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Relationships
    kategori = relationship("KategoriMenu", back_populates="menu")
    detail_pesanan = relationship("DetailPesanan", back_populates="menu")
    stok_harian = relationship("StokHarian", back_populates="menu", uselist=False)
