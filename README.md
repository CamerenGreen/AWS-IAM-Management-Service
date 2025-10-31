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

Authentication
--
This service supports a simple API-key based protection for the `/api/*` endpoints.

- To enable it set the `API_KEY` environment variable to a secret value.
- Requests must then include a header `X-API-Key: <your-key>`.
- If `API_KEY` is not set the auth dependency is a no-op (this makes local testing and the provided pytest tests unchanged).

Example (PowerShell):

```powershell
$env:API_KEY = "my-secret-key"
curl -H "X-API-Key: my-secret-key" http://127.0.0.1:8000/api/users
```

Notes
- For production consider using OAuth/OpenID Connect or an API gateway with proper auth and rate limiting. The API key approach here is intended for small internal tooling and demos.

Testing
Run the tests (they use moto to mock AWS):

```powershell
pytest -q
```
