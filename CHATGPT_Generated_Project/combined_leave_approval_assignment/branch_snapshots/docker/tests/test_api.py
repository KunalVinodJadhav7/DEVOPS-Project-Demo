import os
from pathlib import Path
TEST_DB=Path('test_leave.db')
if TEST_DB.exists(): TEST_DB.unlink()
os.environ['DATABASE_URL']=f'sqlite:///{TEST_DB.absolute()}'
os.environ['SECRET_KEY']='test-secret'
from fastapi.testclient import TestClient
from app.main import app
client=TestClient(app)

def token(username,password):
    return client.post('/api/auth/login',data={'username':username,'password':password}).json()['access_token']

def setup_module():
    for username,role in [('emp1','employee'),('hr1','hr')]:
        client.post('/api/auth/register',json={'username':username,'email':username+'@example.com','password':'Passw0rd!','role':role})

def teardown_module():
    if TEST_DB.exists(): TEST_DB.unlink()

def test_employee_submission_and_hr_review():
    emp=token('emp1','Passw0rd!')
    r=client.post('/api/leave/submit',data={'start_date':'2026-09-01','end_date':'2026-09-03','reason':'Family trip'},headers={'Authorization':f'Bearer {emp}'})
    assert r.status_code==200
    leave_id=r.json()['id']
    hr=token('hr1','Passw0rd!')
    r=client.patch(f'/api/leave/{leave_id}/hr-review',json={'approved':True,'comments':'Checked'},headers={'Authorization':f'Bearer {hr}'})
    assert r.status_code==200 and r.json()['status']=='PENDING_MANAGER'
