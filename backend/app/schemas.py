from datetime import date, datetime
from enum import StrEnum
from typing import Optional

from pydantic import BaseModel, Field


class JobStatus(StrEnum):
    SAVED = "saved"
    APPLIED = "applied"
    INTERVIEW = "interview"
    OFFER = "offer"
    REJECTED = "rejected"


class JobBase(BaseModel):
    company: str = Field(min_length=1, max_length=150)
    role: str = Field(min_length=1, max_length=150)
    location: Optional[str] = Field(default=None, max_length=120)
    salary_min: Optional[int] = Field(default=None, ge=0)
    salary_max: Optional[int] = Field(default=None, ge=0)
    status: JobStatus = JobStatus.SAVED
    source_url: Optional[str] = Field(default=None, max_length=500)
    notes: Optional[str] = Field(default=None, max_length=2_000)
    applied_on: Optional[date] = None


class JobCreate(JobBase):
    pass


class JobUpdate(BaseModel):
    company: Optional[str] = Field(default=None, min_length=1, max_length=150)
    role: Optional[str] = Field(default=None, min_length=1, max_length=150)
    location: Optional[str] = Field(default=None, max_length=120)
    salary_min: Optional[int] = Field(default=None, ge=0)
    salary_max: Optional[int] = Field(default=None, ge=0)
    status: Optional[JobStatus] = None
    source_url: Optional[str] = Field(default=None, max_length=500)
    notes: Optional[str] = Field(default=None, max_length=2_000)
    applied_on: Optional[date] = None


class JobRead(JobBase):
    id: int
    created_at: datetime
    updated_at: datetime
