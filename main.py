from fastapi import FastAPI
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware
from openai import OpenAI
import os

# Initialize OpenAI client with your API key
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

app = FastAPI()

# Enable CORS so frontend can access this API
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# Pydantic model for input
class Prompt(BaseModel):
    prompt: str

# POST endpoint for deep research
@app.post("/api/research")
async def research(data: Prompt):
    try:
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {
                    "role": "system",
                    "content": "You are an expert researcher. Provide a deep, detailed, and well-referenced explanation of the user's question using accurate and updated information."
                },
                {
                    "role": "user",
                    "content": data.prompt
                }
            ],
            max_tokens=2000,
            temperature=0.7
        )
        result_text = response.choices[0].message.content
        return {"result": result_text}

    except Exception as e:
        return {"result": f"Error: {str(e)}"}
