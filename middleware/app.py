import os
import requests
from flask import Flask, request, jsonify
from dotenv import load_dotenv
#something
load_dotenv()
app = Flask(__name__)

# Environment variables
GITHUB_TOKEN = os.getenv("GITHUB_TOKEN")
BACKEND_URL = os.getenv("BACKEND_URL", "http://localhost:5001/generate-messages")


def post_comment_to_github(repo_full_name, pr_number, comment_markdown):
    """Posts a markdown-formatted comment to the given Pull Request."""
    url = f"https://api.github.com/repos/{repo_full_name}/issues/{pr_number}/comments"
    headers = {
        "Authorization": f"token {GITHUB_TOKEN}",
        "Accept": "application/vnd.github+json"
    }
    response = requests.post(url, headers=headers, json={"body": comment_markdown})
    return response.status_code, response.text


@app.route("/webhook", methods=["POST"])
def handle_webhook():
    """Handles GitHub Pull Request events."""
    payload = request.json

    # Only process PR events
    if "pull_request" not in payload:
        return jsonify({"msg": "Not a pull_request event"}), 200

    pr = payload["pull_request"]
    repo_full_name = payload["repository"]["full_name"]
    pr_number = pr.get("number", 0)
    pr_title = pr.get("title", "")
    pr_body = pr.get("body", "")

    # Forward PR info to backend AI service
    try:
        ai_response = requests.post(BACKEND_URL, json={
            "title": pr_title,
            "description": pr_body
        }, timeout=5)
        ai_response.raise_for_status()
        suggestions_markdown = ai_response.json().get("suggestions_markdown", "")
        if not suggestions_markdown:
            suggestions_markdown = "_No AI suggestions, here are defaults:_\n- Review code style\n- Add tests\n- Update docs"
    except Exception:
        suggestions_markdown = (
            "_AI backend unavailable. Suggested actions:_\n"
            "- Implement logging\n"
            "- Refactor repetitive code\n"
            "- Ensure API error handling"
        )

    # Post the suggestions as a PR comment
    status, resp_text = post_comment_to_github(repo_full_name, pr_number, suggestions_markdown)

    return jsonify({
        "status": "posted",
        "github_status": status,
        "response": resp_text
    })


@app.route("/health", methods=["GET"])
def health_check():
    """Health check endpoint."""
    return "Middleware is running!", 200


if __name__ == "__main__":
    app.run(port=5000, debug=True)
