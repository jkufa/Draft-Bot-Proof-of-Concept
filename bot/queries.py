from sqlalchemy import create_engine, func
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
import sys,os,json,requests
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
    winner = "none"
    if "https://replay.pokemonshowdown.com" not in url:
      return "That is not a valid replay!"
    data = requests.get(url=url+".json").json()
    p1 = data["p1"]
    p2 = data["p2"]
    log = data["log"].split("\n")
    teams = self.fetch_teams(log)
    for i in range(0,len(log)):
      print(log[i])
      if "|win|" in log[-i]:
        winner = log[-i].split("|")[-1]

    # TODO: Add db stuff, round robin stuff

    # I'm sorry, I really wanted to do this in one line
    return p1 + "'s team: " + str(teams[0])[1:-1].replace("'","") + "\n" + p2 +"'s team: " + str(teams[1])[1:-1].replace("'","") + "\n" + "Winner: " + winner + "\nDifferential: " + str(abs(self.calc_differential(log)))
  
  def fetch_teams(self, log):
    teams = [[],[]]
    for i in range(0,len(log)):
      if "|poke|" in log[i]:
        mon = log[i].split("|")[-2].split(",")[0]
        if "p1|" in log[i]:
          teams[0].append(mon)
        elif "p2|" in log[i]:
          teams[1].append(mon)
    return teams
  
  def calc_differential(self, log):
    diff = 0
    for i in range(0,len(log)):
      if "|faint|" in log[i]:
        if "p1a:" in log[i]:
          diff -= 1
        elif "p2a:" in log[i]:
          diff += 1
    return diff

  
