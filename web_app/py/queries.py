from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from db.py.tables import DraftList,League,User,Administrator,Coach
from sqlalchemy.ext.declarative import declarative_base
# from flask_sqlalchemy import SQLAlchemy


Base = declarative_base()

def test_func():
  print("test.py accessed")

class Insert:
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

  def init_league(self, lname, lformat, tierlist):
    tierlist = session.query(DraftList).filter_by(name=tierlist).first()
    league = League(name=lname,format=lformat,dlist_id=tierlist.id)
    session.add(league)
    session.commit()

  def init_users(self, users, timezones, is_coach, is_admin, lname):
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
