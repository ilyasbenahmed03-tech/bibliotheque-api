--pour lancer avec biblio_owner, une fois que les tables existent
GRANT SELECT, INSERT, UPDATE, DELETE ON utilisateur TO biblio_app_role;
GRANT SELECT, INSERT, UPDATE, DELETE ON livre TO biblio_app_role;
GRANT SELECT, INSERT, UPDATE, DELETE ON emprunt TO biblio_app_role;

EXIT;