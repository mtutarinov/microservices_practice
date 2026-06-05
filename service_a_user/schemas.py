import uuid

from pydantic import BaseModel

class UserCreated(BaseModel):

    name: str
    id: str = str(uuid.uuid4())
