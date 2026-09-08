from pydantic import BaseModel, Field


class TestCaseReworkRequest(BaseModel):
    document_name: str
    current_test_cases: str
    issues: list[str] = Field(default_factory=list)
    required_changes: list[str] = Field(default_factory=list)
    retry_count: int = Field(default=0, ge=0)
