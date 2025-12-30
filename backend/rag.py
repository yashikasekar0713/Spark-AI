import os
import requests
from langchain_community.vectorstores import FAISS
from langchain_huggingface import HuggingFaceEmbeddings

# =====================
# Groq Config
# =====================
GROQ_API_KEY = os.getenv("GROQ_API_KEY")
CHAT_URL = "https://api.groq.com/openai/v1/chat/completions"

HEADERS = {
    "Authorization": f"Bearer {GROQ_API_KEY}",
    "Content-Type": "application/json"
}

# =====================
# Embeddings (LOCAL + FREE)
# =====================
embeddings = HuggingFaceEmbeddings(
    model_name="sentence-transformers/paraphrase-MiniLM-L3-v2"
)

# =====================
# Load FAISS DB
# =====================
_db = None

def get_db():
    global _db
    if _db is None:
        _db = FAISS.load_local(
            "faiss_db",
            embeddings,
            allow_dangerous_deserialization=True
        )
    return _db

# =====================
# Call Groq LLM
# =====================
def call_llm(prompt: str) -> str:
    payload = {
        "model": "llama-3.1-8b-instant",
        "messages": [
            {"role": "system", "content": "You are a startup funding assistant."},
            {"role": "user", "content": prompt}
        ],
        "temperature": 0.3,
        "max_tokens": 300
    }

    res = requests.post(
        CHAT_URL,
        headers=HEADERS,
        json=payload,
        timeout=30
    )
    res.raise_for_status()

    return res.json()["choices"][0]["message"]["content"]

# =====================
# RAG Entry Point
# =====================
def ask_ai(question: str):
    db = get_db()
    docs = db.similarity_search(question, k=3)

    context = "\n".join(d.page_content for d in docs)

    prompt = f"""
Answer ONLY using the context below.
If the answer is not present, say "Data not available".

Context:
{context}

Question:
{question}
"""

    answer = call_llm(prompt)
    return answer, docs

