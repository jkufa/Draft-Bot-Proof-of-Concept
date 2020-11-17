import csv
import validators
from sqlalchemy import create_engine, select, Table
from sqlalchemy.orm import sessionmaker

from init_tables import Base, DraftList, Pokemon

engine = create_engine('sqlite:///pokemon_draft_league.db',echo=True)
Base.metadata.bind = engine
DBSession = sessionmaker(bind=engine)
session = DBSession()

def init_draftlist():
  rows = []
  with open("ywnb_2.csv","r") as csv_file:
    content = csv.reader(csv_file, delimiter=',')
    mon_values=next(content)
    for row in content:
      rows.append(row)

    for i in range(0,len(mon_values)):
      parse_rows(mon_values,rows,i)

def parse_rows(mon_values,rows, i):
  for row in rows:
    if(row[i] == ''):
      return
    # print(row[i])
    # pkmn = Table("pokemon", Base.metadata, autoload=True)
    # test = select(pkmn.name).where(pkmn.name==row[i])
    # result = session.execute(test).all()
    # print(result)
    # print(test)
    session.add(DraftList(pokemon_value=mon_values[i], pokemon=row[i]))
    # print(i, row[i])

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


f= open("gen8.txt","r")
data = f.read()
pokemons = data.split(', ')

# Check for duplicates
duplicates = set()
for pokemon in pokemons:
    if pokemons.count(pokemon) > 1:
        duplicates.add(pokemon)
print(duplicates)

# add pokemon to db
for pokemon in pokemons:
  url = get_url(pokemon)
  session.add(Pokemon(name=pokemon, url=url))

# add draftlist
init_draftlist()
session.add(DraftList(name="YWNB Season 2"))

session.commit()