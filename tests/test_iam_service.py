import json
import boto3
from moto import mock_iam
from app.services.iam_service import IAMService


def test_create_and_list_user_and_group_and_policy():
    with mock_iam():
        svc = IAMService(region_name="us-east-1")

        # create user
        user = svc.create_user("alice")
        assert user["UserName"] == "alice"

        users = svc.list_users()
        assert any(u["UserName"] == "alice" for u in users)

        # create group and add user
        group = svc.create_group("devs")
        assert group["GroupName"] == "devs"

        svc.add_user_to_group("alice", "devs")
        members = svc.client.get_group(GroupName="devs")
        assert any(u["UserName"] == "alice" for u in members.get("Users", []))

        # create policy
        policy_doc = {
            "Version": "2012-10-17",
            "Statement": [{
                "Effect": "Allow",
                "Action": "s3:ListBucket",
                "Resource": "*"
            }]
        }
        policy = svc.create_policy("ListS3", policy_doc, description="Allow listing S3")
        assert "PolicyName" in policy

        # attach to user
        svc.attach_user_policy("alice", policy["Arn"])
        attached = svc.client.list_attached_user_policies(UserName="alice")
        assert any(p["PolicyArn"] == policy["Arn"] for p in attached.get("AttachedPolicies", []))

        # detach and delete policy
        svc.detach_user_policy("alice", policy["Arn"])
        svc.delete_policy(policy["Arn"])

        # remove user from group and delete group
        svc.remove_user_from_group("alice", "devs")
        svc.delete_group("devs")

        # delete user
        svc.delete_user("alice")

        assert svc.list_users() == []
