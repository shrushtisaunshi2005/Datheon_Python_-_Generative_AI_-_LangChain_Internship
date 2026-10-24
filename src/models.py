from pydantic import BaseModel, Field
from typing import List, Optional


class ResumeData(BaseModel):
    name: str = Field(description="Full name of the person")
    email: Optional[str] = Field(default=None, description="Email address")
    phone: Optional[str] = Field(default=None, description="Phone number")
    job_title: Optional[str] = Field(default=None, description="Current or most relevant job title")
    experience_years: Optional[float] = Field(
        default=None,
        description="Total years of professional experience"
    )
    skills: List[str] = Field(
        default_factory=list,
        description="List of technical or professional skills"
    )