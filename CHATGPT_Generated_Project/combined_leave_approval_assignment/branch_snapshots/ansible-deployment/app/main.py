import os
from datetime import date
from pathlib import Path
from fastapi import Depends, FastAPI, Form, HTTPException, UploadFile, File, status
from fastapi.responses import HTMLResponse
from sqlalchemy import select
from sqlalchemy.orm import Session
from .database import Base, engine, get_db
from .models import UserRole, LeaveStatus
from .orm_models import Role, User, LeaveRequest, AuditLog
from .schemas import UserCreate, LeaveSubmitInput, ReviewInput
from .security import hash_password, verify_password, create_token, require_roles

app=FastAPI(title='Employee Leave Approval System', version='1.0.0')
UPLOAD_DIR=Path(os.getenv('UPLOAD_DIR','uploads')); UPLOAD_DIR.mkdir(exist_ok=True)

@app.on_event('startup')
def startup():
    Base.metadata.create_all(engine)
    db=next(get_db())
    try:
        descriptions={UserRole.EMPLOYEE:'Employee',UserRole.HR:'HR reviewer',UserRole.MANAGER:'Manager reviewer',UserRole.ADMIN:'Admin reviewer',UserRole.SUPER_ADMIN:'Super Admin'}
        for role,desc in descriptions.items():
            if not db.scalar(select(Role).where(Role.role_name==role)):
                db.add(Role(role_name=role,description=desc))
        db.commit()
    finally: db.close()

def audit(db, leave, actor, action, comments):
    db.add(AuditLog(leave_request_id=leave.id, actor_id=actor.id, action_performed=action, comments=comments))

@app.get('/health')
def health(): return {'status':'ok','database':engine.url.get_backend_name()}

@app.post('/api/auth/register')
def register(payload:UserCreate,db:Session=Depends(get_db)):
    if db.scalar(select(User).where((User.username==payload.username)|(User.email==str(payload.email)))): raise HTTPException(409,'Username or email already exists')
    role=db.scalar(select(Role).where(Role.role_name==payload.role))
    user=User(username=payload.username,email=str(payload.email),password_hash=hash_password(payload.password),role=role); db.add(user); db.commit(); db.refresh(user)
    return {'id':user.id,'username':user.username,'email':user.email,'role':user.role.role_name.value}

@app.post('/api/auth/login')
def login(username:str=Form(...),password:str=Form(...),db:Session=Depends(get_db)):
    user=db.scalar(select(User).where(User.username==username))
    if not user or not verify_password(password,user.password_hash): raise HTTPException(401,'Invalid username or password')
    return {'access_token':create_token(user),'token_type':'bearer'}

@app.post('/api/leave/submit')
def submit_leave(start_date:date=Form(...),end_date:date=Form(...),reason:str=Form(...,min_length=5,max_length=250),supporting_document:UploadFile|None=File(None),current_user=Depends(require_roles(UserRole.EMPLOYEE)),db:Session=Depends(get_db)):
    data=LeaveSubmitInput(start_date=start_date,end_date=end_date,reason=reason)
    document_name=document_path=None
    if supporting_document:
        name=Path(supporting_document.filename or 'document.bin').name
        if Path(name).suffix.lower() not in {'.pdf','.png','.jpg','.jpeg','.doc','.docx'}: raise HTTPException(400,'Unsupported document type')
        target=UPLOAD_DIR/(os.urandom(8).hex()+Path(name).suffix.lower()); target.write_bytes(supporting_document.file.read()); document_name=name; document_path=str(target)
    leave=LeaveRequest(employee_id=current_user.id,start_date=data.start_date,end_date=data.end_date,reason=data.reason,status=LeaveStatus.PENDING_HR,document_name=document_name,document_path=document_path); db.add(leave); db.flush(); audit(db,leave,current_user,'LEAVE_SUBMITTED',reason); db.commit(); db.refresh(leave)
    return {'id':leave.id,'status':leave.status.value}

