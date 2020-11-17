# import csv
# from sqlalchemy import create_engine
# from sqlalchemy.orm import sessionmaker

# from initialize_tables import Base, League, User, Administrator, Coach, Pokemon, Team, Match

# engine = create_engine('sqlite:///pokemon_draft_league.db',echo=True)
# Base.metadata.bind = engine
# DBSession = sessionmaker(bind=engine)
# session = DBSession()

# def init_league(lname, lformat, users, timezones, is_coach, is_admin, draftlist):
#   session.add(League(name = lname, format=lformat)) 
#   for user in users:
#     for tz in timezones:
#       session.add(User(username=user, timezone=tz))
#   init_draftlist()

# def init_draftlist():
#   rows = []
#   with open("ywnb_2.csv","r") as csv_file:
#     content = csv.reader(csv_file, delimiter=',')
#     mon_values=next(content)
#     print(mon_values)
#     for row in content:
#       rows.append(row)

#     for i in range(0,len(rows[0])):
#       parse_rows(rows,i)

# def parse_rows(rows, i):
#   for row in rows:
#     if(row[i] == ''):
#       return
#     # session.add(Pokemon(name=row[i]), url=get_url(row[i]))
#     # print(i, row[i])

# def get_url(pokemon):
#   # Pokemon with hypen in name that don't need to be split
#   pokemon_with_hypens = [ "Ho-Oh", "Porygon-Z", "Jangmo-o", "Hakamo-o", "Kommo-o"] 
#   if(pokemon in pokemon_with_hypens):
#     url =  "https://www.serebii.net/pokedex-swsh/"+str(pokemon.lower())
#   else:
#     chunks = pokemon.split('-')
#     pokemon_name = chunks[0].replace(" ", "").lower()
#     url =  "https://www.serebii.net/pokedex-swsh/"+str(pokemon_name)
#   return url