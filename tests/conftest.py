# pour les tests on utilise sqlite en memoire , comme ca on TRAVAILLE PAS AVEC la base oracle
import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool
from app.database import Base, get_db
from app.main import app
from app.models import Utilisateur
from app.security import hacher_mot_de_passe
# pour les tests on utilise sqlite en memoire , comme ca on TRAVAILLE PAS AVEC la base oracle
engine_test = create_engine("sqlite://", connect_args={"check_same_thread": False}, poolclass=StaticPool)
SessionTest = sessionmaker(bind=engine_test, autoflush=False)

def get_db_test():
    db= SessionTest()
    try:
     yield db
    finally:
     db.close()
#on remplace get_db par la base de test
app.dependency_overrides[get_db]= get_db_test
@pytest.fixture
def client():
    #on repart avec une base vide pourchaque test
    Base.metadata.drop_all(engine_test)
    Base.metadata.create_all(engine_test)
    db = SessionTest()
    db.add(Utilisateur(nom="Admin", email="admin@test.fr", role="admin", mot_de_passe=hacher_mot_de_passe("Admin1234")))
    db.commit()
    db.close()
    return TestClient(app)

def se_connecter(client, email, mdp):
    r= client.post("/auth/connexion", data={"username": email, "password": mdp})
    return {"Authorization": "Bearer " + r.json()["access_token"]}

@pytest.fixture
def admin(client):
    return se_connecter(client, "admin@test.fr", "Admin1234")

@pytest.fixture
def membre(client):
    client.post("/auth/inscription", json={"nom": "Dupont", "email": "dupont@test.fr", "mot_de_passe": "Motdepasse1"})
    return se_connecter(client, "dupont@test.fr", "Motdepasse1")

@pytest.fixture
def livre(client, admin):
    r = client.post("/livres", json={"titre": "Dune", "auteur": "Frank Herbert", "genre": "Science-fiction"}, headers=admin)
    return r.json()
