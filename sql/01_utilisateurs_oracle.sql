--compte proprietairee: il peut creer les tables
CREATE USER biblio_owner IDENTIFIED BY "Owner2026"
  DEFAULT TABLESPACE users
  QUOTA UNLIMITED ON users;
GRANT CREATE SESSION, CREATE TABLE, CREATE VIEW, CREATE SEQUENCE,
      CREATE PROCEDURE, CREATE TRIGGER TO biblio_owner;
--role pour lAPI 
CREATE ROLE biblio_app_role;
GRANT CREATE SESSION TO biblio_app_role;
--compte de lAPI :il peut  se connecter 
CREATE USER biblio_app IDENTIFIED BY "App2026";
GRANT biblio_app_role TO biblio_app;
--on verifie
SELECT username, account_status FROM dba_users WHERE username LIKE 'BIBLIO%';

EXIT;