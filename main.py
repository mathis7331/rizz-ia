from fastapi import FastAPI
from pydantic import BaseModel
import os
from openai import OpenAI
from fastapi.middleware.cors import CORSMiddleware   # ⬅️ AJOUT

app = FastAPI()

# Autoriser toutes les origines (pratique pour dev et tests)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],      # plus tard tu pourras restreindre
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
# Lecture de la clé OpenAI depuis Railway (Variables)
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

class MessageInput(BaseModel):
    context: str | None = None
    message: str

@app.get("/")
def root():
    return {"status": "ok", "service": "Rizz IA - Full AI Enabled"}

@app.post("/analyze")
def analyze_message(data: MessageInput):
    """
    RIZZ IA — analyse un message et génère les meilleures réponses.
    """
    prompt = f"""
    Tu es RIZZ-IA, une intelligence spécialisée en séduction, rizz,
    psychologie sociale et analyse des messages.

    Analyse ce message :
    ─────────────────────────────
    Message : "{data.message}"
    Contexte : "{data.context}"
    ─────────────────────────────

    Donne-moi AU FORMAT JSON :
    1. un "rizz_score" de 0 à 100
    2. un "interest" = faible / moyen / élevé
    3. un objet "replies" avec :
        - smooth
        - humour
        - sigma
    4. "advice" = conseil court

    Format :
    {{
      "rizz_score": 0-100,
      "interest": "faible/moyen/élevé",
      "replies": {{
        "smooth": "…",
        "humour": "…",
        "sigma": "…"
      }},
      "advice": "…"
    }}
    """

    ai = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[{"role": "user", "content": prompt}],
        max_tokens=300
    )

    # Réponse brute de l’IA
    raw = ai.choices[0].message.content

    return {"analysis": raw}
