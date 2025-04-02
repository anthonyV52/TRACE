from neo4j import GraphDatabase

# Replace with your actual credentials and connection string
uri = "bolt://localhost:7687"  # or neo4j+s://<your-aura-url>
user = "neo4j"
password = "neo4j123"

driver = GraphDatabase.driver(uri, auth=(user, password))

def get_driver():
    return driver
