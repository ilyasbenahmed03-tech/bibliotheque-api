# API Bibliotheque en ligne

Mini projet 5BDDD (SUPINFO).
## ILYAS BENAHMED ET MAHMOUD QZIBAR 
API pour gerer une bibliotheque : les utilisateurs, les livres et les emprunts.

Techniques : FastAPI, Oracle (Docker), SQLAlchemy, Alembic, Pydantic, JWT.

## Ce que fait l'API

- inscription / connexion (mot de passe hache avec argon2, token JWT de 60 min)
- les livres : ajout, modif, suppression (admin seulement) et recherche par titre, auteur ou genre
- emprunter un livre (seulement s'il est dispo) et le rendre
- voir ses emprunts en cours et son historique
- la doc swagger est sur /docs

## Securite de la base

On n'utilise pas le compte system. Il y a 2 comptes Oracle :
- biblio_owner : c'est lui qui a les tables, on l'utilise que pour les migrations Alembic
- biblio_app : c'est le compte de l'API, il peut juste faire SELECT/INSERT/UPDATE/DELETE (via le role biblio_app_role)

Comme ca meme si quelqu'un passe par l'API il peut pas supprimer ou modifier les tables.

## Lancer le projet

1. Oracle avec docker
```
docker run -d --name orcl-free -p 1521:1521 -e ORACLE_PASSWORD=SUPINFO2025 gvenzl/oracle-free:23-slim
```

2. Creer les comptes (avec system)
```
docker cp sql/01_utilisateurs_oracle.sql orcl-free:/tmp/
docker exec -it orcl-free sqlplus system/SUPINFO2025@FREEPDB1 "@/tmp/01_utilisateurs_oracle.sql"
```

3. Installer
```
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
```
puis copier `.env.example` en `.env` et remplir les mots de passe.

4. Creer les tables puis donner les droits a l'API
```
alembic upgrade head
docker cp sql/02_droits_api.sql orcl-free:/tmp/
docker exec -it orcl-free sqlplus biblio_owner/Owner2026@FREEPDB1 "@/tmp/02_droits_api.sql"
```

5. Creer l'admin et lancer
```
python creer_admin.py
uvicorn app.main:app --reload
```
Aller sur http://127.0.0.1:8000/docs

## Routes

Auth
- POST /auth/inscription
- POST /auth/connexion

Utilisateurs
- GET /utilisateurs/moi
- GET /utilisateurs/moi/emprunts (en cours)
- GET /utilisateurs/moi/historique
- GET /utilisateurs (admin)
- GET /utilisateurs/{id}/historique (admin)

Livres
- GET /livres?titre=&auteur=&genre=
- GET /livres/{id}
- POST /livres (admin)
- PATCH /livres/{id} (admin)
- DELETE /livres/{id} (admin)

Emprunts
- POST /emprunts
- POST /emprunts/{id}/retour
- GET /emprunts (admin, les emprunts en cours)

## Migrations

```
alembic history
<base> -> b6ce4d3ae5e2, creation des tables
b6ce4d3ae5e2 -> 55582e873101 (head), ajout date de retour prevue
```

## Tests

```
pytest -v
```
les tests utilisent sqlite en memoire donc ils touchent pas a Oracle.