# Employee Leave Approval System

A Python/FastAPI 5-tier Employee Leave Approval System for the DevOps project. The application uses SQLAlchemy for persistence and can connect to SQLite, PostgreSQL, or MariaDB/MySQL through `DATABASE_URL`.

## Architecture

Browser frontend -> FastAPI REST API -> SQLAlchemy -> SQLite / PostgreSQL / MariaDB

Roles: Employee -> HR -> Manager -> Admin/Department Head -> Super Admin.

Workflow: PENDING_HR -> PENDING_MANAGER -> PENDING_ADMIN -> APPROVED / REJECTED.

## Windows local run

Use the existing project virtual environment, then run from this folder:

```bat
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

Open:

- http://localhost:8000/dashboard
- http://localhost:8000/docs

For the configured VS Code environment, the reference activation command is:

```bat
cd /d "C:\Users\kphvj\.vscode\Programs\DEVOPS-Project-CLONE&Setup\DevOps_Env\Scripts" && call activate.bat && cd /d "C:\Users\kphvj\.vscode\Programs\DEVOPS-Project-CLONE&Setup\CHATGPT_Generated_Project\leave_approval_assignment_ready"
```

## Environment

Copy `.env.example` to `.env` and set a strong `SECRET_KEY` of at least 32 bytes. The database can be selected with `DATABASE_URL`.

SQLite:

```text
DATABASE_URL=sqlite:///./leave_approval.db
```

PostgreSQL:

```text
DATABASE_URL=postgresql+psycopg://postgres:password@localhost:5432/leave_approval_db
```

MariaDB/MySQL:

```text
DATABASE_URL=mysql+pymysql://root:password@localhost:3306/leave_approval_db
```

## Test

```bat
pytest -v
python -m unittest discover selenium
```

## Docker

```bat
docker compose up --build
```

Then open http://localhost:8000/dashboard.

## Git strategy

`main` = production, `develop` = staging/integration. Feature branches represent validation, HR review, manager approval, admin/UI, Selenium, Jenkins, Docker, and Ansible work.

## Frontend

Open `http://localhost:8000/dashboard` after starting FastAPI. The frontend is a role-aware vanilla HTML/CSS/JavaScript application backed by the FastAPI API.

- Employee: submit and track leave.
- HR: review requests in `PENDING_HR`.
- Manager: review requests in `PENDING_MANAGER`.
- Admin: finalize requests in `PENDING_ADMIN`.
- Super Admin: dispatch notifications and inspect audit status.
