from collections import defaultdict
import csv
from sqlalchemy import create_engine, Table, Column, Integer, String, ForeignKey, CheckConstraint
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import backref, relation, relationship

Base = declarative_base()

# Association Tables
class DraftListPokemon(Base):
  __tablename__ = "draftlist_pokemon"
  dlist_id = Column('dlist_id', Integer, ForeignKey('draftlist.id'), primary_key=True)
  pkmn_name = Column('pkmn_name', String, ForeignKey('pokemon.name'), primary_key=True)
  pkmn_value = Column('pkmn_value', String(10))

class TeamMatch(Base):
  __tablename__ = "team_match"
  team_id = Column('team_id', Integer, ForeignKey('team.id'), primary_key=True)
  match_id = Column('match_id', Integer, ForeignKey('match.id'), primary_key=True)

class MatchLeague(Base): #LeagueMatches relationship
  __tablename__ = "match_league"
  match_id = Column('id', Integer, ForeignKey('match.id'), primary_key=True)
  # 1 League Many MatchesScheduled
  league_id = Column('league_id', Integer, ForeignKey('league.id'),primary_key=True)
  # league = relationship('League', back_populates='leagues')

class PokemonTeam(Base):
  __tablename__ = "pokemon_team"
  pkmn_name = Column('pkmn_name', String(25), ForeignKey('pokemon.name'), primary_key=True)
  team_id = Column('team_id', Integer, ForeignKey('team.id'), primary_key=True)

class DraftList(Base):
    __tablename__ = "draftlist"
    id = Column('id', Integer, primary_key=True)
    name = Column('name', String, unique=True)
    pokemons = relationship("Pokemon", secondary="draftlist_pokemon")
    leagues = relationship("League", backref='draftlist')

class Pokemon(Base):
    __tablename__ = "pokemon"
    name = Column('name', String(25), primary_key=True)
    url = Column('url', String(60))
     # M:N, Pokemon to DraftList
    draftlists = relationship("DraftList", secondary="draftlist_pokemon")

class League(Base):
    __tablename__ = "league"
    id = Column('id', Integer, primary_key=True)
    name = Column('name', String(256), unique=True)
    format =  Column('format', String(20))
    # 1 DraftList Many Leagues
    dlist_id = Column('dlist_id', Integer, ForeignKey('draftlist.id'))
    users = relationship("User", cascade="all,delete", backref="league")
    # matches_scheduled = relationship("MatchLeague", back_populates='league')
    matches_leagues = relationship("MatchLeague", cascade="all,delete", backref="league")

class User(Base):
  __tablename__ = "user"
  username = Column('username', String, primary_key=True)
  timezone = Column('timezone', String(6))
  # UserLeague relationship
  league_id = Column('league_id', Integer, ForeignKey('league.id'))
  # league = relationship("League", back_populates = "users")
  coaches = relationship("Coach",cascade="all,delete",backref="user")
  admins = relationship("Administrator",cascade="all,delete",backref="user")

class Administrator(Base):
  __tablename__ = "administrator"
  username = Column(String, ForeignKey('user.username'), primary_key=True)

class Coach(Base):
  __tablename__ = "coach"
  discord_username = Column('discord_username', String, ForeignKey('user.username'), primary_key=True)
  showdown_username = Column('showdown_username', String, unique=True)
  # TeamCoach relationship
  team = relationship("Team", uselist=False, back_populates="coach",cascade="all,delete")
  
class Team(Base):
  __tablename__ = "team"
  id = Column('id', Integer, primary_key=True)
  league_id = Column('league_id', Integer, ForeignKey('league.id'))
  name = Column('name', String(80), CheckConstraint("name != 'BYE'"),unique=True)
  differential = Column('differential', Integer, default=0)
  # TeamCoach relationship
  coach_username = Column('coach_username', String, ForeignKey('coach.discord_username'))
  coach = relationship("Coach", back_populates="team")
  # TeamMatch relationship
  matches = relationship("Match", secondary="team_match",cascade="all,delete",backref="team")

class Match(Base):
  __tablename__ = "match"
  id = Column('id', Integer, primary_key=True)
  # Many matches in one MatchSchedule
  week_no = Column('week_no', Integer)
  # mschedule = relationship("MatchSchedule", back_populates="matches")
  differential = Column('differential', Integer, default=0)
  url = Column('url', String(60))
  winner = Column('winner', String(80))
  # p1 = Column('p1', String(80))
  # p2 = Column('p2', String(80))
  # TeamMatch Relationship
  # teams = relationship("Team", secondary="team_match")