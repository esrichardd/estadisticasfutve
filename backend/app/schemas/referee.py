from datetime import datetime
from typing import Optional
from uuid import UUID

from pydantic import BaseModel, ConfigDict


class RefereeBase(BaseModel):
    name: str
    nationality: Optional[str] = None
    is_active: bool = True


class RefereeCreate(RefereeBase):
    pass


class RefereeUpdate(BaseModel):
    name: Optional[str] = None
    nationality: Optional[str] = None
    is_active: Optional[bool] = None


class RefereeResponse(RefereeBase):
    id: UUID
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)
