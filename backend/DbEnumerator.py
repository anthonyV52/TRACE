import sqlite3
from typing import List, Optional, Tuple, Any
from fastapi import FastAPI

app = FastAPI()

class DBEnumerator:
    def __init__(self, db_path: str):
        """
        Initializes the DBEnumerator with a database path.
        Ensures the connection is closed initially.
        """
        self.db_path = db_path
        self.connection: Optional[sqlite3.Connection] = None
        self.cursor: Optional[sqlite3.Cursor] = None
        self.query: Optional[str] = None
        self.tables: List[str] = []

    def open_connection(self):
        """Opens a connection to the database."""
        if not self.connection:
            try:
                self.connection = sqlite3.connect(self.db_path)
                self.cursor = self.connection.cursor()
            except sqlite3.Error as e:
                print(f"Error opening database: {e}")

    def close_connection(self):
        """Closes the database connection."""
        if self.connection:
            try:
                self.connection.close()
            except sqlite3.Error as e:
                print(f"Error closing database: {e}")
            finally:
                self.connection = None
                self.cursor = None

    def execute_query(self, query: str, params: Tuple[Any, ...] = ()):
        """
        Executes a given SQL query (INSERT, UPDATE, DELETE).
        """
        if not self.connection:
            self.open_connection()
        try:
            self.cursor.execute(query, params)
            self.connection.commit()
        except sqlite3.Error as e:
            print(f"Error executing query: {e}")

    def fetch_results(self, query: str, params: Tuple[Any, ...] = ()) -> List[Tuple[Any]]:
        """
        Executes a SELECT query and fetches all results.
        """
        if not self.connection:
            self.open_connection()
        try:
            self.cursor.execute(query, params)
            return self.cursor.fetchall()
        except sqlite3.Error as e:
            print(f"Error fetching results: {e}")
            return []

    def is_connection_open(self) -> bool:
        """Checks if the database connection is open."""
        return self.connection is not None

    def initialize_enumeration(self, query: str):
        """Stores the SQL query for execution."""
        self.query = query

    def get_query_results(self) -> List[str]:
        """Returns the results of the last executed query."""
        if not hasattr(self, "results"):
            raise Exception("Query must be executed before fetching results.")
        return self.results

    def store_table(self, table_name: str):
        """Stores a reference to an existing table."""
        if not self.connection:
            raise Exception("Database connection must be open to store tables.")
        self.tables.append(table_name)

    def get_table_names(self) -> List[str]:
        """Retrieves the stored table names."""
        if not self.tables:
            raise Exception("No tables have been stored.")
        return self.tables

    def get_table_features(self, table_name: str) -> List[str]:
        """Retrieves column names of a given table."""
        if table_name not in self.tables:
            raise Exception("Table is not stored in the enumerator.")
        if not self.connection:
            raise Exception("Database connection must be open.")
        self.cursor.execute(f"PRAGMA table_info({table_name})")
        columns = [row[1] for row in self.cursor.fetchall()]
        return columns

# FastAPI Routes
db_enumerator = DBEnumerator("your_database.db")

@app.post("/open_connection")
def open_connection():
    db_enumerator.open_connection()

@app.post("/close_connection")
def close_connection():
    db_enumerator.close_connection()

@app.post("/initialize_enumeration")
def initialize_enumeration(query: str):
    db_enumerator.initialize_enumeration(query)

@app.post("/execute_query")
def execute_query(query: str):
    db_enumerator.execute_query(query)

@app.get("/get_query_results")
def get_query_results():
    return db_enumerator.fetch_results(db_enumerator.query)

@app.post("/store_table")
def store_table(table_name: str):
    db_enumerator.store_table(table_name)

@app.get("/get_table_names")
def get_table_names():
    return db_enumerator.get_table_names()

@app.get("/get_table_features")
def get_table_features(table_name: str):
    return {"features": db_enumerator.get_table_features(table_name)}
