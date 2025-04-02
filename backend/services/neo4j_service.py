from neo4j import GraphDatabase
from pydantic import BaseModel
from typing import List, Tuple, Optional
from datetime import date

# Config (replace if you're using env variables or a config file)
NEO4J_URI = "bolt://localhost:7687"
NEO4J_USER = "neo4j"
NEO4J_PASSWORD = "12345678"  # Change this to your actual password

driver = GraphDatabase.driver(NEO4J_URI, auth=(NEO4J_USER, NEO4J_PASSWORD))

class Project(BaseModel):
    id: str
    name: str
    owner: str
    isLocked: bool = False
    files: List[str] = []
    IPList: List[Tuple[str, int]] = []

class ProjectManager(BaseModel):
    name: str
    owner: str
    IPList: List[Tuple[str, int]]
    dateRange: Optional[Tuple[date, date]] = None
    locked: bool = False

def get_all_projects():
    with driver.session() as session:
        result = session.run("MATCH (p:Project) RETURN p")
        return [
            {
                "id": record["p"]["id"],
                "name": record["p"]["name"],
                "owner": record["p"]["owner"],
                "isLocked": record["p"].get("isLocked", False),
                "files": record["p"].get("files", []),
                "IPList": record["p"].get("IPList", [])
            }
            for record in result
        ]

def create_user_node(user_id: int, name: str):
    with driver.session() as session:
        session.run("MERGE (u:User {id: $id}) SET u.name = $name", id=user_id, name=name)

def verify_user(user_id: int, name: str):
    with driver.session() as session:
        result = session.run("MATCH (u:User {id: $id, name: $name}) RETURN u", id=user_id, name=name)
        return result.single() is not None

def create_project_node(project: Project):
    with driver.session() as session:
        session.run("""
            MERGE (p:Project {id: $id})
            SET p.name = $name,
                p.owner = $owner,
                p.isLocked = $isLocked,
                p.files = $files,
                p.IPList = $IPList
        """, id=project.id, name=project.name, owner=project.owner,
             isLocked=project.isLocked, files=project.files, IPList=str(project.IPList))

def create_project_manager_node(pm: ProjectManager):
    with driver.session() as session:
        session.run("""
            MERGE (pm:ProjectManager {name: $name})
            SET pm.owner = $owner,
                pm.IPList = $IPList,
                pm.dateRange = $dateRange,
                pm.locked = $locked
        """, name=pm.name,
             owner=pm.owner,
             IPList=str(pm.IPList),
             dateRange=str(pm.dateRange),
             locked=pm.locked)

def link_owner_to_project(user_id: int, project_id: str):
    with driver.session() as session:
        session.run("""
            MATCH (u:User {id: $user_id}), (p:Project {id: $project_id})
            MERGE (u)-[:OWNS]->(p)
        """, user_id=user_id, project_id=project_id)

def get_project_node(project_id: str):
    with driver.session() as session:
        result = session.run("MATCH (p:Project {id: $id}) RETURN p", id=project_id)
        record = result.single()
        if not record:
            raise Exception("Project not found")
        node = record["p"]
        return {
            "id": node["id"],
            "name": node["name"],
            "owner": node["owner"],
            "isLocked": node["isLocked"],
            "files": node.get("files", []),
            "IPList": node.get("IPList", [])
        }

def get_project_owner_node(project_id: str):
    with driver.session() as session:
        result = session.run("""
            MATCH (u:User)-[:OWNS]->(p:Project {id: $project_id})
            RETURN u
        """, project_id=project_id)
        record = result.single()
        if not record:
            raise Exception("Owner not found")
        node = record["u"]
        return {"id": node["id"], "name": node["name"]}

def update_project_owner(project_id: str, new_owner: str):
    with driver.session() as session:
        session.run("MATCH (p:Project {id: $id}) SET p.owner = $new_owner", id=project_id, new_owner=new_owner)

def update_project_id(old_id: str, new_id: str):
    with driver.session() as session:
        session.run("MATCH (p:Project {id: $old_id}) SET p.id = $new_id", old_id=old_id, new_id=new_id)

def update_project_lock(project_id: str, lock: bool):
    with driver.session() as session:
        session.run("MATCH (p:Project {id: $id}) SET p.isLocked = $locked", id=project_id, locked=lock)

def link_user_access_to_project(user_id: int, project_id: str):
    with driver.session() as session:
        session.run("""
            MERGE (u:User {id: $user_id})
            MERGE (p:Project {id: $project_id})
            MERGE (u)-[:ACCESSED]->(p)
        """, user_id=user_id, project_id=project_id)

def get_all_users():
    with driver.session() as session:
        result = session.run("MATCH (u:User) RETURN u")
        return [
            {
                "id": record["u"]["id"],
                "name": record["u"]["name"]
            }
            for record in result
        ]
