from fastapi import APIRouter, Depends, HTTPException, status
from typing import Any, Dict
from .schemas import (
    UserCreate,
    ActionResponse,
    PolicyCreate,
    AttachPolicyRequest,
    GroupCreate,
    AddUserToGroupRequest,
)
from .services.iam_service import IAMService
import os

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
