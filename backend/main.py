from fastapi import FastAPI, HTTPException, Query
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import os

# Neo4j service functions
from neo4j_service import (
    create_project_node,
    create_user_node,
    link_owner_to_project,
    get_project_node,
    get_project_owner_node,
    update_project_owner,
    update_project_id,
    update_project_lock
)

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",
        "http://127.0.0.1:5173"  # ⚠️ Temporary for testing
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ==== Models ====

class User(BaseModel):
    id: int
    name: str
    permissions: list[str]

class Project(BaseModel):
    id: int
    name: str
    owner_id: int
    locked: bool = False

class ProjectCreateRequest(BaseModel):
    name: str
    owner_id: int

# ==== Project Endpoints under /project ====

@app.get("/project")
def get_all_projects():
    return {"message": "Neo4j doesn't support simple list-all like SQL - use browser or custom Cypher"}

@app.post("/project/create")
def create_project(request: ProjectCreateRequest):
    new_project_id = request.owner_id * 1000 + len(request.name)  # temporary ID logic
    project = Project(id=new_project_id, name=request.name, owner_id=request.owner_id)

    create_user_node(project.owner_id, f"User{project.owner_id}")
    create_project_node(project)
    link_owner_to_project(project.owner_id, project.id)

    return {"message": "Project created and synced to Neo4j", "project_id": project.id}

@app.get("/project/{project_id}/name")
def get_project_name(project_id: int):
    project = get_project_node(project_id)
    return {"project_name": project['name']}

@app.get("/project/{project_id}/owner")
def get_project_owner(project_id: int):
    owner = get_project_owner_node(project_id)
    return {"owner": owner}

@app.get("/project/{project_id}/id")
def get_project_id(project_id: int):
    project = get_project_node(project_id)
    return {"project_id": project['id']}

@app.get("/project/{project_id}/locked")
def is_project_locked(project_id: int):
    project = get_project_node(project_id)
    return {"locked": project['locked']}

@app.post("/project/{project_id}/set_owner")
def set_project_owner(project_id: int, new_owner_id: int, requester_id: int):
    update_project_owner(project_id, new_owner_id)
    return {"message": f"Owner changed to {new_owner_id}"}

@app.post("/project/{project_id}/set_id")
def set_project_id(project_id: int, new_id: int, requester_id: int):
    update_project_id(project_id, new_id)
    return {"message": f"Project ID changed to {new_id}"}

@app.post("/project/{project_id}/set_lock")
def set_project_lock(project_id: int, lock: bool, requester_id: int):
    update_project_lock(project_id, lock)
    return {"message": f"Project lock status changed to {lock}"}

@app.post("/project/import")
def import_project(requester_id: int = Query(..., description="User ID of requester")):
    return {"message": f"Importing project by user {requester_id}"}

@app.get("/project/{project_id}/export")
def export_project(project_id: int, format: str, requester_id: int):
    if format not in ["XML", "CSV"]:
        raise HTTPException(status_code=400, detail="Invalid format")

    project = get_project_node(project_id)
    file_path = f"exports/project_{project_id}.{format.lower()}"
    os.makedirs("exports", exist_ok=True)

    with open(file_path, "w") as file:
        file.write(f"Exported project {project_id} in {format} format.")

    return {"message": "Project exported successfully", "file_path": file_path}

# ==== Run directly ====
if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)