from flask import Flask, request, jsonify
from ai_pipeline import generate_suggestions  # Fixed import

app = Flask(__name__)

@app.route("/generate-messages", methods=["POST"])
def generate_messages():
    data = request.json
    title = data.get("title", "")
    description = data.get("description", "")

    if not title and not description:
        return jsonify({"error": "Missing PR data"}), 400

    suggestions = generate_suggestions(title, description)
    return jsonify({"suggestions": suggestions})

if __name__ == "__main__":
    app.run(port=5001)
