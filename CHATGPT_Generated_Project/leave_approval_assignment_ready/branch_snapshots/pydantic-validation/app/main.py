from fastapi import FastAPI, HTTPException
from .models import LeaveStatus
from .schemas import LeaveSubmitInput

app = FastAPI(title='Employee Leave Approval System', version='0.2.0')

@app.get('/health')
def health():
    return {'status':'ok', 'service':'Employee Leave Approval System'}

@app.post('/api/leave/validate')
def validate_leave(payload: LeaveSubmitInput):
    return {
        'valid': True,
        'initial_status': LeaveStatus.PENDING_HR.value,
        'start_date': payload.start_date,
        'end_date': payload.end_date,
        'reason': payload.reason,
    }
