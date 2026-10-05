from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database import get_db
from app.models import Emprunt, Utilisateur
from app.schemas import EmpruntOut, UtilisateurOut
from app.security import admin_requis, get_utilisateur_connecte

router = APIRouter(prefix="/utilisateurs", tags=["Utilisateurs"])
@router.get("/moi", response_model=UtilisateurOut)
def mon_profil(moi: Utilisateur = Depends(get_utilisateur_connecte)):
    return moi

#les livres que jai en ce moment (pas encore rendus)
@router.get("/moi/emprunts", response_model=list[EmpruntOut])
def mes_emprunts_en_cours(moi: Utilisateur = Depends(get_utilisateur_connecte), db: Session = Depends(get_db)):
    return (
        db.query(Emprunt)
        .filter(Emprunt.utilisateur_id == moi.id, Emprunt.date_retour.is_(None))
        .order_by(Emprunt.date_emprunt.desc())
        .all()
    )

#tous mes emprunts, rendus ou pas
@router.get("/moi/historique", response_model=list[EmpruntOut])
def mon_historique(moi: Utilisateur = Depends(get_utilisateur_connecte), db: Session = Depends(get_db)):
    return (
        db.query(Emprunt)
        .filter(Emprunt.utilisateur_id == moi.id)
        .order_by(Emprunt.date_emprunt.desc())
        .all()
    )

#Pour admin
@router.get("", response_model=list[UtilisateurOut], dependencies=[Depends(admin_requis)])
def lister_utilisateurs(db: Session = Depends(get_db)):
    return db.query(Utilisateur).order_by(Utilisateur.id).all()

@router.get("/{utilisateur_id}/historique", response_model=list[EmpruntOut], dependencies=[Depends(admin_requis)])
def historique_utilisateur(utilisateur_id: int, db: Session = Depends(get_db)):
    if db.get(Utilisateur, utilisateur_id) is None:
        raise HTTPException(status_code=404, detail="Utilisateur introuvable")
    return (
        db.query(Emprunt)
        .filter(Emprunt.utilisateur_id == utilisateur_id)
        .order_by(Emprunt.date_emprunt.desc())
        .all()
    )