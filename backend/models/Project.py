from pydantic import BaseModel

class Project(BaseModel):
    id: int
    name: str
    owner_id: int
    locked: bool = False

class ProjectCreateRequest(BaseModel):
    name: str
    owner_id: int

class User(BaseModel):
    id: int
    name: str
    permissions: list[str]
