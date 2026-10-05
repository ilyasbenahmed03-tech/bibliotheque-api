from fastapi import FastAPI
from app.routers import auth, emprunts, livres, utilisateurs

app = FastAPI(
    title="API Bibliothèque",
    description="Projet 5BDDD - gestion d'une bibliothèque en ligne (FastAPI + Oracle)",
    version="1.0",
)
app.include_router(auth.router)
app.include_router(utilisateurs.router)
app.include_router(livres.router)
app.include_router(emprunts.router)

@app.get("/", tags=["Accueil"])
def accueil():
    return {"message": "API Bibliothèque en ligne, la doc est sur /docs"}