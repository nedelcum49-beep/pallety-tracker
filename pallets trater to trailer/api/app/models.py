
from sqlalchemy import Column, Integer, String, Boolean, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from datetime import datetime
from .db import Base

class Trailer(Base):
    __tablename__ = "trailers"
    id = Column(Integer, primary_key=True)
    code = Column(String, unique=True)
    status = Column(String, default="OPEN")
    pallets = relationship("Pallet", back_populates="trailer")

class Pallet(Base):
    __tablename__ = "pallets"
    id = Column(Integer, primary_key=True)
    barcode = Column(String, unique=True, index=True)
    trailer_id = Column(Integer, ForeignKey("trailers.id"))
    is_active = Column(Boolean, default=True)
    trailer = relationship("Trailer", back_populates="pallets")

class Audit(Base):
    __tablename__ = "audit"
    id = Column(Integer, primary_key=True)
    action = Column(String)
    operator = Column(String)
    timestamp = Column(DateTime, default=datetime.utcnow)
