from datetime import date, datetime
from pydantic import BaseModel, ConfigDict, EmailStr, Field

#Utilisateurs
class UtilisateurCreate(BaseModel):
    nom: str = Field(min_length=1, max_length=100)
    prenom: str | None = Field(default=None, max_length=100)
    email: EmailStr
    telephone: str | None = Field(default=None, max_length=20)
    mot_de_passe: str = Field(min_length=8)

class UtilisateurOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: int
    nom: str
    prenom: str | None
    email: str
    telephone: str | None
    role: str
    date_inscription: datetime

class Token(BaseModel):
    access_token: str
    token_type: str = "bearer"


#Livres 
class LivreCreate(BaseModel):
    titre: str = Field(min_length=1, max_length=200)
    auteur: str = Field(min_length=1, max_length=150)
    genre: str | None = Field(default=None, max_length=50)
    date_publication: date | None = None

#pour la modification on ne met que les champs qu'on veut changer
class LivreUpdate(BaseModel):
    titre: str | None = Field(default=None, min_length=1, max_length=200)
    auteur: str | None = Field(default=None, min_length=1, max_length=150)
    genre: str | None = Field(default=None, max_length=50)
    date_publication: date | None = None
    disponible: bool | None = None

class LivreOut(LivreCreate):
    model_config =ConfigDict(from_attributes=True)
    id: int
    disponible: bool

#Emprunts 
class EmpruntCreate(BaseModel):
    livre_id: int

class EmpruntOut(BaseModel):
    model_config =ConfigDict(from_attributes=True)
    id: int
    livre: LivreOut
    date_emprunt: datetime
    date_retour_prevue: datetime | None
    date_retour: datetime | None    