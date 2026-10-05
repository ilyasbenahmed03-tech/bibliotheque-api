from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import func
from sqlalchemy.orm import Session
from app.database import get_db
from app.models import Emprunt, Livre
from app.schemas import LivreCreate, LivreOut, LivreUpdate
from app.security import admin_requis
router = APIRouter(prefix="/livres", tags=["Livres"])

def chercher_livre(db: Session, livre_id: int) -> Livre:
    livre = db.get(Livre, livre_id)
    if livre is None:
        raise HTTPException(status_code=404, detail="Livre introuvable")
    return livre

# recherche par titre et lauteur ou genre (tous les filtres sont optionels)
@router.get("", response_model=list[LivreOut])
def lister_livres(
    titre: str | None = None,
    auteur: str | None = None,
    genre: str | None = None,
    db: Session = Depends(get_db),
):
    requete = db.query(Livre)
    # lower() des deux côtés pour que la recherche ne prend pas compte des majuscules
    if titre:
        requete = requete.filter(func.lower(Livre.titre).like(f"%{titre.lower()}%"))
    if auteur:
        requete = requete.filter(func.lower(Livre.auteur).like(f"%{auteur.lower()}%"))
    if genre:
        requete = requete.filter(func.lower(Livre.genre) == genre.lower())
    return requete.order_by(Livre.titre).all()

@router.get("/{livre_id}", response_model=LivreOut)
def detail_livre(livre_id: int, db: Session = Depends(get_db)):
    return chercher_livre(db, livre_id)

@router.post("", response_model=LivreOut, status_code=201, dependencies=[Depends(admin_requis)])
def ajouter_livre(donnees: LivreCreate, db: Session = Depends(get_db)):
    livre = Livre(**donnees.model_dump())
    db.add(livre)
    db.commit()
    db.refresh(livre)
    return livre

@router.patch("/{livre_id}", response_model=LivreOut, dependencies=[Depends(admin_requis)])
def modifier_livre(livre_id: int, donnees: LivreUpdate, db: Session = Depends(get_db)):
    livre = chercher_livre(db, livre_id)
    
    for champ, valeur in donnees.model_dump(exclude_unset=True).items():
        setattr(livre, champ, valeur)
    db.commit()
    db.refresh(livre)
    return livre

@router.delete("/{livre_id}", status_code=204, dependencies=[Depends(admin_requis)])
def supprimer_livre(livre_id: int, db: Session = Depends(get_db)):
    livre = chercher_livre(db, livre_id)
    en_cours = db.query(Emprunt).filter(Emprunt.livre_id == livre_id, Emprunt.date_retour.is_(None)).first()
    if en_cours:
        raise HTTPException(status_code=409, detail="Impossible de supprimer un livre qui est emprunté")
    db.delete(livre)
    db.commit()