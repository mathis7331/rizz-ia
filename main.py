from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()

class MessageInput(BaseModel):
    context: str | None = None
    message: str

@app.get("/")
def root():
    return {"status": "ok", "service": "Rizz IA - MVP sans IA"}

@app.post("/analyze")
def analyze_message(data: MessageInput):
    """
    Pour l'instant, pas d'IA :
    on renvoie juste une fausse analyse de test.
    Ensuite on branchera OpenAI ici.
    """
    message = data.message

    # Exemple de pseudo "analyse" sans IA:
    response = {
        "original_message": message,
        "context": data.context,
        "rizz_score": 69,  # valeur random pour test
        "interest_estimate": "Impossible à dire sans IA (MVP)",
        "suggested_replies": [
            "Pour l'instant c'est une réponse de test.",
            "On branchera Rizz IA ici bientôt 😉",
        ],
    }

    return response
