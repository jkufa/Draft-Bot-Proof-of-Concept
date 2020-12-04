from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from db.py.tables import DraftList,League, Match, MatchSchedule, Team, TeamMatch,User,Administrator,Coach
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
    session.commit()

  def ins_users(self, users, timezones, is_coach, is_admin, lname):
    league = session.query(League).filter_by(name=lname).first()
    for i in range(0,len(users)):
      usr=users[i]
      tz = timezones[i]
      print(usr, tz, league.id,'\n')
      user = User(username=users[i],timezone=timezones[i],league_id=league.id)
      session.add(user)
      if is_coach[i]:
        coach = Coach(discord_username=users[i])
        session.add(coach)
      if is_admin[i]:
        admin = Administrator(username=users[i])
        session.add(admin)
      session.commit()
    
  def select_leagues(self):
    lgs = session.query(League).all()
    return lgs

  def gen_round_robin(self,lname,teams):
    random.shuffle(teams)
    if len(teams) % 2 != 0:
      teams.append("BYE")
    week_no = 0
    matches = [] # in case unbound
    for i in range(0,len(teams)-1):
      matches = []
      for i in range(0,len(teams)//2):
        match = teams[i],teams[-(i+1)]
        matches.append(match)
      week_no += 1
      self.ins_weekly_matches(lname, matches, week_no)
      teams.insert(1, teams.pop(-1))
    return matches
  
  def ins_weekly_matches(self, lname, matches, week_no):
    for match in matches:
      league = session.query(League).filer_by(name=lname).first() # put this in diff function for inserting
      match_schedule = MatchSchedule(league_id=league.id,week_no=week_no)
      session.add(match_schedule)
      m = Match(mschedule_id=match_schedule.id)
      session.add(m)
      for i in range(0,len(match)):
        team = session.query(Team).filter_by(name=match[i])
        team_match = TeamMatch(team_id=team.id, match_id=m.id)
        session.add(team_match)
      session.commit()
  
  def init_teams(lname):
    return None