@app.get('/api/leave/requests')
def list_requests(current_user=Depends(require_roles(UserRole.EMPLOYEE,UserRole.HR,UserRole.MANAGER,UserRole.ADMIN,UserRole.SUPER_ADMIN)),db:Session=Depends(get_db)):
    rows=db.scalars(select(LeaveRequest).order_by(LeaveRequest.created_at.desc())).all(); return [{'id':x.id,'employee_id':x.employee_id,'status':x.status.value,'reason':x.reason} for x in rows]

@app.get('/dashboard',response_class=HTMLResponse)
def dashboard():
    return Path('templates/dashboard.html').read_text()

@app.patch('/api/leave/{leave_id}/manager-approve')
def manager_review(leave_id:int,payload:ReviewInput,current_user=Depends(require_roles(UserRole.MANAGER,UserRole.SUPER_ADMIN)),db:Session=Depends(get_db)):
    leave=db.get(LeaveRequest,leave_id)
    if not leave: raise HTTPException(404,'Leave request not found')
    if leave.status!=LeaveStatus.PENDING_MANAGER: raise HTTPException(400,'Request is not pending Manager review')
    leave.manager_comments=payload.comments; leave.status=LeaveStatus.PENDING_ADMIN if payload.approved else LeaveStatus.REJECTED; audit(db,leave,current_user,'MANAGER_APPROVED' if payload.approved else 'MANAGER_REJECTED',payload.comments); db.commit(); return {'id':leave.id,'status':leave.status.value}

@app.patch('/api/leave/{leave_id}/admin-finalize')
def admin_finalize(leave_id:int,payload:ReviewInput,current_user=Depends(require_roles(UserRole.ADMIN,UserRole.SUPER_ADMIN)),db:Session=Depends(get_db)):
    leave=db.get(LeaveRequest,leave_id)
    if not leave: raise HTTPException(404,'Leave request not found')
    if leave.status!=LeaveStatus.PENDING_ADMIN: raise HTTPException(400,'Request is not pending Admin oversight')
    leave.admin_notes=payload.comments; leave.status=LeaveStatus.APPROVED if payload.approved else LeaveStatus.REJECTED; audit(db,leave,current_user,'ADMIN_APPROVED' if payload.approved else 'ADMIN_REJECTED',payload.comments); db.commit(); return {'id':leave.id,'status':leave.status.value}

@app.post('/api/leave/{leave_id}/notify-employee')
def notify_employee(leave_id:int,current_user=Depends(require_roles(UserRole.SUPER_ADMIN)),db:Session=Depends(get_db)):
    leave=db.get(LeaveRequest,leave_id)
    if not leave: raise HTTPException(404,'Leave request not found')
    if leave.status not in {LeaveStatus.APPROVED,LeaveStatus.REJECTED}: raise HTTPException(400,'Final decision is required before notification')
    audit(db,leave,current_user,'EMPLOYEE_NOTIFICATION_DISPATCHED',leave.status.value); db.commit(); return {'message':'Notification dispatched','leave_id':leave.id,'status':leave.status.value}

@app.patch('/api/leave/{leave_id}/hr-review')
def hr_review(leave_id:int,payload:ReviewInput,current_user=Depends(require_roles(UserRole.HR,UserRole.SUPER_ADMIN)),db:Session=Depends(get_db)):
    leave=db.get(LeaveRequest,leave_id)
    if not leave: raise HTTPException(404,'Leave request not found')
    if leave.status!=LeaveStatus.PENDING_HR: raise HTTPException(400,'Request is not pending HR review')
    leave.hr_comments=payload.comments; leave.status=LeaveStatus.PENDING_MANAGER if payload.approved else LeaveStatus.REJECTED; audit(db,leave,current_user,'HR_APPROVED' if payload.approved else 'HR_REJECTED',payload.comments); db.commit(); return {'id':leave.id,'status':leave.status.value}
