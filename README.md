# 🤖 SmaartCommit

> ✨ _"Smarter Commits. Cleaner Code."_

**SmaartCommit** is an AI-powered GitHub middleware that listens to Pull Request events and generates clear, meaningful commit message suggestions using **LangChain** and **Groq LLMs**.

---

## 🚀 What It Does

Whenever a developer opens or updates a Pull Request, SmaartCommit:

1. Receives the webhook via a Flask backend  
2. Parses the PR title and description  
3. Sends it to Groq LLM using LangChain  
4. Posts a suggested commit message back as a comment on the PR

---

## 🛠️ Tech Stack

| Layer         | Technology                |
| ------------- | ------------------------- |
| Backend       | Python, Flask             |
| AI Engine     | LangChain + Groq LLM      |
| GitHub Events | Webhooks + REST API       |
| Deployment    | Ngrok / Render (Local dev)|

---

## 📁 Folder Structure

```

smaartcommit/
├── backend/
│   ├── app.py               # Flask server with webhook
│   ├── ai\_pipeline.py       # LangChain + Groq logic
│   ├── .env                 # API keys and secrets
│   └── requirements.txt     # All dependencies
├── .gitignore
└── README.md

````

---

## ⚙️ Getting Started

### 1️⃣ Clone the Repo

```bash
git clone https://github.com/Samyukta04/smaartcommit.git
cd smaartcommit/backend
````

### 2️⃣ Setup Python Virtual Environment

```bash
python -m venv venv
.\venv\Scripts\activate   # Windows
# or
source venv/bin/activate  # macOS/Linux
```

### 3️⃣ Install Requirements

```bash
pip install -r requirements.txt
```

### 4️⃣ Add `.env` File

Create a `.env` file inside the `backend/` folder:

```
GROQ_API_KEY=your_groq_key_here
GITHUB_TOKEN=your_github_token_here
```

---

## 🚦 Run the Server

```bash
python app.py
```

By default, the app runs on: [http://127.0.0.1:5001](http://127.0.0.1:5001)

---

## 🔁 GitHub Webhook Setup

1. Go to your GitHub repo → **Settings → Webhooks → Add Webhook**
2. **Payload URL**: Your Ngrok or Render link + `/webhook`
   *Example*: `https://<your-tunnel>.ngrok.io/webhook`
3. **Content Type**: `application/json`
4. **Events**: `Just the pull_request event`
5. Click **Add Webhook**

---

## 🧪 Sample Test

You can test using `curl`:

```bash
curl -X POST http://127.0.0.1:5001/generate-messages \
  -H "Content-Type: application/json" \
  -d '{"title": "Add login", "description": "Implements JWT-based authentication flow."}'
```

✅ Response:

```json
{
  "suggestion": "feat(auth): add JWT-based login and authentication flow"
}
```

---

## 👥 Team SmaartCommit

| Name       | Role                    |
| ---------- | ----------------------- |
| Samyukta   | Middleware + DevOps     |
| Teammate 1 | AI Pipeline (LangChain) |
| Teammate 2 | GitHub Integration      |
| Teammate 3 | API Testing             |
| Teammate 4 | Docs + Demo Video       |

---

## 🎯 Why SmaartCommit?

Because writing meaningful commit messages shouldn’t be hard.
Let the AI do the smart part, while you focus on writing code. 🧠✨

---

## 📜 License

Team 16
```
