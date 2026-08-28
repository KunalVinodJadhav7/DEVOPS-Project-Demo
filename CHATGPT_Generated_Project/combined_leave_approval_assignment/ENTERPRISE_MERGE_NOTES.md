# Enterprise Dashboard Merge Notes

This repository preserves the original assignment's branch history and `branch_snapshots/` directory as historical evidence.

## Merge sequence
1. Existing feature branches remain unchanged.
2. Added branch `feature/enterprise-dashboard` from `develop`.
3. Applied the enterprise dashboard/application changes on that branch.
4. Merged `feature/enterprise-dashboard` into `develop`.
5. Merged `develop` into `main`.
6. Tagged the resulting production state as `v1.2.0-enterprise`.

## Enterprise changes merged
- Added the role-aware `frontend/` application.
- Added frontend static asset serving.
- Added `/employee`, `/hr`, `/manager`, `/admin`, and `/super-admin` routes.
- Added `/api/auth/me`.
- Expanded leave-request response fields and employee scoping.
- Added leave audit and supporting-document endpoints.
- Enforced a 32-byte minimum `SECRET_KEY` and `.env` loading.
- Added `python-dotenv` dependency.
- Updated Docker image to include the frontend.
