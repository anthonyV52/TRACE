from neo4j import GraphDatabase

class DBEnumerator:
    def __init__(self, driver):
        self.driver = driver
        self.tableNames = []
        self.columnNames = {}
        self.table = {}

    def enumerate_database(self):
        with self.driver.session() as session:
            # Get all labels (table names)
            result = session.run("CALL db.labels()")
            self.tableNames = [record["label"] for record in result]

            for label in self.tableNames:
                # Get column names
                props_result = session.run(f"""
                    MATCH (n:{label})
                    RETURN keys(n) AS props
                    LIMIT 1
                """)
                props = props_result.single()
                if props:
                    self.columnNames[label] = props["props"]

                # Get sample rows
                data_result = session.run(f"""
                    MATCH (n:{label})
                    RETURN properties(n) AS row
                    LIMIT 25
                """)
                self.table[label] = [record["row"] for record in data_result]

    def get_summary(self):
        return {
            "tableNames": self.tableNames,
            "columnNames": self.columnNames,
            "table": self.table
        }
