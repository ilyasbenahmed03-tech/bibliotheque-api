from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from app.database import get_db
from app.models import Utilisateur
from app.schemas import Token, UtilisateurCreate, UtilisateurOut
from app.security import creer_token, hacher_mot_de_passe, verifier_mot_de_passe

router = APIRouter(prefix="/auth", tags=["Authentification"])

@router.post("/inscription", response_model=UtilisateurOut, status_code=201)
def inscription(donnees: UtilisateurCreate, db: Session = Depends(get_db)):
    email = donnees.email.lower()

    deja_inscrit = db.query(Utilisateur).filter(Utilisateur.email == email).first()
    if deja_inscrit:
        raise HTTPException(status_code=409, detail="Cet email est déjà utilisé")

    utilisateur = Utilisateur(
     nom=donnees.nom,
     prenom=donnees.prenom,
     email=email,
    telephone=donnees.telephone,
     mot_de_passe=hacher_mot_de_passe(donnees.mot_de_passe),
     role="membre",  
    )
    db.add(utilisateur)
    db.commit()
    db.refresh(utilisateur)
    return utilisateur

@router.post("/connexion", response_model=Token)
def connexion(form: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    utilisateur = db.query(Utilisateur).filter(Utilisateur.email == form.username.lower()).first()
    if utilisateur is None or not verifier_mot_de_passe(form.password, utilisateur.mot_de_passe):
        raise HTTPException(status_code=401, detail="Email ou mot de passe incorrect")
    return {"access_token": creer_token(utilisateur), "token_type": "bearer"}