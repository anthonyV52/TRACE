from neo4j import GraphDatabase
from pydantic import BaseModel

# Config (replace if you're using env variables or a config file)
NEO4J_URI = "bolt://localhost:7687"
NEO4J_USER = "neo4j"
NEO4J_PASSWORD = "12345678"  # Change this to your actual password

driver = GraphDatabase.driver(NEO4J_URI, auth=(NEO4J_USER, NEO4J_PASSWORD))

class Project(BaseModel):
    id: int
    name: str
    owner_id: int
    locked: bool = False

def get_all_projects():
    with driver.session() as session:
        result = session.run("MATCH (p:Project) RETURN p")
        return [
            {
                "id": record["p"]["id"],
                "name": record["p"]["name"],
                "owner_id": record["p"]["owner_id"],
                "locked": record["p"].get("locked", False)
            }
            for record in result
        ]

def create_user_node(user_id: int, name: str):
    with driver.session() as session:
        session.run("MERGE (u:User {id: $id}) SET u.name = $name", id=user_id, name=name)

def create_project_node(project: Project):
    with driver.session() as session:
        session.run("""
            MERGE (p:Project {id: $id})
            SET p.name = $name, p.owner_id = $owner_id, p.locked = $locked
        """, id=project.id, name=project.name, owner_id=project.owner_id, locked=project.locked)

def link_owner_to_project(user_id: int, project_id: int):
    with driver.session() as session:
        session.run("""
            MATCH (u:User {id: $user_id}), (p:Project {id: $project_id})
            MERGE (u)-[:OWNS]->(p)
        """, user_id=user_id, project_id=project_id)

def get_project_node(project_id: int):
    with driver.session() as session:
        result = session.run("MATCH (p:Project {id: $id}) RETURN p", id=project_id)
        record = result.single()
        if not record:
            raise Exception("Project not found")
        node = record["p"]
        return {
            "id": node["id"],
            "name": node["name"],
            "owner_id": node["owner_id"],
            "locked": node["locked"]
        }

def get_project_owner_node(project_id: int):
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

def update_project_owner(project_id: int, new_owner_id: int):
    with driver.session() as session:
        session.run("MATCH (p:Project {id: $id}) SET p.owner_id = $new_owner_id", id=project_id, new_owner_id=new_owner_id)

def update_project_id(old_id: int, new_id: int):
    with driver.session() as session:
        session.run("MATCH (p:Project {id: $old_id}) SET p.id = $new_id", old_id=old_id, new_id=new_id)

def update_project_lock(project_id: int, lock: bool):
    with driver.session() as session:
        session.run("MATCH (p:Project {id: $id}) SET p.locked = $locked", id=project_id, locked=lock)

def  link_user_access_to_project(user_id: int, project_id: int):
    with driver.session() as session:
        session.run("""
            MERGE (u:User {id: $user_id})
            MERGE (p:Project {id: $project_id})
            MERGE (u)-[:ACCESSED]->(p)
        """, user_id=user_id, project_id=project_id)
