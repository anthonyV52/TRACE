from fastapi import APIRouter, HTTPException, Query
from models.Project import Project, ProjectCreateRequest
from services.neo4j_service import (
    create_project_node, create_user_node, link_owner_to_project,
    get_project_node, get_project_owner_node, link_user_access_to_project,
    update_project_owner, update_project_id, update_project_lock,
    get_all_projects
)

router = APIRouter(prefix="/project", tags=["Project"])

@router.get("")
def list_projects():
    return get_all_projects()

@router.post("/create")
def create_project(request: ProjectCreateRequest):
    if request.owner_id != 1:
        raise HTTPException(status_code=403, detail="Only Lead Analyst can create projects")

    new_project_id = request.owner_id * 1000 + len(request.name)
    project = Project(id=new_project_id, name=request.name, owner_id=request.owner_id)
    create_user_node(project.owner_id, f"User{project.owner_id}")
    create_project_node(project)
    link_owner_to_project(project.owner_id, project.id)
    return {"message": "Project created and synced to Neo4j", "project_id": project.id}

@router.get("/{project_id}")
def get_full_project(project_id: int, requester_id: int = Query(...)):
    project = get_project_node(project_id)
    owner = get_project_owner_node(project_id)

    # Log access for non-owners
    if requester_id != project["owner_id"]:
        link_user_access_to_project(requester_id, project_id)

    return {
        "project": project,
        "owner": owner
    }

@router.get("/{project_id}/name")
def get_name(project_id: int):
    return {"project_name": get_project_node(project_id)["name"]}

@router.get("/{project_id}/owner")
def get_owner(project_id: int):
    return {"owner": get_project_owner_node(project_id)}

@router.get("/{project_id}/id")
def get_id(project_id: int):
    return {"project_id": get_project_node(project_id)["id"]}

@router.get("/{project_id}/locked")
def get_locked(project_id: int):
    return {"locked": get_project_node(project_id)["locked"]}

@router.post("/{project_id}/set_owner")
def set_owner(project_id: int, new_owner_id: int, requester_id: int):
    update_project_owner(project_id, new_owner_id)
    return {"message": f"Owner changed to {new_owner_id}"}

@router.post("/{project_id}/set_id")
def set_id(project_id: int, new_id: int, requester_id: int):
    update_project_id(project_id, new_id)
    return {"message": f"Project ID changed to {new_id}"}

@router.post("/{project_id}/set_lock")
def set_lock(project_id: int, lock: bool, requester_id: int):
    update_project_lock(project_id, lock)
    return {"message": f"Project lock status changed to {lock}"}

@router.post("/import")
def import_project(requester_id: int = Query(..., description="User ID of requester")):
    return {"message": f"Importing project by user {requester_id}"}

@router.get("/{project_id}/export")
def export_project(project_id: int, format: str, requester_id: int):
    if format not in ["XML", "CSV"]:
        raise HTTPException(status_code=400, detail="Invalid format")

    project = get_project_node(project_id)
    file_path = f"exports/project_{project_id}.{format.lower()}"
    import os
    os.makedirs("exports", exist_ok=True)

    with open(file_path, "w") as file:
        file.write(f"Exported project {project_id} in {format} format.")

    return {"message": "Project exported successfully", "file_path": file_path}
