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
        repo_name = params.get("repo")
        pr_number = params.get("pr_number")

        if not all([owner, repo_name, pr_number]):
            raise ValueError("Missing required parameters: owner, repo, pr_number")

        g = Github(os.environ["GITHUB_TOKEN"])
        repo = g.get_repo(f"{owner}/{repo_name}")
        pr = repo.get_pull(int(pr_number))

        # diff 내용 가져오기
        files = pr.get_files()
        diff_content = []
        for f in files:
            diff_content.append({
                "filename": f.filename,
                "status": f.status,
                "additions": f.additions,
                "deletions": f.deletions,
                "patch": f.patch or ""
            })

        response_body = {
            "title": pr.title,
            "body": pr.body or "",
            "state": pr.state,
            "author": pr.user.login,
            "created_at": pr.created_at.isoformat(),
            "changed_files": pr.changed_files,
            "additions": pr.additions,
            "deletions": pr.deletions,
            "diff_url": pr.diff_url,
            "diff": diff_content
        }

        return build_response(event, 200, response_body)

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
