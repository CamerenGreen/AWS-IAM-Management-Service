from fastapi import APIRouter, Depends, HTTPException, status, UploadFile, File
from typing import Any, Dict
from .schemas import (
    UserCreate,
    ActionResponse,
    PolicyCreate,
    AttachPolicyRequest,
    GroupCreate,
    AddUserToGroupRequest,
    PolicyFromFile,
)
from .services.iam_service import IAMService
import os
import json
from pathlib import Path

router = APIRouter()


def get_iam_service() -> IAMService:
    region = os.getenv("AWS_DEFAULT_REGION")
    return IAMService(region_name=region)


@router.post("/users", response_model=ActionResponse)
def create_user(payload: UserCreate, svc: IAMService = Depends(get_iam_service)):
    try:
        user = svc.create_user(payload.username)
        return ActionResponse(success=True, message="User created", data={"user": user})
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.delete("/users/{username}", response_model=ActionResponse)
def delete_user(username: str, svc: IAMService = Depends(get_iam_service)):
    try:
        svc.delete_user(username)
        return ActionResponse(success=True, message="User deleted")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/users", response_model=ActionResponse)
def list_users(svc: IAMService = Depends(get_iam_service)):
    try:
        users = svc.list_users()
        return ActionResponse(success=True, message="OK", data={"users": users})
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/policies", response_model=ActionResponse)
def create_policy(payload: PolicyCreate, svc: IAMService = Depends(get_iam_service)):
    try:
        p = svc.create_policy(payload.name, payload.policy_document, payload.description)
        return ActionResponse(success=True, message="Policy created", data={"policy": p})
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/policies/upload", response_model=ActionResponse)
def upload_policy_json(file: UploadFile = File(...)):
    """Upload a JSON policy file and save it under `policies/` for later use.

    Returns filename saved on disk.
    """
    try:
        content = file.file.read()
        # validate JSON
        policy = json.loads(content)

        policies_dir = Path("./policies")
        policies_dir.mkdir(parents=True, exist_ok=True)

        dest = policies_dir / file.filename
        # write bytes back
        with open(dest, "wb") as fh:
            fh.write(content)

        return ActionResponse(success=True, message="Policy JSON uploaded", data={"filename": str(dest)})
    except json.JSONDecodeError as e:
        raise HTTPException(status_code=400, detail=f"Invalid JSON: {e}")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/policies/from-file", response_model=ActionResponse)
def create_policy_from_file(payload: PolicyFromFile, svc: IAMService = Depends(get_iam_service)):
    """Create a managed IAM policy using a saved JSON file from `policies/` directory.
    Body: { "name": "PolicyName", "filename": "sample.json" }
    """
    try:
        policies_dir = Path("./policies")
        file_path = policies_dir / payload.filename
        if not file_path.exists():
            raise HTTPException(status_code=404, detail="Policy file not found")

        with open(file_path, "r", encoding="utf-8") as fh:
            policy_doc = json.load(fh)

        p = svc.create_policy(payload.name, policy_doc)
        return ActionResponse(success=True, message="Policy created from file", data={"policy": p})
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.delete("/policies/{policy_arn}", response_model=ActionResponse)
def delete_policy(policy_arn: str, svc: IAMService = Depends(get_iam_service)):
    try:
        svc.delete_policy(policy_arn)
        return ActionResponse(success=True, message="Policy deleted")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/users/{username}/attach-policy", response_model=ActionResponse)
def attach_policy(username: str, payload: AttachPolicyRequest, svc: IAMService = Depends(get_iam_service)):
    try:
        svc.attach_user_policy(username, payload.policy_arn)
        return ActionResponse(success=True, message="Policy attached")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/users/{username}/detach-policy", response_model=ActionResponse)
def detach_policy(username: str, payload: AttachPolicyRequest, svc: IAMService = Depends(get_iam_service)):
    try:
        svc.detach_user_policy(username, payload.policy_arn)
        return ActionResponse(success=True, message="Policy detached")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/groups", response_model=ActionResponse)
def create_group(payload: GroupCreate, svc: IAMService = Depends(get_iam_service)):
    try:
        g = svc.create_group(payload.name)
        return ActionResponse(success=True, message="Group created", data={"group": g})
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.delete("/groups/{group_name}", response_model=ActionResponse)
def delete_group(group_name: str, svc: IAMService = Depends(get_iam_service)):
    try:
        svc.delete_group(group_name)
        return ActionResponse(success=True, message="Group deleted")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/groups/{group_name}/add-user", response_model=ActionResponse)
def add_user_to_group(group_name: str, payload: AddUserToGroupRequest, svc: IAMService = Depends(get_iam_service)):
    try:
        svc.add_user_to_group(payload.username, group_name)
        return ActionResponse(success=True, message="User added to group")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/groups/{group_name}/remove-user", response_model=ActionResponse)
def remove_user_from_group(group_name: str, payload: AddUserToGroupRequest, svc: IAMService = Depends(get_iam_service)):
    try:
        svc.remove_user_from_group(payload.username, group_name)
        return ActionResponse(success=True, message="User removed from group")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
