from pydantic import BaseModel, Field, JsonValue


class APIErrorResponse(BaseModel):
    """Stable error contract shared by every HTTP error response."""

    title: str
    status: int
    code: str
    message: str
    details: dict[str, JsonValue] = Field(default_factory=dict)
