from sqlalchemy import Column, Integer, Date, ForeignKey
from sqlalchemy.orm import relationship
from datetime import date
from app.database import Base


class StokHarian(Base):
    __tablename__ = "stok_harian"

    id = Column(Integer, primary_key=True, index=True)
    menu_id = Column(Integer, ForeignKey("menu.id"), unique=True, nullable=False)
    tanggal = Column(Date, default=date.today)
    stok_tersedia = Column(Integer, nullable=False, default=0)
    stok_terjual = Column(Integer, default=0)

    # Relationships
    menu = relationship("Menu", back_populates="stok_harian")
