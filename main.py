from fastapi import FastAPI
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware
from openai import OpenAI
import os

# Initialize OpenAI client with API key from environment
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

app = FastAPI()

# Allow frontend to access backend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# Define request format
class Prompt(BaseModel):
    prompt: str

# Deep research endpoint
@app.post("/api/research")
async def research(data: Prompt):
    try:
        response = client.chat.completions.create(
            model="gpt-4-1106-preview",  # ✅ Updated model name
            messages=[
                {
                    "role": "system",
                    "content": "You are an expert researcher. Provide a deep, well-referenced and comprehensive explanation of the user's question."
                },
                {
                    "role": "user",
                    "content": data.prompt
                }
            ],
            max_tokens=2000,
            temperature=0.7
        )
        return {"result": response.choices[0].message.content}

    except Exception as e:
        return {"result": f"Error: {str(e)}"}
