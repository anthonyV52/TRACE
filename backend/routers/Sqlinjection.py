# backend/routers/sqlinjection.py

from fastapi import APIRouter
from pydantic import BaseModel
from typing import List
from backend.services.SQLInjection import SQLInjection

router = APIRouter()
scanner = SQLInjection()


class ScanConfig(BaseModel):
    url: str
    port: str
    username: str
    password: str
    enumLevel: str
    timeout: str
    additional: str
    enumeration: bool

class PayloadList(BaseModel):
    payloads: List[str]



@router.post("/api/sql/start")
def start_sql_scan(config: ScanConfig):
    scanner.set_scan_config(config.dict())
    scanner.start_scan()
    return {"status": "Scan started"}

@router.post("/api/sql/pause")
def pause_sql_scan():
    scanner.pause_scan()
    return {"status": "Scan paused"}

@router.post("/api/sql/resume")
def resume_sql_scan():
    scanner.resume_scan()
    return {"status": "Scan resumed"}

@router.post("/api/sql/restart")
def restart_sql_scan():
    scanner.reset_service()
    scanner.start_scan()
    return {"status": "Scan restarted"}

@router.get("/api/sql-scan-status")
def get_sql_status():
    return scanner.get_scan_status()

@router.get("/api/sql/structure")
def get_structure():
    return scanner.get_database_structure()


@router.get("/api/sql/logs")
def get_terminal_logs():
    return {"logs": scanner.get_terminal_logs()}
