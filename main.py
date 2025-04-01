
from fastapi import FastAPI, Request
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware
import openai
import os

openai.api_key = os.getenv("OPENAI_API_KEY")

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

class Prompt(BaseModel):
    prompt: str

@app.post("/api/research")
async def research(data: Prompt):
    try:
        system_message = {
            "role": "system",
            "content": "You are an expert researcher. Provide a deep, detailed, and well-referenced explanation of the user's question using accurate and updated information."
        }
        user_message = {"role": "user", "content": data.prompt}

        response = openai.ChatCompletion.create(
            model="gpt-4-turbo",
            messages=[system_message, user_message],
            max_tokens=2000,
            temperature=0.7
        )
        result_text = response.choices[0].message.content
        return {"result": result_text}

    except Exception as e:
        return {"result": f"Error: {str(e)}"}
