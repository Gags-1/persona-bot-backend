from fastapi import FastAPI
from pydantic import BaseModel
import os
from dotenv import load_dotenv
import google.generativeai as genai  # type: ignore
from fastapi.middleware.cors import CORSMiddleware

load_dotenv()
API_KEY = os.getenv("API_KEY")


System_prompt=os.getenv("System_prompt")

genai.configure(api_key=API_KEY)

model = genai.GenerativeModel(model_name='gemini-2.0-flash')

chat = model.start_chat(history=[
    {"role": "user", "parts": System_prompt}
])



app= FastAPI()

# CORS setup
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


class Input(BaseModel):
    message:str


@app.post('/chat-bot')
def chat_bot(req:Input):
    try:
        response = chat.send_message(req.message)
        return {"response": response.text}
    except Exception as e:
        return {"error": str(e)}

