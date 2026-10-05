import os
from datetime import datetime, timedelta, timezone
import jwt
from dotenv import load_dotenv
from fastapi import Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer
from pwdlib import PasswordHash
from sqlalchemy.orm import Session
from app.database import get_db
from app.models import Utilisateur

load_dotenv()
SECRET_KEY= os.getenv("JWT_SECRET")
ALGORITHM= "HS256"
DUREE_TOKEN_MINUTES= 60

# argon2 pour hacher les mots de passe
password_hash= PasswordHash.recommended()
# indique  FastAPI et Swager ou on peut recuperer  le token
oauth2_scheme= OAuth2PasswordBearer(tokenUrl="/auth/connexion")


def hacher_mot_de_passe(mot_de_passe: str) -> str:
 return password_hash.hash(mot_de_passe)

def verifier_mot_de_passe(mot_de_passe: str, hash_enregistre: str) -> bool:
 return password_hash.verify(mot_de_passe, hash_enregistre)

def creer_token(utilisateur: Utilisateur) -> str:
    expiration=datetime.now(timezone.utc) + timedelta(minutes=DUREE_TOKEN_MINUTES)
    donnees= {"sub": str(utilisateur.id), "role": utilisateur.role, "exp": expiration}
    return jwt.encode(donnees, SECRET_KEY, algorithm=ALGORITHM)


def get_utilisateur_connecte(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):
    erreur =HTTPException(
        status_code=401,
        detail="Token invalide ou expiré",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        donnees =jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        utilisateur_id =int(donnees["sub"])
    except (jwt.PyJWTError, KeyError, ValueError):
     raise erreur

    utilisateur = db.get(Utilisateur, utilisateur_id)
    if utilisateur is None:
     raise erreur
    return utilisateur

#admin
def admin_requis(utilisateur: Utilisateur = Depends(get_utilisateur_connecte)):
    if utilisateur.role != "admin":
        raise HTTPException(status_code=403, detail="Réservé aux administrateurs")
    return utilisateur