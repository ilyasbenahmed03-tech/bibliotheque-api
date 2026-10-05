#tests utilisateurs
def test_inscription(client):
 r = client.post("/auth/inscription", json={"nom": "Martin", "email": "martin@test.fr", "mot_de_passe": "Motdepasse1"})
 assert r.status_code == 201
 assert r.json()["role"] == "membre"
 assert "mot_de_passe" not in r.json()

def test_inscription_email_deja_utilise(client, membre):
 r = client.post("/auth/inscription", json={"nom": "Autre", "email": "dupont@test.fr", "mot_de_passe": "Motdepasse1"})
 assert r.status_code == 409

def test_inscription_email_invalide(client):
 r = client.post("/auth/inscription", json={"nom": "X", "email": "pas-un-email", "mot_de_passe": "Motdepasse1"})
 assert r.status_code == 422

def test_connexion_mauvais_mdp(client, membre):
 r = client.post("/auth/connexion", data={"username": "dupont@test.fr", "password": "faux"})
 assert r.status_code == 401

def test_profil_sans_token(client):
 assert client.get("/utilisateurs/moi").status_code == 401

def test_profil_avec_token(client, membre):
 r = client.get("/utilisateurs/moi", headers=membre)
 assert r.status_code == 200
 assert r.json()["email"] == "dupont@test.fr"

#tests livres
def test_ajouter_livre_admin(client, admin):
 r = client.post("/livres", json={"titre": "1984", "auteur": "George Orwell"}, headers=admin)
 assert r.status_code == 201
 assert r.json()["disponible"] is True

def test_ajouter_livre_membre(client, membre):
 r = client.post("/livres", json={"titre": "1984", "auteur": "George Orwell"}, headers=membre)
 assert r.status_code == 403

def test_recherche(client, livre):
 assert len(client.get("/livres?titre=dun").json()) == 1
 assert len(client.get("/livres?auteur=HERBERT").json()) == 1
 assert len(client.get("/livres?genre=roman").json()) == 0

def test_modifier_livre(client, admin, livre):
 r = client.patch(f"/livres/{livre['id']}", json={"titre": "Dune 2"}, headers=admin)
 assert r.status_code == 200
 assert r.json()["titre"] =="Dune 2"

def test_livre_introuvable(client):
 assert client.get("/livres/999").status_code == 404

#tests emprunts
def test_emprunter_et_rendre(client, membre, livre):
 r =client.post("/emprunts", json={"livre_id": livre["id"]}, headers=membre)
 assert r.status_code == 201
 emprunt =r.json()
 assert emprunt["livre"]["disponible"] is False
 assert emprunt["date_retour_prevue"] is not None
 r = client.post(f"/emprunts/{emprunt['id']}/retour", headers=membre)
 assert r.status_code ==200
 assert r.json()["livre"]["disponible"] is True

def test_livre_deja_emprunte(client, membre, livre):
 client.post("/emprunts", json={"livre_id": livre["id"]}, headers=membre)
 r =client.post("/emprunts", json={"livre_id": livre["id"]}, headers=membre)
 assert r.status_code == 409

def test_rendre_deux_fois(client, membre, livre):
 emprunt = client.post("/emprunts", json={"livre_id": livre["id"]}, headers=membre).json()
 client.post(f"/emprunts/{emprunt['id']}/retour", headers=membre)
 r = client.post(f"/emprunts/{emprunt['id']}/retour", headers=membre)
 assert r.status_code == 409

def test_en_cours_et_historique(client, membre, livre):
 emprunt = client.post("/emprunts", json={"livre_id": livre["id"]}, headers=membre).json()
 assert len(client.get("/utilisateurs/moi/emprunts", headers=membre).json()) == 1
 client.post(f"/emprunts/{emprunt['id']}/retour", headers=membre)
 assert len(client.get("/utilisateurs/moi/emprunts", headers=membre).json()) == 0
 assert len(client.get("/utilisateurs/moi/historique", headers=membre).json()) == 1