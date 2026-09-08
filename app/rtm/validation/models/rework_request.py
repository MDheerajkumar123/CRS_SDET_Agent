
from pydantic import BaseModel, Field


class RTMReworkRequest(BaseModel):
    document_name: str
    current_rtm: str
    issues: list[str] = Field(default_factory=list)
    required_changes: list[str] = Field(default_factory=list)
    retry_count: int = Field(default=0, ge=0)
