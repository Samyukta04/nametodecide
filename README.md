
# SmartCommit – AI Suggestions on Pull Requests

SmartCommit is a system that listens to GitHub Pull Request (PR) events, sends the PR details (title & description) to an AI backend, and posts AI-generated review suggestions as a comment on the PR automatically.

This solution was built for a Hackathon.

---

## How It Works
1. A **GitHub Webhook** triggers when a PR is opened.
2. The webhook hits the **Flask Middleware** (this repo).
3. Middleware forwards the PR details (title, description) to the **AI Backend**.
4. Suggestions (or defaults) are posted as a comment back to the PR using the GitHub API.

---

## Project Structure
```

nametodecide/
├── backend/             # AI suggestion service (runs separately)
├── middleware/          # Flask app handling GitHub webhooks
│   ├── app.py           # Main server
│   ├── requirements.txt # Python dependencies
│   ├── .env             # Environment variables
│   └── venv/            # (local environment, ignored)

````

---

## Prerequisites
- Python 3.10+
- `pip` and `virtualenv`
- GitHub Personal Access Token (with `repo` scope)
- Ngrok (or any tunnel) for testing locally

---

## Setup Instructions

### 1. Clone the Repository
```bash
git clone https://github.com/Samyukta04/nametodecide.git
cd nametodecide/middleware
````

### 2. Setup Python Environment

```bash
python -m venv venv
# On Windows:
venv\Scripts\activate
# On macOS/Linux:
source venv/bin/activate

pip install -r requirements.txt
```

### 3. Add Environment Variables

Create a `.env` file inside `middleware/`:

```
GITHUB_TOKEN=<your_personal_access_token>
BACKEND_URL=http://localhost:5001/generate-messages
```

The `GITHUB_TOKEN` must be a Personal Access Token with permissions to comment on PRs in your target repository.

---

## Running the Services

### Start the Backend (AI Suggestion Service)

From the `backend/` directory:

```bash
python app.py
```

Runs on `http://localhost:5001` by default.

### Start the Middleware

From the `middleware/` directory:

```bash
python app.py
```

Runs on `http://localhost:5000` by default.

### Expose Middleware using Ngrok

```bash
ngrok http 5000
```

Copy the forwarding URL (e.g., `https://xxxxx.ngrok-free.app`) — this will be the webhook endpoint.

---

## Setting Up GitHub Webhook

1. Go to your repository → **Settings** → **Webhooks**.
2. Add a new webhook:

   * **Payload URL**: `https://<ngrok-url>/webhook`
   * **Content type**: `application/json`
   * **Select event**: `Pull requests`
3. Save.

---

## Testing Locally

Manually trigger the webhook using `curl`:

```bash
curl -X POST https://<ngrok-url>/webhook \
-H "Content-Type: application/json" \
-d '{
  "action": "opened",
  "repository": { "full_name": "Samyukta04/nametodecide" },
  "pull_request": {
    "number": 1,
    "title": "Add login API",
    "body": "Implemented JWT authentication and fixed session timeout bug."
  }
}'
```

You should see:

* A response with `"status": "posted"`
* A comment automatically added to your PR.

---

## Example Output on GitHub PR

```
_No AI suggestions, here are defaults:_
- Review code style
- Add tests
- Update docs
```

---

## Deploying / Final Notes

* Make sure **`backend` and `middleware` are both running**.
* `ngrok` must be active whenever you want GitHub to reach your local server.
* To deploy permanently, you can host `middleware` and `backend` on any cloud (Heroku, Render, AWS, etc.).

---

## Branch Info

* **Main branch** contains the final integrated solution (backend + middleware).
* Push your work here:

```bash
git add .
git commit -m "Final SmartCommit Hackathon Submission"
git push origin main
```

---



