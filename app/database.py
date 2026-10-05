import os
from dotenv import load_dotenv
from sqlalchemy import create_engine, event
from sqlalchemy.orm import DeclarativeBase, sessionmaker

#on recupere les infos du fichier .env
load_dotenv()
HOST = os.getenv("ORACLE_HOST", "localhost")
PORT = os.getenv("ORACLE_PORT", "1521")
SERVICE = os.getenv("ORACLE_SERVICE", "FREEPDB1")
APP_USER = os.getenv("APP_USER")
APP_PASSWORD = os.getenv("APP_PASSWORD")
OWNER_USER = os.getenv("OWNER_USER")
#lAPI se connecte avec biblio_app (le compte qui a le moins de droits)
DATABASE_URL = f"oracle+oracledb://{APP_USER}:{APP_PASSWORD}@{HOST}:{PORT}/?service_name={SERVICE}"
engine = create_engine(DATABASE_URL)

#les tables appartiennent a biblio_owner 
#Donc a chaque connexion on dit pour Oracle de chercher les tables chez biblio_owner,
#sinon on doit ecrire biblio_owner.livre à chaque requête.
@event.listens_for(engine, "connect")
def utiliser_schema_owner(connexion, _):
    cursor = connexion.cursor()
    cursor.execute(f"ALTER SESSION SET CURRENT_SCHEMA = {OWNER_USER}")
    cursor.close()
SessionLocal = sessionmaker(bind=engine, autoflush=False)

class Base(DeclarativeBase):
    pass
#donner une session a chaque requete de lAPI et la ferme a la fin
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()