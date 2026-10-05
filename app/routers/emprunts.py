from datetime import datetime, timedelta    
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database import get_db
from app.models import Emprunt, Livre, Utilisateur
from app.schemas import EmpruntCreate, EmpruntOut
from app.security import admin_requis, get_utilisateur_connecte

router = APIRouter(prefix="/emprunts", tags=["Emprunts"])
@router.post("", response_model=EmpruntOut, status_code=201)
def emprunter_livre(
    donnees: EmpruntCreate,
    moi: Utilisateur = Depends(get_utilisateur_connecte),
    db: Session = Depends(get_db),
):
 #on bloque la ligne du livre le temps de la transaction pour que deux personnes ne peuvent pas emprunter en meme temps
    livre = db.query(Livre).filter(Livre.id == donnees.livre_id).with_for_update().first()
    if livre is None:
        raise HTTPException(status_code=404, detail="Livre introuvable")
    if not livre.disponible:
        raise HTTPException(status_code=409, detail="Ce livre n'est pas disponible")
    maintenant = datetime.now()
    emprunt = Emprunt(
        utilisateur_id=moi.id,
        livre_id=livre.id,
        date_emprunt=maintenant,
        date_retour_prevue=maintenant + timedelta(days=14),
    )
    livre.disponible = False
    db.add(emprunt)
    db.commit()  # lemprunt et la disponibilite sont enregistrés ensemble
    db.refresh(emprunt)
    return emprunt
@router.post("/{emprunt_id}/retour", response_model=EmpruntOut)
def rendre_livre(
    emprunt_id: int,
    moi: Utilisateur = Depends(get_utilisateur_connecte),
    db: Session = Depends(get_db),
):
    emprunt = db.get(Emprunt, emprunt_id)
    # un membre ne peut rendre que ses propres emprunts 
    if emprunt is None or (emprunt.utilisateur_id != moi.id and moi.role != "admin"):
        raise HTTPException(status_code=404, detail="Emprunt introuvable")
    if emprunt.date_retour is not None:
        raise HTTPException(status_code=409, detail="Ce livre a déjà été rendu")
    emprunt.date_retour = datetime.now()
    emprunt.livre.disponible = True
    db.commit()
    db.refresh(emprunt)
    return emprunt

#liste de tous les emprunts en cours pour l'admin
@router.get("", response_model=list[EmpruntOut], dependencies=[Depends(admin_requis)])
def emprunts_en_cours(db: Session = Depends(get_db)):
    return (
        db.query(Emprunt)
        .filter(Emprunt.date_retour.is_(None))
        .order_by(Emprunt.date_emprunt.desc())
        .all()
    )