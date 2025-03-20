from typing import List, Dict, Optional
import os

class Project:
    project_counter = 1
    
    def __init__(self, name: str, owner: str):
        self.name = name
        self.owner = owner
        self.is_locked = False
        self.archived = False
        self.project_id = Project.project_counter
        self.ip_list: List[str] = []
        Project.project_counter += 1
    
    def get_project_name(self) -> str:
        return self.name
    
    def get_project_owner(self) -> str:
        return self.owner
    
    def get_project_id(self) -> int:
        return self.project_id
    
    def is_project_locked(self) -> bool:
        return self.is_locked
    
    def set_project_owner(self, new_owner: str, requester: str) -> bool:
        if requester == self.owner:
            self.owner = new_owner
            return True
        return False
    
    def set_project_id(self, new_id: int, requester: str) -> bool:
        if requester == self.owner:
            self.project_id = new_id
            return True
        return False
    
    def set_project_lock(self, lock: bool, requester: str) -> bool:
        if requester == self.owner:
            self.is_locked = lock
            return True
        return False