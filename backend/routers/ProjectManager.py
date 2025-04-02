from fastapi import APIRouter, HTTPException
from models.ProjectManager import ProjectManager
from typing import Optional, List, Tuple

router = APIRouter()

# Temporary in-memory project store
project_store: dict[str, ProjectManager] = {}

@router.post("/project_manager/create")
def create_project(pm: ProjectManager):
    if pm.name in project_store:
        raise HTTPException(status_code=400, detail="Project already exists.")
    project_store[pm.name] = pm
    return {"success": True, "message": f"Project '{pm.name}' created."}

@router.get("/project_manager/load/{name}")
def load_project(name: str):
    project = project_store.get(name)
    if not project:
        raise HTTPException(status_code=404, detail="Project not found.")
    return project

@router.delete("/project_manager/delete/{name}")
def delete_project(name: str, requester: str):
    project = project_store.get(name)
    if not project:
        raise HTTPException(status_code=404, detail="Project not found.")
    if project.locked:
        raise HTTPException(status_code=403, detail="Project is locked.")
    if project.owner != requester:
        raise HTTPException(status_code=403, detail="Only the owner can delete the project.")
    del project_store[name]
    return {"success": True, "message": f"Project '{name}' deleted."}

@router.post("/project_manager/lock/{name}")
def lock_project(name: str, requester: str):
    project = project_store.get(name)
    if not project:
        raise HTTPException(status_code=404, detail="Project not found.")
    if project.owner != requester:
        raise HTTPException(status_code=403, detail="Only the owner can lock the project.")
    project.locked = True
    return {"success": True, "message": f"Project '{name}' locked."}

@router.get("/project_manager/export/{name}")
def export_project(name: str):
    project = project_store.get(name)
    if not project:
        raise HTTPException(status_code=404, detail="Project not found.")
    return project.dict()

@router.post("/project_manager/import")
def import_project(pm: ProjectManager):
    project_store[pm.name] = pm
    return {"success": True, "message": f"Project '{pm.name}' imported."}

@router.post("/project_manager/import_ip/{name}")
def import_ip_list(name: str, ip_list: List[Tuple[str, int]]):
    project = project_store.get(name)
    if not project:
        raise HTTPException(status_code=404, detail="Project not found.")
    project.IPList = ip_list
    return {"success": True, "message": "IP list updated."}

@router.get("/project_manager/read_ip/{name}")
def read_ip_list(name: str):
    project = project_store.get(name)
    if not project:
        raise HTTPException(status_code=404, detail="Project not found.")
    return {"IPList": project.IPList}
