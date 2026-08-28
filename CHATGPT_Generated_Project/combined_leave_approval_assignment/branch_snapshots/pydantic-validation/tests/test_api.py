from fastapi.testclient import TestClient
from app.main import app
client = TestClient(app)

def test_health():
    assert client.get('/health').json()['status'] == 'ok'

def test_validation_accepts_valid_request():
    r = client.post('/api/leave/validate', json={'start_date':'2026-09-01','end_date':'2026-09-03','reason':'Family trip'})
    assert r.status_code == 200
    assert r.json()['initial_status'] == 'PENDING_HR'

def test_validation_rejects_bad_dates():
    r = client.post('/api/leave/validate', json={'start_date':'2026-09-03','end_date':'2026-09-01','reason':'Family trip'})
    assert r.status_code == 422

def test_validation_rejects_short_reason():
    r = client.post('/api/leave/validate', json={'start_date':'2026-09-01','end_date':'2026-09-02','reason':'No'})
    assert r.status_code == 422
