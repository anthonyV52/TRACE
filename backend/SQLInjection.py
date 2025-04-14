from typing import List, Dict, Optional, Any
import os
import re

class SQLInjection:
    def __init__(self):
        self.predefined_queries = ["SELECT * FROM users", "DROP TABLE students"]
        self.stored_requests = {}
        self.stored_responses = {}
        self.terminal_logs = []
        self.request_counter = 1
        self.scan_running = False
        self.scan_paused = False
        self.scan_progress = 0
        self.scan_config = {
            "url": "",
            "port": "",
            "username": "",
            "password": "",
            "enumLevel": "",
            "timeout": "",
            "additional": "",
            "enumeration": False
        }
    
    def get_predefined_queries(self) -> List[str]:
        """
        Returns the list of predefined queries.

        Returns:
            List[str]: The list of predefined queries.
        """
        return self.predefined_queries
    
    def store_request(self, request: str) -> bool:
        if request:
            self.stored_requests[self.request_counter] = request
            self.request_counter += 1
            return True
        return False
    
    def set_scan_config(self, config: Dict[str, Any]):
        for key in self.scan_config:
            if key in config:
                self.scan_config[key] = config[key]
    
    def start_scan(self):
        self.scan_running = True
        self.scan_paused = False
        self.scan_progress = 0
        self.terminal_logs = []
        self._simulate_scan()
       
    def run_scan_with_payloads(self, payloads: List[str]):
        self.scan_running = True
        self.terminal_logs = []
        self.scan_progress = 0

        for idx, payload in enumerate(payloads):
            if not self.scan_running:
                break
            while self.scan_paused:
                time.sleep(1)

            self.store_request(payload)
            result = SQLInjectionScan.scan_input_sql_injection(payload)
            response = "Possible SQLi" if result else "Safe"
            self.store_response(self.request_counter - 1, response)
            self.terminal_logs.append(f"Scanned payload {payload} → {response}")

            self.scan_progress = int((idx + 1) / len(payloads) * 100)
            time.sleep(1)  # simulate response delay

        self.scan_running = False
        
        
    def pause_scan(self):
        if self.scan_running:
            self.scan_paused = True

    def resume_scan(self):
        if self.scan_running and self.scan_paused:
            self.scan_paused = False
    
    def get_request_by_id(self, request_id: int) -> Optional[str]:
        return self.stored_requests.get(request_id)
    
    def modify_request(self, request_id: int, new_request: str) -> bool:
        if request_id in self.stored_requests:
            self.stored_requests[request_id] = new_request
            return True
        return False
    
    def store_response(self, request_id: int, response: str) -> bool:
        if request_id in self.stored_requests:
            self.stored_responses[request_id] = response
            return True
        return False    
    
    def get_response_by_id(self, request_id: int) -> Optional[str]:
        return self.stored_responses.get(request_id)
    
    def get_all_requests(self) -> Dict[int, str]:
        return self.stored_requests
    
    def get_all_responses(self) -> Dict[int, str]:
        return self.stored_responses
    
    def get_scan_status(self):
        return {
            "progress": self.scan_progress,
            "paused": self.scan_paused,
            "metrics": {
                "testingType": "SQL Scan",
                "processedRequests": self.request_counter - 1,
                "effectivePayloads": len(self.stored_requests),
                "responseTime": f"{0.5 * (self.request_counter - 1):.2f}s"
            },
            "results": [
                {
                    "id": rid,
                    "parameter": "param",
                    "method": "POST",
                    "type": "1 W",
                    "payload": req,
                    "status": 200,
                    "length": 0.512,
                    "vulnerable": SQLInjectionScan.scan_input_sql_injection(req)
                }
                for rid, req in self.stored_requests.items()
            ]
        }
    
    def save_results_to_file(self, filename: str = "sql_results.txt") -> None:
        with open(filename, "w") as file:
            for request_id in self.stored_requests:
                request = self.stored_requests[request_id]
                response = self.stored_responses.get(request_id, "No Response")
                file.write(f"Request {request_id}: {request}\nResponse: {response}\n\n")
        print(f"Results saved to {filename}")
                
                
    def reset_service(self) -> None:
        self.stored_requests = {}
        self.stored_responses = {}
        self.request_counter = 1
        
    def get_available_features(self) -> List[str]:
        return ["SQL Injection Scan",
                "Modify SQL Request",
                "Show Stored SQL Requests",
                "Show Stored SQL Responses",
                "Save Results to File",
                "Reset Service"]
        
        
    def get_terminal_logs(self) -> List[str]:
        return self.terminal_logs

    
    
    
    def get_database_structure(self) -> Dict[str, List[Dict[str, str]]]:
        return {
            "login_info": [
                {"column": "user_id", "type": "int", "nullable": "No", "key": "PRI"},
                {"column": "username", "type": "varchar(255)", "nullable": "No", "key": "-"},
                {"column": "password", "type": "varchar(255)", "nullable": "No", "key": "-"},
                {"column": "full_name", "type": "varchar(255)", "nullable": "No", "key": "-"},
        ],
            "products": [
                {"column": "product_id", "type": "int", "nullable": "No", "key": "PRI"},
                {"column": "name", "type": "varchar(255)", "nullable": "No", "key": "-"},
                {"column": "price", "type": "float", "nullable": "No", "key": "-"},
         ]
    }
