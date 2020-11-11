from enum import unique
from sqlalchemy import create_engine, Table, Column, Integer, String, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relation, relationship
from sqlalchemy.sql.sqltypes import Boolean

Base = declarative_base()

teams_matches = Table('teams_matches', Base.metadata,
    Column('match_id', Integer, ForeignKey('match.id'),unique=True),
    Column('team_id', Integer, ForeignKey('team.id'))
)

draftlist_pokemon = Table('draftlist_pokemon', Base.metadata,
    Column('league_id', Integer, ForeignKey('league.id')),
    Column('pokemon_name', Integer, ForeignKey('pokemon.name'))
)

class League(Base):
    __tablename__ = "league"
    id = Column('id', Integer, primary_key=True)
    name = Column('name', String, unique=True)
    format = Column('format', String)
    # UserLeague relationship
    users = relationship("User", back_populates="league")
    # DraftList
    draftlist = relationship("DraftList", back_populates="league")

class User(Base):
    __tablename__ = "user"
    username = Column('username', String, primary_key=True)
    timezone = Column('timezone', String)
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

class Pokemon(Base):
    __tablename__ = "pokemon"
    name = Column('name', String, primary_key=True)
    url = Column('url', String, unique=True)
    # PokemonTeam relationship
    team_id = Column('team_id', Integer, ForeignKey('team.id'))
    team = relationship("Team", back_populates="pokemon")
    #DraftList
    draftlist = relationship("DraftList",secondary='draftlist_pokemon',back_populates='pokemon')


class DraftList(Base):
    __tablename__ = "draftlist"
    id = Column('id',Integer,primary_key=True)
    value = Column('value',Integer)
    is_drafted = Column('is_drafted',Boolean)
    # League
    league_id = Column('league_id', Integer, ForeignKey('league.id'))
    league = relationship("League", back_populates = "draftlist")
    # Pokemon
    pokemon_name= Column('pokemon_name', String, ForeignKey('pokemon.name'), unique=True)
    pokemon = relationship("Pokemon",secondary="draftlist_pokemon",back_populates="draftlist")

class Team(Base):
    __tablename__ = "team"
    id = Column('id', Integer, primary_key=True)
    name = Column('name', String, unique=True)
    differential = Column('differential',Integer)
    wins = Column('wins',Integer)
    # TeamCoach relationship
    coach_username = Column('coach_username',String, ForeignKey('coach.discord_username'))
    coach = relationship("Coach", uselist=False, back_populates="coach")
    # PokemonTeam relationship
    pokemon = relationship("Pokemon", back_populates="team")
    # MatchTeam relationship
    matches = relationship("Match",secondary="teams_matches",back_populates="teams")

class Match(Base):
    __tablename__ = "match"
    id = Column('id', Integer, primary_key=True)
    differential = Column('differential', Integer)
    #Schedules
    week_no = Column('week_no', Integer)
    # MatchTeam relationship
    teams = relationship("Team",secondary="teams_matches",back_populates="matches")


engine = create_engine('sqlite:///pokemon_draft_league.db',echo=True)
Base.metadata.create_all(engine)