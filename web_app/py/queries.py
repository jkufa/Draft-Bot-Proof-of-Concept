from csv import DictReader
from inspect import getsource
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from db.py.tables import DraftList, DraftListPokemon,League, Match, MatchLeague, Team, TeamMatch,User,Administrator,Coach
from sqlalchemy.ext.declarative import declarative_base
import random
# from flask_sqlalchemy import SQLAlchemy

Base = declarative_base()

def test_func():
  print("test.py accessed")

class Query:
  # def __init__(self,file_path,app):
  def __init__(self,file_path):
    file_path =  file_path
    engine = create_engine('sqlite:///'+file_path)
    Base.metadata.create_all(engine)
    Base.metadata.bind = engine
    DBSession = sessionmaker(bind=engine)
    # globals
    global session
    # global db
    session = DBSession()
    # db = SQLAlchemy(app)

  def ins_league(self, lname, lformat, tierlist):
    tierlist = session.query(DraftList).filter_by(name=tierlist).first()
    league = League(name=lname,format=lformat,dlist_id=tierlist.id)
    session.add(league)
    try:
      session.commit()
    except:
      session.rollback()
      return False
    return True

  def ins_users(self, users, timezones, is_coach, is_admin, lname):
    league = session.query(League).filter_by(name=lname).first()
    for i in range(0,len(users)):
      usr=users[i]
      tz = timezones[i]
      # print(usr, tz, league.id,'\n')
      user = User(username=users[i],timezone=timezones[i],league_id=league.id)
      session.add(user)
      if is_coach[i]:
        coach = Coach(discord_username=users[i])
        session.add(coach)
      if is_admin[i]:
        admin = Administrator(username=users[i])
        session.add(admin)
      try:
        session.commit()
      except:
        session.rollback()
        return False
    return True
    

  def gen_round_robin(self,lname):
    l_id = session.query(League).filter_by(name=lname).first().id
    teams = self.fetch_team_ids(l_id) # list of teams by id
    random.shuffle(teams)
    if len(teams) % 2 != 0:
      teams.append("BYE")
    week_no = 1
    matches = [] # in case unbound
    for i in range(0,len(teams)-1):
      matches = []
      for i in range(0,len(teams)//2):
        match = teams[i],teams[-(i+1)]
        matches.append(match)
      self.ins_weekly_matches(lname, matches, week_no)
      week_no += 1
      # self.ins_match(session.query(MatchSchedule).filter_by(id=))
      teams.insert(1, teams.pop(-1))
    return matches
  
  def ins_weekly_matches(self, lname, matches, week_no):
    league = session.query(League).filter_by(name=lname).first()
    for match in matches:
      if "BYE" not in match:
        m = self.ins_match(week_no)
        ml = self.ins_match_league(league.id,m.id)
        for i in range(0,len(match)):
          team = session.query(Team).filter_by(id=match[i]).first()
          t = self.ins_team_match(team.id, m.id)
    
  def ins_team_match(self, team_id, match_id):
    team_match = TeamMatch(team_id=team_id, match_id=match_id)
    session.add(team_match)
    session.commit()
    return team_match

  def ins_match_league(self, league_id, match_id):
    match_league = MatchLeague(league_id=league_id,match_id=match_id)
    session.add(match_league)
    session.commit()
    return match_league

  def ins_match(self, week_no):
    m = Match(week_no=week_no)
    session.add(m)
    session.commit()
    return m

  # TODO: add function that inserts teams into database so gen_round_robin can run
  def init_teams(self, lname):
    league = self.fetch_league(lname)
    users = session.query(User).filter_by(league_id=league.id).all()
    for user in users:
      coach = session.query(Coach).filter_by(discord_username=user.username).first()
      team_name = str(coach.discord_username).split('#')[0] + "'s Team"
      team = Team(league_id=league.id,coach_username=coach.discord_username,name=team_name)
      session.add(team)
      try:
        session.commit()
      except:
        session.rollback()
        print("exception occured")
  
  def fetch_team_ids(self,league_id):
    teams = session.query(Team).filter_by(league_id=league_id).all()
    ids = []
    for team in teams:
      ids.append(team.id)
    return ids

  def fetch_leagues(self):
    lgs = session.query(League).all()
    return lgs
    
  def fetch_league(self,lname):
    return session.query(League).filter_by(name=lname).first()

  def fetch_users(self):
    return session.query(User).all()

  def fetch_dlist(self,dlist_id):
    return session.query(DraftList).filter_by(id=dlist_id).first()

  def fetch_dlist_pokemon(self,dlist_id):
    return session.query(DraftListPokemon).filter_by(dlist_id=dlist_id).all()

  def del_user(self,username):
    user = session.query(User).filter_by(username=username).first()
    session.delete(user)
    session.commit()
  
  def del_league(self,lname):
    league = session.query(League).filter_by(name=lname).first()
    session.delete(league)
    session.commit()
    

  def fetch_league_dlist(self,lname):
    league = self.fetch_league(lname)
    return session.query(DraftList).filter_by(id=league.dlist_id).first()

  def fetch_tiers(self,dlist_id):
    tiers = []
    q = session.query(DraftListPokemon.pkmn_value).filter_by(dlist_id=dlist_id).distinct().order_by(DraftListPokemon.pkmn_value).all()
    for value in q:
      tiers.append(*value)
    return tiers

  def query_pkmn_name_by_value(self,pkmn_value):
    return session.query(DraftListPokemon.pkmn_name).filter_by(pkmn_value=pkmn_value).all()
