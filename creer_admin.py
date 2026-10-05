#creer le compte administrateur 
from app.database import SessionLocal
from app.models import Utilisateur
from app.security import hacher_mot_de_passe

EMAIL = "admin@biblio.fr"
MOT_DE_PASSE = "Admin2026"
db = SessionLocal()
if db.query(Utilisateur).filter(Utilisateur.email == EMAIL).first():
    print("L'admin existe déjà")
else:
    admin = Utilisateur(
     nom="Admin",
     prenom="Bibliothèque",
     email=EMAIL,
     mot_de_passe=hacher_mot_de_passe(MOT_DE_PASSE),
     role="admin",
    )
    db.add(admin)
    db.commit()
    print("Admin créé :", EMAIL)
db.close()