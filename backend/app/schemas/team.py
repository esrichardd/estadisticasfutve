from datetime import datetime
from typing import Optional
from uuid import UUID

from pydantic import BaseModel, ConfigDict


class TeamBase(BaseModel):
    name: str
    short_name: Optional[str] = None
    abbreviation: Optional[str] = None
    city: Optional[str] = None
    stadium: Optional[str] = None
    logo_url: Optional[str] = None
    founded_year: Optional[int] = None
    is_active: bool = True


class TeamCreate(TeamBase):
    pass


class TeamUpdate(BaseModel):
    name: Optional[str] = None
    short_name: Optional[str] = None
    abbreviation: Optional[str] = None
    city: Optional[str] = None
    stadium: Optional[str] = None
    logo_url: Optional[str] = None
    founded_year: Optional[int] = None
    is_active: Optional[bool] = None


class TeamResponse(TeamBase):
    id: UUID
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)
