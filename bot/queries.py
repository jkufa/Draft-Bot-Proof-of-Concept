from werkzeug.wrappers import PlainRequest
import discord
from sqlalchemy import create_engine, func, desc
from sqlalchemy.orm import query_expression, sessionmaker
from sqlalchemy.ext.declarative import declarative_base
import sys,os,json,requests
sys.path.insert(1, os.path.abspath(os.getcwd())+"/db/py")
from tables import DraftList,League,User,Administrator,Coach,Pokemon,Team,TeamMatch,Match,MatchLeague,PokemonTeam,DraftListPokemon

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
    self.league = session.query(League).filter_by(name=lname).first()
  
  def register_showdown_user(self,d_user, sd_user):
    try:
      user = session.query(Coach).filter_by(discord_username=d_user).first()
      user.showdown_username = sd_user
      session.commit()
      return True
    except:
      session.rollback()
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
      if "|win|" in log[-i]:
        winner = log[-i].split("|")[-1]
    coaches = []
    if self.check_showdown_names([p1,p2]):
      for p in [p1,p2]:
        coaches.append(session.query(Coach).filter_by(showdown_username=p).first().discord_username)
        self.update_team(p,differential,winner=True) if winner==p else self.update_team(p,differential)
      if not self.update_match(coaches, url,differential, winner):
        return "Error submitting replay. This match has already been submitted!"
    else:
      return "Error submitting replay. These showdown users are not registered!"

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
      if coach == None:
        return False
    return True      

  def update_match(self,coaches,url,differential,winner):
    teams = []
    for coach in coaches:
      team = session.query(Team).filter_by(coach_username=coach, league_id=self.league.id).first()
      teams.append(team.id)
    t1 = session.query(TeamMatch).filter(TeamMatch.team_id==teams[0]).all()
    t2 = session.query(TeamMatch).filter(TeamMatch.team_id==teams[1]).all()
    for x in t1:
      for y in t2:
        if x.match_id == y.match_id:
          m_id = session.query(Match).filter_by(id=x.match_id).first().id
    match = session.query(Match).filter_by(id=m_id).first()
    if not match.url and match.differential == 0:
      match.differential=differential
      match.winner=winner
      match.url=url
      session.commit()
      return True
    return False
  
  def update_team(self,team,differential,winner=False):
    coach = session.query(Coach).filter_by(showdown_username=team).first()
    t_diff = session.query(Team).filter_by(coach_username=coach.discord_username).first().differential
    if winner:
      t_diff = t_diff + differential
      team = session.query(Team).filter_by(coach_username=coach.discord_username).first()
      team.differential=t_diff
    else:
      t_diff = t_diff - differential
      team = session.query(Team).filter_by(coach_username=coach.discord_username).first()
      team.differential=t_diff
    session.commit()

  def query_coach(self, discord_username):
    coach = session.query(Coach).filter_by(discord_username=discord_username).first()
    return coach

  def query_team(self, discord_username):
    coach = self.query_coach(discord_username)
    team = session.query(Team).filter_by(coach_username=coach.discord_username).first()
    return team
  
  def add_pokemon_to_team(self,username,pokemon_name):
    team = self.query_team(username)
    pokemon = session.query(DraftListPokemon).filter_by(dlist_id=self.league.dlist_id,pkmn_name=pokemon_name.capitalize()).first()
    if pokemon != None:
      pokemon_team = PokemonTeam(pkmn_name=pokemon.pkmn_name, team_id = team.id)
      session.add(pokemon_team)
      try: 
        session.commit()
      except:
        session.rollback()
        return("Error adding Pokemon. Perhaps it's already on your team?")
      return (str(pokemon.pkmn_name) + " added to team " + str(team.name))
    return ("Error. This Pokemon does not exist!")
  
  def replace_pokemon_on_team(self,username,curr_mon_name,new_mon_name):
    team = self.query_team(username)
    curr_mon = session.query(Pokemon).filter_by(name=curr_mon_name.capitalize()).first()
    new_mon = session.query(Pokemon).filter_by(name=new_mon_name.capitalize()).first()
    if curr_mon != None and new_mon != None:
      pokemon_team = session.query(PokemonTeam).filter_by(pkmn_name=curr_mon.name, team_id=team.id).first()
      if pokemon_team != None:
        pokemon_team.pkmn_name = new_mon.name
        session.commit()
        return("Success! Replaced " + str(curr_mon.name) + " with " + str(new_mon.name))
    return("Error: One of the pokemon you submitted is invalid.")
  
  def is_admin(self,discord_username):
    admin = session.query(Administrator).filter_by(username=discord_username).first()
    if(admin != None):
      return True
    return False
  
  def rankings(self):
    teams = session.query(Team).filter_by(league_id=self.league.id).order_by(desc(Team.differential)).all()
    out = "Rankings:\n"
    i = 1
    for team in teams:
      out = out + str(i) +  ": " + str(team.name) + "\n"
      i += 1
    return out
  
  def user_info(self,discord_username):
    d = session.query(User).filter(User.username.contains(discord_username)).first()
    if d == None:
      return "Error! That user could not be found."
    c = self.query_coach(d.username)
    t = self.query_team(d.username)
    pkmn = session.query(Pokemon).join(PokemonTeam).filter_by(team_id=t.id).all()
    out = ("**"+ str(c.discord_username) + "'s Info**\nShowdown Username: " + str(c.showdown_username) 
    + "\nTeam: " + str(t.name) + "\nTimezone: " + str(d.timezone) + "\nDifferential: " + str(t.differential) + "\nPokemon: ")
    for mon in pkmn:
      out = out + str(mon.name) + ", "
    return out[0:-2]
  
  def register_showdown(self,discord_username,sd_username):
    c = self.query_coach(discord_username)
    c.showdown_username = sd_username
    session.commit()
    return "Registered showdown username " + sd_username

  def calc_avg_diff(self):
    matches_played = session.query(Match).join(MatchLeague).filter(MatchLeague.league_id==self.league.id).all()
    n = 0
    total = 0
    for match in matches_played:
      if match.differential > 0:
        total += match.differential
        n += 1
    if n == 0:
      n = 1
    return "The average match differential for " + self.league.name + " is " + str(total//n) + "."

  def fetch_player_matches(self, t):
    matches = session.query(Match).join(TeamMatch).filter(TeamMatch.team_id==t.id).filter(TeamMatch.match_id==Match.id).all()
    return matches
  
  def find_coach(self,player):
    return session.query(Coach).filter(Coach.discord_username.contains(player)).first()

  def print_player_matches(self,player):
    c = self.find_coach(player)
    t = self.query_team(c.discord_username)
    matches =  self.fetch_player_matches(t)
    out = player + "'s matches" + "\n"
    for match in matches:
      opponent = session.query(TeamMatch).filter_by(match_id=match.id).filter(TeamMatch.team_id != t.id).first()
      opponent_team = session.query(Team).filter_by(id=opponent.team_id).first()
      out += c.discord_username + " vs. " + opponent_team.coach_username + "\n"
    return out
  
  def fetch_matches_played(self, player):
    matches = self.fetch_player_matches(player)
    played = player + "'s played matches: \n"
    for match in matches:
      if match.url != None:
        played += match.url + "\n"
    return played
  
  def fetch_match(self,p1,p2):
    try:
      p1c = self.find_coach(p1)
      p2c = self.find_coach(p2)
      p1t = self.query_team(p1c.discord_username)
      p2t = self.query_team(p2c.discord_username)
      p1m =  self.fetch_player_matches(p1t)
      p2m =  self.fetch_player_matches(p2t)
    except:
      return "Error: A user could not be found. Make sure you're command is right.\nProper syntax: `!match <user 1>,<user 2>` (no space with comma)"
    for m1 in p1m:
      for m2 in p2m:
        if m1.id == m2.id:
          if m1.url != None:
            return p1c.discord_username + "vs. " +  p2c.discord_username + "\n Match: " + m1.url
          else:
            return p1c.discord_username + "vs. " +  p2c.discord_username + "\n They haven't played yet!"
    return "Error: Could not find match for those 2 users!"


