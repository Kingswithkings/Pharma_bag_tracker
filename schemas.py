from pydantic import BaseModel, Field
from datetime import datetime
from typing import Optional


class BagCreate(BaseModel):
    bag_id: str = Field(..., example="170")
    ward: str = Field(..., example="21")
    status: str = Field(default="in_transit", example="in_transit")
    courier: Optional[str] = Field(default=None, example="Kings")
    notes: Optional[str] = None


class BagUpdateStatus(BaseModel):
    status: str = Field(..., example="delivered")
    ward: Optional[str] = None
    courier: Optional[str] = None
    notes: Optional[str] = None


class BagResponse(BaseModel):
    id: int
    bag_id: str
    ward: str
    status: str
    courier: Optional[str]
    notes: Optional[str]
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True