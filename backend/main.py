from fastapi import FastAPI
from pydantic import BaseModel
from DbEnumerator import DBEnumerator

app = FastAPI()
db = DBEnumerator("database.db")

class QueryModel(BaseModel):
    query: str

class TableModel(BaseModel):
    table_name: str

@app.post("/open_connection")
def open_connection():
    db.open_connection()
    return {"message": "Connection opened"}

@app.post("/close_connection")
def close_connection():
    db.close_connection()
    return {"message": "Connection closed"}

@app.get("/is_connection_open")
def is_connection_open():
    return {"is_open": db.is_connection_open()}

@app.post("/initialize_enumeration")
def initialize_enumeration(query: QueryModel):
    db.initialize_enumeration(query.query)
    return {"message": "Query initialized"}

@app.post("/execute_query")
def execute_query():
    db.execute_query()
    return {"message": "Query executed"}

@app.get("/get_query_results")
def get_query_results():
    return {"results": db.get_query_results()}

@app.post("/store_table")
def store_table(table: TableModel):
    db.store_table(table.table_name)
    return {"message": f"Table {table.table_name} stored"}

@app.get("/get_table_names")
def get_table_names():
    return {"tables": db.get_table_names()}

@app.get("/get_table_features")
def get_table_features(table_name: str):
    return {"features": db.get_table_features(table_name)}
