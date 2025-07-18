from fastapi import FastAPI, Request
from langchain.llms import OpenAI
from langchain.prompts import PromptTemplate

app = FastAPI()

@app.post("/commit-message")
async def generate_commit_message(request: Request):
    payload = await request.json()
    diff = payload.get("diff", "")

    prompt = PromptTemplate.from_template(
        "Write a concise commit message for the following git diff:\n{diff}"
    )
    
    llm = OpenAI(model="gpt-3.5-turbo")
    message = llm(prompt.format(diff=diff))

    return {"commit_message": message}
