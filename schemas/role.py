from pydantic import BaseModel
from typing import List
from model import Session, Role

class RoleSchema(BaseModel):
    id: int
    name: str
    description: str

class RoleSearchSchema(BaseModel):
    name: str

class RoleDeletionSchema(BaseModel):
    message: str
    name: str

def role_presentation(role: Role) -> dict:
    return {
        "id": role.id,
        "name": role.name,
        "description": role.description,
    }

def roles_presentation(roles: List[Role]) -> dict:
    return {
        "roles": [role_presentation(role) for role in roles]
    }