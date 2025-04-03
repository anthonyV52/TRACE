from fastapi import APIRouter, HTTPException, Query
from models.ProjectManager import ProjectManager
from typing import List, Tuple
from services.neo4j_service import get_project_node, delete_project_node, user_owns_project, update_project_lock,get_project_node
from neo4j_driver import get_driver
from pydantic import BaseModel



router = APIRouter()

class LockToggleRequest(BaseModel):
    lock: bool

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

@router.post("/project/{project_id}/lock")
def toggle_project_lock(project_id: str, data: LockToggleRequest, requester_id: int = Query(...)):
    project = get_project_node(project_id)
    
    if not user_owns_project(requester_id, project_id):
        raise HTTPException(status_code=403, detail="Only the owner can modify lock state.")

    update_project_lock(project_id, data.lock)

    return {"message": f"Project '{project_id}' is now {'locked' if data.lock else 'unlocked'}."}

@router.get("/project_manager/export/{name}")
def export_project(name: str):
    project = project_store.get(name)
    if not project:
        raise HTTPException(status_code=404, detail="Project not found.")
    return project.model_dump()

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

@router.get("/neo4j/people")
def get_people():
    driver = get_driver()
    query = "MATCH (p:Person) RETURN p.name AS name, p.age AS age"
    try:
        with driver.session() as session:
            result = session.run(query)
            people = [{"name": record["name"], "age": record["age"]} for record in result]
        return {"people": people}
    except Exception as e:
        return {"error": str(e)}
