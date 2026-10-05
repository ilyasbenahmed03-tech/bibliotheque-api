import os
from logging.config import fileConfig
from alembic import context
from dotenv import load_dotenv
from sqlalchemy import create_engine
from app.database import Base
from app import models 
load_dotenv()

config = context.config
if config.config_file_name is not None:
    fileConfig(config.config_file_name)

target_metadata = Base.metadata

# alembic va se connecté avec biblio_owner pour creer les tables
OWNER_URL = (
    f"oracle+oracledb://{os.getenv('OWNER_USER')}:{os.getenv('OWNER_PASSWORD')}"
    f"@{os.getenv('ORACLE_HOST')}:{os.getenv('ORACLE_PORT')}/?service_name={os.getenv('ORACLE_SERVICE')}"
)

def run_migrations_offline():
    context.configure(url=OWNER_URL, target_metadata=target_metadata, literal_binds=True)
    with context.begin_transaction():
        context.run_migrations()
def run_migrations_online():
    engine = create_engine(OWNER_URL)
    with engine.connect() as connection:
        context.configure(connection=connection, target_metadata=target_metadata)
        with context.begin_transaction():
            context.run_migrations()

if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()