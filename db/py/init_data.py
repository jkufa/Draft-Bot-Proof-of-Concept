import csv
import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from tables import Base,DraftListPokemon,DraftList,Pokemon

file_path = os.path.abspath(os.getcwd())+"/db/"
engine = create_engine('sqlite:///'+file_path+"/pokemon_draft_league.db")
Base.metadata.create_all(engine)
Base.metadata.bind = engine
DBSession = sessionmaker(bind=engine)
session = DBSession()

def get_url(pokemon):
  # Pokemon with hypen in name that don't need to be split
  pokemon_with_hypens = [ "Ho-Oh", "Porygon-Z", "Jangmo-o", "Hakamo-o", "Kommo-o"] 
  if(pokemon in pokemon_with_hypens):
    url =  "https://www.serebii.net/pokedex-swsh/"+str(pokemon.lower())
  else:
    chunks = pokemon.split('-')
    pokemon_name = chunks[0].replace(" ", "").lower()
    url =  "https://www.serebii.net/pokedex-swsh/"+str(pokemon_name)
  return url

def add_initial_draftlist():
  rows = []
  with open(file_path+"tierlists/ywnb_2.csv","r") as csv_file:
    data = csv.reader(csv_file, delimiter=',')
    tiers = next(data)
    for row in data:
      rows.append(row)
    for i in range(0,len(tiers)):
      col = fetch_col(rows,i)
      insert_by_col(tiers[i],col)

# Get all Pokemon in each column
def fetch_col(rows, i):
  col = []
  for row in rows:
    if(row[i] == ''):
      return col
    col.append(row[i])
  return col

def insert_by_col(tier,col):
  mons = session.query(Pokemon).filter(Pokemon.name.in_(col)).all()
  dlist = session.query(DraftList).filter(DraftList.id == 1).first()
  for mon in mons:
    dlist_mon = DraftListPokemon(dlist_id=dlist.id, pkmn_name=mon.name,pkmn_value=tier)
    session.add(dlist_mon)

    # print(mon.name)
  # dlist.pokemons = [mon for mon in mons]
  session.commit()

# Check for duplicates
def check_duplicates(pokemons):
    for pokemon in pokemons:
        if pokemons.count(pokemon) > 1:
            print(pokemon + "Has a duplicate!")
            return False
    return True

# add pokemon to db
def add_pkmn():
    # INITIALIZE DATA #
    f= open(file_path+"gen8.txt","r")
    data = f.read()
    pokemons = data.split(', ')
    for pokemon in pokemons:
        url = get_url(pokemon)
        session.add(Pokemon(name=pokemon, url=url))
    f.close()

# add all pokemon to db
add_pkmn()
session.commit()

# Add initial draftlist
session.add(DraftList(name="YWNB Season 2"))
session.commit()

# Add Pokemon to draftlist
add_initial_draftlist()
