import os
from sqlalchemy import create_engine
from tables import Base

file_path = os.path.abspath(os.getcwd())+"/db/py/files/pokemon_draft_league.db"
engine = create_engine('sqlite:///'+file_path,echo=True)
Base.metadata.create_all(engine)