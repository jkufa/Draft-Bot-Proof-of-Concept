from sqlalchemy import create_engine, func
from sqlalchemy.orm import query_expression, sessionmaker
from sqlalchemy.ext.declarative import declarative_base
import sys,os,json,requests
sys.path.insert(1, os.path.abspath(os.getcwd())+"/db/py")
from tables import DraftList,League,User,Administrator,Coach,Pokemon,Team,TeamMatch,Match,PokemonTeam

Base = declarative_base()


class Query():
  def __init__(self,file_path,lname):
    file_path =  file_path
    engine = create_engine('sqlite:///'+file_path)
    Base.metadata.create_all(engine)
    Base.metadata.bind = engine
    DBSession = sessionmaker(bind=engine)
    global session
    session = DBSession()
    self.league_id = session.query(League).filter_by(name=lname).first().id


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
    differential = self.calc_differential(log)
    teams = self.fetch_teams(log)
    for i in range(0,len(log)):
      # print(log[i])
      if "|win|" in log[-i]:
        winner = log[-i].split("|")[-1]
    # TODO: Add db stuff, round robin stuff
    coaches = []
    if self.check_showdown_names([p1,p2]):
      for p in [p1,p2]:
        coaches.append(session.query(Coach).filter_by(showdown_username=p).first().discord_username)
        self.update_team(p,differential,winner=True) if winner==p else self.update_team(p,differential)
      self.update_match(coaches, url,differential, winner)

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
    return abs(diff)
  
  def check_showdown_names(self, players):
    for player in players:
      coach = session.query(Coach).filter_by(showdown_username=player).first()
      if coach.discord_username == None:
        return False
    return True      

  def update_match(self,coaches,url,differential,winner):
    teams = []
    for coach in coaches:
      team = session.query(Team).filter_by(coach_username=coach, league_id=self.league_id).first()
      teams.append(team.id)
    t1 = session.query(TeamMatch).filter(TeamMatch.team_id==teams[0]).all()
    t2 = session.query(TeamMatch).filter(TeamMatch.team_id==teams[1]).all()
    for x in t1:
      for y in t2:
        if x.match_id == y.match_id:
          m_id = session.query(Match).filter_by(id=x.match_id).first().id
    match = session.query(Match).filter_by(id=m_id).first()
    match.url=url
    match.differential=differential
    match.winner=winner
    session.commit()
  
  def update_team(self,team,differential,winner=False):
    coach = session.query(Coach).filter_by(showdown_username=team).first()
    t_diff = session.query(Team).filter_by(coach_username=coach.discord_username).first().differential
    print(team)
    if winner:
      t_diff = t_diff + differential
      team = session.query(Team).filter_by(coach_username=coach.discord_username).first()
      team.differential=t_diff
    else:
      t_diff = t_diff - differential
      team = session.query(Team).filter_by(coach_username=coach.discord_username).first()
      team.differential=t_diff
    session.commit()
    print(team)

  def query_team(self, discord_username):
    coach = session.query(Coach).filter_by(discord_username=discord_username).first()
    team = session.query(Team).filter_by(coach_username=coach.discord_username).first()
    return team

  
  def add_pokemon_to_team(self,username,pokemon_name):
    team = self.query_team(username)
    print(team.id)
    pokemon = session.query(Pokemon).filter_by(name=pokemon_name).first()
    if pokemon != None:
      pokemon_team = PokemonTeam(pkmn_name=pokemon_name, team_id = team.id)
      try: 
        session.add(pokemon_team)
      except:
        return("Error adding Pokemon. Perhaps it's already on your team?")
      session.commit()
      return (str(pokemon_name) + " added to team " + str(team.name))
    return ("Error. This Pokemon does not exist!")
  
  def replace_pokemon_on_team(self,username,curr_mon_name,new_mon_name):
    team = self.query_team(username)
    curr_mon = session.query(Pokemon).filter_by(name=curr_mon_name).first()
    new_mon = session.query(Pokemon).filter_by(name=new_mon_name).first()
    if curr_mon != None and new_mon != None:
      pokemon_team = session.query(PokemonTeam).filter_by(pkmn_name=curr_mon.name, team_id=team.id).first()
      if pokemon_team != None:
        pokemon_team.pkmn_name = new_mon.name
        session.commit()
        return("Success! Replaced " + str(curr_mon.name) + " with " + str(new_mon.name))
    return("Error: One of the pokemon you submitted is invalid.")
    





