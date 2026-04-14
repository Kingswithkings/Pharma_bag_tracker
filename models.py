from sqlalchemy import Column, Integer, String, DateTime
from sqlalchemy.sql import func
from database import Base


class BagRecord(Base):
    __tablename__ = "bag_records"

    id = Column(Integer, primary_key=True, index=True)
    bag_id = Column(String, index=True, nullable=False)
    ward = Column(String, nullable=False)
    status = Column(String, nullable=False, default="in_transit")
    courier = Column(String, nullable=True)
    notes = Column(String, nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())