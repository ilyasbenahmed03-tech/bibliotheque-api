from datetime import datetime
from sqlalchemy import (
    Boolean, CheckConstraint, Column, Date, DateTime, ForeignKey, Identity, Integer, String,
)
from sqlalchemy.orm import relationship
from app.database import Base

class Utilisateur(Base):
    __tablename__ = "utilisateur"
    #Oracle refusebtout autre role que ces 2
    __table_args__ = (CheckConstraint("role IN ('membre', 'admin')", name="ck_utilisateur_role"),)
    id = Column(Integer, Identity(), primary_key=True)
    nom = Column(String(100), nullable=False)
    prenom = Column(String(100))
    email = Column(String(255), unique=True, nullable=False)
    telephone = Column(String(20))
    mot_de_passe = Column(String(255), nullable=False)  # on mettra le hash
    role = Column(String(20), nullable=False, default="membre")
    date_inscription = Column(DateTime, nullable=False, default=datetime.now)
    emprunts = relationship("Emprunt", back_populates="utilisateur")

class Livre(Base):
    __tablename__ ="livre"
    id = Column(Integer, Identity(), primary_key=True)
    titre = Column(String(200), nullable=False)
    auteur = Column(String(150), nullable=False)
    genre = Column(String(50))
    date_publication = Column(Date)
    disponible = Column(Boolean, nullable=False, default=True)
    emprunts = relationship("Emprunt", back_populates="livre", passive_deletes=True)

class Emprunt(Base):
    __tablename__ ="emprunt"
    id= Column(Integer, Identity(), primary_key=True)
    utilisateur_id= Column(Integer, ForeignKey("utilisateur.id", ondelete="CASCADE"), nullable=False)
    livre_id= Column(Integer, ForeignKey("livre.id", ondelete="CASCADE"), nullable=False)
    date_emprunt= Column(DateTime, nullable=False, default=datetime.now)
    date_retour_prevue= Column(DateTime) #14 jours apres l.emprunt
    date_retour= Column(DateTime) #vide ouisque  livre nest toujours encore pas rendu
    utilisateur= relationship("Utilisateur", back_populates="emprunts")
    livre= relationship("Livre", back_populates="emprunts")