from fastapi import FastAPI
from pydantic import BaseModel
import os
import json
from openai import OpenAI
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

# CORS pour pouvoir appeler depuis le navigateur / Hoppscotch
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Client OpenAI : clé lue depuis les variables d'environnement (Railway)
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
    Retourne un vrai JSON propre (pas un bloc de texte).
    """

    prompt = f"""
    Tu es RIZZ-IA, une intelligence spécialisée en séduction, rizz,
    psychologie sociale et analyse des messages.

    Analyse ce message :
    ─────────────────────────────
    Message : "{data.message}"
    Contexte : "{data.context}"
    ─────────────────────────────

    Donne-moi AU FORMAT JSON STRICT :
    1. un "rizz_score" de 0 à 100
    2. un "interest" = "faible" / "moyen" / "élevé"
    3. un objet "replies" avec :
        - "smooth"
        - "humour"
        - "sigma"
    4. "advice" = conseil court

    Format attendu, sans explication, sans texte autour, sans ``` :
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
        max_tokens=300,
    )

    raw = ai.choices[0].message.content or ""
    content = raw.strip()

    # Si l'IA renvoie encore des ```json ... ```, on nettoie
    if content.startswith("```"):
        parts = content.split("```")
        if len(parts) >= 2:
            content = parts[1].strip()
            if content.startswith("json"):
                content = content[4:].lstrip("\n").strip()

    try:
        parsed = json.loads(content)
    except Exception:
        # Si jamais ça plante, on renvoie le brut pour debug
        parsed = {"raw": raw}

    return parsed
