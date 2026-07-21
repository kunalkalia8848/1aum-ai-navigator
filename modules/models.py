from pydantic import BaseModel, Field


class ExecutiveSummary(BaseModel):
    current_state: str
    top_strengths: list[str] = Field(min_length=1, max_length=3)
    key_gaps: list[str] = Field(min_length=1, max_length=3)
    priority_use_cases: list[str] = Field(min_length=1, max_length=3)
    immediate_actions: list[str] = Field(min_length=1, max_length=5)
    limitations: list[str] = Field(min_length=1, max_length=3)