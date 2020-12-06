from inspect import getsource
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
      # print(usr, tz, league.id,'\n')
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

  def gen_round_robin(self,lname):
    l_id = session.query(League).filter_by(name=lname).first().id
    teams = self.fetch_team_ids(l_id) # list of teams by id
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
      print(week_no, matches)
      # self.ins_match(session.query(MatchSchedule).filter_by(id=))
      teams.insert(1, teams.pop(-1))
    return matches
  
  def ins_weekly_matches(self, lname, matches, week_no):
    league = session.query(League).filter_by(name=lname).first()
    for match in matches:
      if "BYE" not in match:
        self.ins_match_schedule(league.id, week_no)
        match_schedule = session.query(MatchSchedule).filter_by(week_no=week_no).all()
        for m_s in match_schedule:
          self.ins_match(m_s.id)
          m = session.query(Match).filter_by(mschedule_id=m_s.id).first()
          for i in range(0,len(match)):
            team = session.query(Team).filter_by(id=match[i]).first()
            team_match = TeamMatch(team_id=team.id, match_id=m.id)
            session.add(team_match)
            session.commit()
    
  def ins_match_schedule(self, league_id, week_no):
    match_schedule = MatchSchedule(league_id=league_id,week_no=week_no)
    session.add(match_schedule)
    session.commit()
    return match_schedule

  def ins_match(self, m_s_id):
    m = Match(mschedule_id=m_s_id)
    session.add(m)
    session.commit()

  # TODO: add function that inserts teams into database so gen_round_robin can run
  def init_teams(self, lname):
    league = session.query(League).filter_by(name=lname).first()
    users = session.query(User).filter_by(league_id=league.id).all()
    for user in users:
      # print(user.username)
      coach = session.query(Coach).filter_by(discord_username=user.username).first()
      team = Team(league_id=league.id,coach_username=coach.discord_username)
      session.add(team)
    session.commit()
  
  def fetch_team_ids(self,league_id):
    teams = session.query(Team).filter_by(league_id=league_id).all()
    ids = []
    for team in teams:
      ids.append(team.id)
    return ids

  

