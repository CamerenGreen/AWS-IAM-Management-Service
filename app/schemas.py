from pydantic import BaseModel, Field
from typing import Optional, Dict, Any, List


class UserCreate(BaseModel):
    username: str = Field(..., min_length=1)


class ActionResponse(BaseModel):
    success: bool
    message: Optional[str]
    data: Optional[Dict[str, Any]]


class PolicyCreate(BaseModel):
    name: str = Field(..., min_length=1)
    description: Optional[str]
    policy_document: Dict[str, Any]


class PolicyFromFile(BaseModel):
    name: str = Field(..., min_length=1)
    filename: str = Field(..., min_length=1)


class AttachPolicyRequest(BaseModel):
    policy_arn: str


class GroupCreate(BaseModel):
    name: str = Field(..., min_length=1)


class AddUserToGroupRequest(BaseModel):
    username: str


class ListUsersResponse(BaseModel):
    users: List[Dict[str, Any]]
