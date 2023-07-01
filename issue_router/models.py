from pydantic import BaseModel
from typing import Optional, List


class CreateIssueRequest(BaseModel):
    """Schema for a /create_issue request."""
    title: str
    url: str
    submitter: str
    arax_url: str
    ars_pk: str
    description: str
    reproduction_steps: str
    screenshots: Optional[List[str]] = []
    type: str


class CreateIssueResponse(BaseModel):
    """Schema for a /create_issue response."""
    url: str
