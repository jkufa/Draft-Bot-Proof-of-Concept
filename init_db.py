import csv
from sqlalchemy import create_engine, Table, Column, Integer, String, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relation, relationship
from sqlalchemy.sql.sqltypes import Boolean
from sqlalchemy.orm import sessionmaker

Base = declarative_base()

# Association Tables
class DraftListPokemon(Base):
  __tablename__ = "draftlist_pokemon"
  dlist_id = Column('dlist_id', Integer, ForeignKey('draftlist.id'), primary_key=True)
  pkmn_name = Column('pkmn_name', String, ForeignKey('pokemon.name'), primary_key=True)
  pkmn_value = Column('pkmn_value', String(10))

class Schedule(Base): #TeamsMatches relationship
  __tablename__ = "schedule"
  match_id = Column('match_id', Integer, ForeignKey('match.id'), primary_key=True)
  team_id = Column('team_id', Integer, ForeignKey('team.id'), primary_key=True)
  week_no = Column('week_no', Integer)

class DraftList(Base):
    __tablename__ = "draftlist"
    id = Column('id', Integer, primary_key=True)
    name = Column('name', String, unique=True)
    pokemons = relationship("Pokemon", secondary="draftlist_pokemon")
    # pokemons = relationship("Pokemon", secondary="draftlist_pokemon", back_populates="draftlists")

class Pokemon(Base):
    __tablename__ = "pokemon"
    name = Column('name', String(25), primary_key=True)
    url = Column('url', String(60))
     # M:N, Pokemon to DraftList
    draftlists = relationship("DraftList", secondary="draftlist_pokemon")
    # draftlists = relationship("DraftList", secondary="draftlist_pokemon", back_populates="pokemons")

class League(Base):
    __tablename__ = "league"
    id = Column('id', Integer, primary_key=True)
    name = Column('name', String(256), unique=True)
    format =  Column('format', String(20))
    users = relationship("User", back_populates="league")
  
class User(Base):
  __tablename__ = "user"
  username = Column('username', String, primary_key=True)
  timezone = Column('timezone', String(6))
  # UserLeague relationship
  league_id = Column('league_id', Integer, ForeignKey('league.id'))
  league = relationship("League", back_populates = "users")

class Administrator(User):
  __tablename__ = "administrator"
  username = Column(String, ForeignKey('user.username'), primary_key=True)

class Coach(User):
  __tablename__ = "coach"
  discord_username = Column('discord_username', String, ForeignKey('user.username'), primary_key=True)
  showdown_username = Column('showdown_username', String, unique=True)
  # TeamCoach relationship
  team = relationship("Team", uselist=False, back_populates="coach")
  
class Team(Base):
  __tablename__ = "team"
  id = Column('id', Integer, primary_key=True)
  name = Column('name', String(80), unique=True)
  differential = Column('differential', Integer)
  # TeamCoach relationship
  coach_username = Column('coach_username',String, ForeignKey('coach.discord_username'))
  coach = relationship("Coach", uselist=False, back_populates="team")
  # League relationship

class Match(Base):
  __tablename__ = "match"
  id = Column('id', Integer, primary_key=True)
  week_no = Column('week_no', Integer)
  differential = Column('differential', Integer)
  url = Column('url', String(60))
  winner = Column('winner', String(80), unique=True)
  loser = Column('loser', String(80), unique=True)
  # League Relationship
  
  

engine = create_engine('sqlite:///pokemon_draft_league.db',echo=True)
Base.metadata.create_all(engine)