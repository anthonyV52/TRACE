from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from services.neo4j_service import create_user_node

router = APIRouter()

class UserCreateRequest(BaseModel):
    id: int
    name: str

@router.post("/user/create")
def create_user(request: UserCreateRequest):
    try:
        create_user_node(request.id, request.name)
        return {"message": f"User {request.name} (ID: {request.id}) created in Neo4j"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
