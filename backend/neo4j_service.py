from neo4j_driver import get_driver

def create_project_node(project):
    with get_driver().session() as session:
        session.run(
            """
            CREATE (p:Project {id: $id, name: $name, owner_id: $owner_id, locked: $locked})
            """,
            id=project.id,
            name=project.name,
            owner_id=project.owner_id,
            locked=project.locked
        )

def create_user_node(user_id: int, name: str):
    with get_driver().session() as session:
        session.run(
            "MERGE (u:User {id: $id, name: $name})",
            id=user_id,
            name=name
        )

def link_owner_to_project(user_id: int, project_id: int):
    with get_driver().session() as session:
        session.run(
            """
            MATCH (u:User {id: $user_id}), (p:Project {id: $project_id})
            MERGE (u)-[:OWNS]->(p)
            """,
            user_id=user_id,
            project_id=project_id
        )
