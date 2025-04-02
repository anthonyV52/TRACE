import json
from fastapi import File, UploadFile
from Project import project
from typing import List, Dict, Optional
import os

class projectManager(project):
    def __init__(self, name: str, owner: str):
        super().__init__(name, owner)
        self.project_store: List[project] = []

    def create_project(self, name: str, owner: str) -> Optional[project]:
        if name and owner:
            new_project = project(name, owner)
            self.project_store.append(new_project)
            return new_project
        return None

    def delete_project(self, project: project, requester: str):
        if project and requester == project.owner:
            self.project_store = [p for p in self.project_store if p != project]
    
    async def import_project(self, requester: str, file: UploadFile = File(...)):
        if not file.filename.endswith(".json"):
            return None
        
        content = await file.read()

        try:
            data = json.loads(content)
            validated_project = ProjectImportSchema(**data)
        except Exception as e:
            return None

        return validated_project

    
    def export_project(self, project: project, format: str, requester: str) -> Optional[str]:
        if project and requester and format.lower() in ("csv", "xml"):
            return f"{project.name}.{format.lower()}"
        return None
    
    def archive_project(self, project: project, requester: str) -> bool:
        if project and requester:
            project.archived = True
            return True
        return False
    
    def display_projects(self, filters: Dict[str, str], requester: str) -> List[project]:
        return [p for p in self.project_store if p.owner == requester]
