from uuid import UUID, uuid4

from pydantic import BaseModel, Field

class UserCreated(BaseModel):

    name: str
    id: UUID = Field(default_factory=uuid4)
