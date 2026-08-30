from pydantic import BaseModel
from ..models.user import User

class UserCreateRequest(BaseModel):
    username: str

class UserDeleteRequest(BaseModel):
    id: int

class UserUpdateRequest(BaseModel):
    id: int
    username: str