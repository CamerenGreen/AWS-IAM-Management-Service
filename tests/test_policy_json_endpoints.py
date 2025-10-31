import io
import json
from fastapi.testclient import TestClient
from moto import mock_iam
from app.main import app
from app.services.iam_service import IAMService


client = TestClient(app)


def test_upload_and_create_policy_from_file(tmp_path):
    # Ensure policies dir exists (the endpoint uses ./policies)
    policies_dir = tmp_path / "policies"
    policies_dir.mkdir()

    # Use moto to mock IAM
    with mock_iam():
        # create a simple policy JSON
        policy_doc = {
            "Version": "2012-10-17",
            "Statement": [{
                "Effect": "Allow",
                "Action": "s3:ListBucket",
                "Resource": "*"
            }]
        }

        # Upload the policy file via API
        file_bytes = json.dumps(policy_doc).encode("utf-8")
        files = {"file": ("tmp_policy.json", io.BytesIO(file_bytes), "application/json")}

        # The endpoint writes to ./policies by default. Change cwd temporarily.
        import os
        old_cwd = os.getcwd()
        try:
            os.chdir(str(tmp_path))
            resp = client.post("/api/policies/upload", files=files)
            assert resp.status_code == 200
            data = resp.json()
            assert data["success"] is True
            filename = data["data"]["filename"]
            assert "tmp_policy.json" in filename

            # Now create policy from file
            payload = {"name": "TmpPolicy", "filename": "tmp_policy.json"}
            resp2 = client.post("/api/policies/from-file", json=payload)
            assert resp2.status_code == 200
            data2 = resp2.json()
            assert data2["success"] is True
            assert "policy" in data2["data"]
        finally:
            os.chdir(old_cwd)
