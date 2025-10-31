# AWS IAM Management Service

This is a small FastAPI-based service that exposes common AWS IAM operations (create/delete users, groups, policies, attach/detach policies, list operations).

Features
- Create/Delete IAM users
- Create/Delete IAM policies
- Attach/Detach user policies
- Create/Delete IAM groups
- Add/Remove user from group
- List users and groups

Requirements
- Python 3.9+
- AWS credentials with IAM permissions (or use moto in tests)

Quick start
1. Copy `.env.example` to `.env` and set AWS credentials or rely on environment/role:

   - AWS_ACCESS_KEY_ID
   - AWS_SECRET_ACCESS_KEY
   - AWS_DEFAULT_REGION

2. Create and activate a virtual environment, install dependencies:

```powershell
python -m venv .venv; .\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
```

3. Run the app locally:

```powershell
$env:AWS_ACCESS_KEY_ID="..."; $env:AWS_SECRET_ACCESS_KEY="..."; $env:AWS_DEFAULT_REGION="us-east-1"
uvicorn app.main:app --reload --port 8000
```

4. API endpoints
- POST /users -> create a user
- DELETE /users/{username} -> delete a user
- GET /users -> list users
- POST /policies -> create policy
- DELETE /policies/{policy_arn} -> delete policy
- POST /users/{username}/attach-policy -> attach a policy to a user
- POST /users/{username}/detach-policy -> detach a policy from a user
- POST /groups -> create group
- DELETE /groups/{group_name} -> delete group
- POST /groups/{group_name}/add-user -> add user to group
- POST /groups/{group_name}/remove-user -> remove user from group

See `app/schemas.py` for payload shapes.

Testing
Run the tests (they use moto to mock AWS):

```powershell
pytest -q
```

Notes
- This is a minimal example. For production, add secure authentication, request throttling, proper error handling, and stricter validation.
