from sqlalchemy import create_engine, func
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
import sys,os
sys.path.insert(1, os.path.abspath(os.getcwd())+"/db/py/")
from tables import DraftList,League,User,Administrator,Coach,Pokemon

Base = declarative_base()


class Query():
  def __init__(self,file_path):
    file_path =  file_path
    engine = create_engine('sqlite:///'+file_path)
    Base.metadata.create_all(engine)
    Base.metadata.bind = engine
    DBSession = sessionmaker(bind=engine)
    global session
    session = DBSession()

  def register_showdown_user(self,d_user, sd_user):
    try:
      user = session.query(Coach).filter_by(discord_username=d_user).first()
      user.showdown_username = sd_user
      session.commit()
      return True
    except:
      return False

  def select_pokemon(self, pkmn_name):
    try:
      mon = session.query(Pokemon).filter(func.lower(Pokemon.name)==func.lower(pkmn_name)).first()
      return mon.name + ": " + mon.url
    except:
      return "Invalid Pokemon: " + pkmn_name

  def submit_replay(self, url):
    print("test")
  
