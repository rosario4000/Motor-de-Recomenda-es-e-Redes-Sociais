from neo4j import GraphDatabase

URI = "bolt://localhost:7687"
USERNAME = "neo4j"
PASSWORD = "valdemiro"

driver = GraphDatabase.driver(
    URI,
    auth=(USERNAME, PASSWORD)
)

def close_connection():
    driver.close()