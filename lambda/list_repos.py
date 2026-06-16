import json
import os
import logging
from github import Github, GithubException

logger = logging.getLogger()
logger.setLevel(logging.INFO)


def handler(event, context):
    logger.info(f"Event: {json.dumps(event)}")
    try:
        params = {p["name"]: p["value"] for p in event.get("parameters", [])}
        owner = params.get("owner")
        repo_type = params.get("type", "all")

        if not owner:
            raise ValueError("Missing required parameter: owner")

        g = Github(os.environ["GITHUB_TOKEN"])
        try:
            user = g.get_user(owner)
        except GithubException:
            user = g.get_organization(owner)

        repos = [{
            "name": r.name,
            "full_name": r.full_name,
            "description": r.description,
            "html_url": r.html_url,
            "private": r.private,
            "fork": r.fork,
            "language": r.language
        } for r in user.get_repos(type=repo_type)]

        return build_response(event, 200, repos)

    except GithubException as e:
        logger.error(f"GitHub API error: {e}")
        return build_response(event, 404, {"error": str(e)})
    except Exception as e:
        logger.error(f"Unexpected error: {e}")
        return build_response(event, 500, {"error": str(e)})


def build_response(event, status, body):
    return {
        "messageVersion": "1.0",
        "response": {
            "actionGroup": event.get("actionGroup"),
            "apiPath": event.get("apiPath"),
            "httpMethod": event.get("httpMethod"),
            "httpStatusCode": status,
            "responseBody": {"application/json": {"body": body}}
        }
    }
