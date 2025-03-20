import sqlite3
from typing import List, Optional

class DBEnumerator:
    def __init__(self, db_path: str):
        """
        Initializes the DBEnumerator with a database path.
        @ensures The connection is closed initially.
        """
        self.db_path = db_path
        self.connection: Optional[sqlite3.Connection] = None
        self.cursor: Optional[sqlite3.Cursor] = None
        self.query: Optional[str] = None
        self.tables: List[str] = []

    def open_connection(self):
        """Opens a connection to the database."""
        if not self.connection:
            self.connection = sqlite3.connect(self.db_path)
            self.cursor = self.connection.cursor()
        else:
            print("Connection is already open.")

    def close_connection(self):
        """Closes the database connection."""
        if self.connection:
            self.connection.close()
            self.connection = None
            self.cursor = None
        else:
            print("No open connection to close.")

    def is_connection_open(self) -> bool:
        """Checks if the database connection is open."""
        return self.connection is not None

    def initialize_enumeration(self, query: str):
        """Stores the SQL query for execution."""
        self.query = query

    def execute_query(self):
        """Executes the stored query and stores the results."""
        if not self.connection or not self.query:
            raise Exception("Database connection must be open and query must be initialized.")
        self.cursor.execute(self.query)
        self.results = self.cursor.fetchall()

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
