import json
from typing import Dict, Any, List, Optional
import boto3
from botocore.exceptions import ClientError


class IAMService:
    """Lightweight wrapper around boto3 IAM client for common operations."""

    def __init__(self, region_name: Optional[str] = None):
        # boto3 will pick up credentials from env, shared config, or role
        session = boto3.Session(region_name=region_name)
        self.client = session.client("iam")

    def create_user(self, username: str) -> Dict[str, Any]:
        resp = self.client.create_user(UserName=username)
        return resp["User"]

    def delete_user(self, username: str) -> Dict[str, Any]:
        # Note: IAM requires detaching policies, deleting access keys, removing from groups before delete
        # This wrapper will attempt to detach inline and managed policies and remove from groups.
        try:
            # detach managed policies
            attached = self.client.list_attached_user_policies(UserName=username)
            for p in attached.get("AttachedPolicies", []):
                self.client.detach_user_policy(UserName=username, PolicyArn=p["PolicyArn"])

            # delete inline policies
            inline = self.client.list_user_policies(UserName=username)
            for name in inline.get("PolicyNames", []):
                self.client.delete_user_policy(UserName=username, PolicyName=name)

            # remove from groups
            groups = self.client.list_groups_for_user(UserName=username)
            for g in groups.get("Groups", []):
                self.client.remove_user_from_group(UserName=username, GroupName=g["GroupName"])

            # delete access keys
            keys = self.client.list_access_keys(UserName=username)
            for k in keys.get("AccessKeyMetadata", []):
                self.client.delete_access_key(UserName=username, AccessKeyId=k["AccessKeyId"])

            # finally delete user
            resp = self.client.delete_user(UserName=username)
            return resp
        except ClientError as e:
            raise

    def list_users(self) -> List[Dict[str, Any]]:
        paginator = self.client.get_paginator("list_users")
        users = []
        for page in paginator.paginate():
            users.extend(page.get("Users", []))
        return users

    def create_policy(self, name: str, policy_document: Dict[str, Any], description: Optional[str] = None) -> Dict[str, Any]:
        doc = json.dumps(policy_document)
        resp = self.client.create_policy(PolicyName=name, PolicyDocument=doc, Description=description or "")
        return resp["Policy"]

    def delete_policy(self, policy_arn: str) -> Dict[str, Any]:
        resp = self.client.delete_policy(PolicyArn=policy_arn)
        return resp

    def attach_user_policy(self, username: str, policy_arn: str) -> Dict[str, Any]:
        resp = self.client.attach_user_policy(UserName=username, PolicyArn=policy_arn)
        return resp

    def detach_user_policy(self, username: str, policy_arn: str) -> Dict[str, Any]:
        resp = self.client.detach_user_policy(UserName=username, PolicyArn=policy_arn)
        return resp

    def create_group(self, name: str) -> Dict[str, Any]:
        resp = self.client.create_group(GroupName=name)
        return resp["Group"]

    def delete_group(self, name: str) -> Dict[str, Any]:
        # need to remove users from group first
        members = self.client.get_group(GroupName=name)
        for u in members.get("Users", []):
            self.client.remove_user_from_group(GroupName=name, UserName=u["UserName"])
        resp = self.client.delete_group(GroupName=name)
        return resp

    def add_user_to_group(self, username: str, group_name: str) -> Dict[str, Any]:
        resp = self.client.add_user_to_group(UserName=username, GroupName=group_name)
        return resp

    def remove_user_from_group(self, username: str, group_name: str) -> Dict[str, Any]:
        resp = self.client.remove_user_from_group(UserName=username, GroupName=group_name)
        return resp
