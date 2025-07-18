import os
import re
from dotenv import load_dotenv
from langchain_groq import ChatGroq
from langchain.prompts import PromptTemplate

load_dotenv()

# Initialize Groq model
llm = ChatGroq(
    api_key=os.getenv("GROQ_API_KEY"),
    model="deepseek-r1-distill-llama-70b",
    temperature=0.3
)

# Strict prompt: only output 3 commit messages
prompt_template = """
You are an assistant that writes **3 clean, conventional commit messages** based ONLY on the PR details.

Rules:
- Use one of these types: feat, fix, chore, docs, refactor, test.
- Each message must be under 60 characters.
- Do NOT include any explanations or thinking.
- Output only the messages, numbered 1 to 3.

Pull Request Title: {title}
Pull Request Description: {description}

Now output ONLY the 3 commit messages:
1.
2.
3.
"""

prompt = PromptTemplate(template=prompt_template, input_variables=["title", "description"])
chain = prompt | llm


def generate_suggestions(title: str, description: str):
    """Generate 3 clean commit message suggestions using Groq."""
    result = chain.invoke({"title": title, "description": description})
    text_output = result.content if hasattr(result, "content") else str(result)

    # Remove any reasoning tags like <think> if the model outputs them
    text_output = re.sub(r"<think>.*?</think>", "", text_output, flags=re.DOTALL)

    # Split into lines and extract messages
    suggestions = []
    for line in text_output.split("\n"):
        line = line.strip()
        if re.match(r"^\d+\.", line):  # Matches lines like '1. message'
            suggestions.append(line.split(".", 1)[1].strip())

    return suggestions[:3]  # Ensure only top 3
