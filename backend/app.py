from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import Response
from pydantic import BaseModel
from rag import ask_ai

app = FastAPI()

# ✅ CORS (explicit & safe)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

class Question(BaseModel):
    question: str

# ✅ Handle CORS preflight explicitly
@app.options("/ask")
def options_ask():
    return Response(status_code=200)

@app.post("/ask")
def ask(query: Question):
    answer, docs = ask_ai(query.question)
    return {
        "answer": answer,
        "sources": [d.metadata for d in docs]
    }

