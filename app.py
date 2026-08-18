from datetime import date
from enum import Enum
from typing import List, Optional
from fastapi import FastAPI, Depends, HTTPException, UploadFile, File, Form, status
from pydantic import BaseModel, Field

app = FastAPI(
    title="Employee Leave Approval System",
    description="5-Tier Enterprise Workflow MVP (Employee -> HR -> Manager -> Admin/Department Head -> Super Admin / Notification)",
    version="2.0.0"
)

# --- UPDATED 5-TIER ORGANIZATIONAL ROLES ---
class UserRole(str, Enum):
    EMPLOYEE = "employee"
    HR = "hr"
    MANAGER = "manager"
    ADMIN = "admin"                    # 4th Tier: Admin / Department Head
    SUPER_ADMIN = "super_admin"        # 5th Tier: System & Notification Oversight

# --- WORKFLOW STATE MACHINE ENUMS ---
class LeaveStatus(str, Enum):
    PENDING_HR = "PENDING_HR"
    PENDING_MANAGER = "PENDING_MANAGER"
    PENDING_ADMIN = "PENDING_ADMIN"
    APPROVED = "APPROVED"
    REJECTED = "REJECTED"

# In-Memory Database Simulation for MVP
LEAVE_DATABASE = []

class LeaveRequestResponse(BaseModel):
    id: int
    employee_id: int
    start_date: date
    end_date: date
    reason: str
    status: LeaveStatus
    document_name: Optional[str] = None
    hr_comments: Optional[str] = None
    manager_comments: Optional[str] = None
    admin_notes: Optional[str] = None

# --- TIER 1: EMPLOYEE SUBMISSION ENDPOINT ---
@app.post("/api/leave/submit", response_model=LeaveRequestResponse, status_code=status.HTTP_201_CREATED)
async def submit_leave(
    employee_id: int = Form(...),
    start_date: date = Form(...),
    end_date: date = Form(...),
    reason: str = Form(..., min_length=5, max_length=250),
    supporting_document: Optional[UploadFile] = File(None)
):
    if start_date > end_date:
        raise HTTPException(status_code=400, detail="Start date cannot be later than end date.")
    
    leave_id = len(LEAVE_DATABASE) + 1
    doc_name = supporting_document.filename if supporting_document else None

    new_request = {
        "id": leave_id,
        "employee_id": employee_id,
        "start_date": start_date,
        "end_date": end_date,
        "reason": reason,
        "status": LeaveStatus.PENDING_HR,
        "document_name": doc_name,
        "hr_comments": None,
        "manager_comments": None,
        "admin_notes": None
    }
    
    LEAVE_DATABASE.append(new_request)
    return new_request

# --- TIER 2: HR REVIEW ENDPOINT ---
@app.patch("/api/leave/{leave_id}/hr-review", response_model=LeaveRequestResponse)
async def hr_review(leave_id: int, approved: bool, comments: str = Form(...), user_role: UserRole = UserRole.HR):
    if user_role not in [UserRole.HR, UserRole.SUPER_ADMIN]:
        raise HTTPException(status_code=403, detail="Unauthorized: Role HR required.")
        
    req = next((item for item in LEAVE_DATABASE if item["id"] == leave_id), None)
    if not req:
        raise HTTPException(status_code=404, detail="Leave request not found.")
    if req["status"] != LeaveStatus.PENDING_HR:
        raise HTTPException(status_code=400, detail="Request is not pending HR review.")

    req["hr_comments"] = comments
    req["status"] = LeaveStatus.PENDING_MANAGER if approved else LeaveStatus.REJECTED
    return req

# --- TIER 3: MANAGER / REVIEWER APPROVAL ENDPOINT ---
@app.patch("/api/leave/{leave_id}/manager-approve", response_model=LeaveRequestResponse)
async def manager_approve(leave_id: int, approved: bool, comments: str = Form(...), user_role: UserRole = UserRole.MANAGER):
    if user_role not in [UserRole.MANAGER, UserRole.SUPER_ADMIN]:
        raise HTTPException(status_code=403, detail="Unauthorized: Role Manager required.")
        
    req = next((item for item in LEAVE_DATABASE if item["id"] == leave_id), None)
    if not req:
        raise HTTPException(status_code=404, detail="Leave request not found.")
    if req["status"] != LeaveStatus.PENDING_MANAGER:
        raise HTTPException(status_code=400, detail="Request is not pending Manager review.")

    req["manager_comments"] = comments
    req["status"] = LeaveStatus.PENDING_ADMIN if approved else LeaveStatus.REJECTED
    return req

# --- TIER 4: ADMIN / DEPARTMENT HEAD OVERSIGHT ENDPOINT ---
@app.patch("/api/leave/{leave_id}/admin-finalize", response_model=LeaveRequestResponse)
async def admin_finalize(leave_id: int, approved: bool, admin_notes: str = Form(...), user_role: UserRole = UserRole.ADMIN):
    if user_role not in [UserRole.ADMIN, UserRole.SUPER_ADMIN]:
        raise HTTPException(status_code=403, detail="Unauthorized: Role Admin/Department Head required.")
        
    req = next((item for item in LEAVE_DATABASE if item["id"] == leave_id), None)
    if not req:
        raise HTTPException(status_code=404, detail="Leave request not found.")
    if req["status"] != LeaveStatus.PENDING_ADMIN:
        raise HTTPException(status_code=400, detail="Request is not pending Admin oversight.")

    req["admin_notes"] = admin_notes
    req["status"] = LeaveStatus.APPROVED if approved else LeaveStatus.REJECTED
    return req

# --- TIER 5: SUPER ADMIN / NOTIFICATION DISPATCH ENDPOINT ---
@app.post("/api/leave/{leave_id}/notify-employee", response_model=dict)
async def super_admin_notify(leave_id: int, user_role: UserRole = UserRole.SUPER_ADMIN):
    if user_role != UserRole.SUPER_ADMIN:
        raise HTTPException(status_code=403, detail="Unauthorized: Super Admin access required for global notification dispatch.")
        
    req = next((item for item in LEAVE_DATABASE if item["id"] == leave_id), None)
    if not req:
        raise HTTPException(status_code=404, detail="Leave request not found.")
        
    print(f"[SUPER ADMIN NOTIFICATION SERVICE]: System-level dispatch triggered for Employee ID {req['employee_id']}. Final Status: {req['status']}")
    
    return {
        "message": "Notification dispatched successfully via Super Admin gateway",
        "leave_id": req["id"],
        "employee_id": req["employee_id"],
        "dispatched_status": req["status"]
    }

# --- TRACKING / AUDIT ENDPOINT ---
@app.get("/api/leave/requests", response_model=List[LeaveRequestResponse])
async def get_all_requests():
    return LEAVE_DATABASE