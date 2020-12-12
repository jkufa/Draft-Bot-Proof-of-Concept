import os,csv,requests, sys, random
from time import sleep
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from tables import Base,DraftListPokemon,DraftList,Pokemon,League,User,Administrator,Coach,Team,Match,TeamMatch,MatchLeague,PokemonTeam

file_path = os.path.abspath(os.getcwd())+"/db/"
engine = create_engine('sqlite:///'+file_path+"/pokemon_draft_league.db")
Base.metadata.create_all(engine)
Base.metadata.bind = engine
DBSession = sessionmaker(bind=engine)
session = DBSession()

debug = False

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
  with open(file_path+"tierlists/YWNBSeason2.csv","r") as csv_file:
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
    pokemons = data.split(',')
    for pokemon in pokemons:
      url = get_url(pokemon)
      if debug:
        rq = requests.get(url)
        sleep(.5)
        txt = rq.text
        if txt[txt.find('<title>')+7 : txt.find('</title>')] == "404 Error":
          print(pokemon)
        else:
          session.add(Pokemon(name=pokemon, url=url))
      else:
        session.add(Pokemon(name=pokemon, url=url))
    f.close()

# Create dummy league for testing
def dummy_league():
  lname = "YWNB Draft League"
  lformat = "Gen 8 OU"
  tlist = "YWNB Season 2"
  # Discord Username, Timezone, isCoach, isAdmin, teamname, showdown name
  users = [["Oh Snapple#2136","CT",True,True,"Mogul Mews","ohsnapplegcc"],
          ["Zaperone#5401","ET",True,True,"Bethlehem Baltoys","zaperone"],
          ["Sir Fresh#4649","CT",True,False,"Graceful Greninjas","Sir Fresh"],
          ["ama#1920","ET",True,False,"Sableyetology","donkchonkler"],
          ["BKMon#0900","CT",True,False,"De Soto Dump","BK Mon"],
          ["I am Wilson | Sad#8469","CT",True,False,"Arctic Spheals","wafcasual"],
          ["ur_gr8_aunt#6453","CT",True,False,"Heavy Duty -<BOOTYS>-","billy6beans"],
          ["Frenetic Bandit#9826","ET",True,False,"Gamer Liquid Garchomp","Frenetic bandit"]]
  # Order is same as users
  pkmn_teams = [["Rillaboom","Ferrothorn","Scolipede","Barraskewda","Politoed","Arcanine","Gastrodon","Jolteon","Dusknoir","Liepard","Musharna","Wigglytuff"],
                ["Jirachi","Keldeo","Toxapex","Incineroar","Mimikyu","Exeggutor","Runerigus","Virizion","Drampa","Dubwool","Shuckle","Steelix"],
                ["Dragapult","Alakazam","Skarmory","Milotic","Porygon-Z","Gardevoir","Lucario","Sirfetch'd","Appletun","Claydol","Flareon","Luxray"],
                ["Kommo-o","Magnezone","Scizor","Krookodile","Talonflame","Dragalge","Rotom-Mow","Xatu","Coalossal","Dugtrio-Alola","Sableye","Shedinja"],
                ["Excadrill","Slowbro","Mandibuzz","Cloyster","Darmanitan","Cobalion","Comfey","Roserade","Malamar","Meowstic","Togedemaru","Trevenant"],
                ["Azumarill","Gyarados","Hippowdon","Bisharp","Lycanroc-Dusk","Decidueye","Ditto","Tentacruel","Manectric","Mr. Mime","Persian","Sawk"],
                ["Zeraora","Kingdra","Pelipper","Mamoswine","Tangrowth","Espeon","Goodra","Raboot","Beartic","Dusclops","Marowak","Ninjask"],
                ["Necrozma","Conkeldurr","Toxtricity","Rotom-Heat","Weezing-Galar","Chandelure","Ribombee","Seismitoad","Drifblim","Lanturn","Orbeetle","Rapidash"]]
  replays = ["https://replay.pokemonshowdown.com/gen8ou-1188184507","https://replay.pokemonshowdown.com/gen8ou-1189823264",
             "https://replay.pokemonshowdown.com/gen8ou-1200111650","https://replay.pokemonshowdown.com/gen8ou-1190173070",
             "https://replay.pokemonshowdown.com/gen8ou-1194688981","https://replay.pokemonshowdown.com/gen8ou-1206979017",
             "https://replay.pokemonshowdown.com/gen8ou-1194847379","https://replay.pokemonshowdown.com/gen8ou-1192677666",
             "https://replay.pokemonshowdown.com/gen8ou-1199018284","https://replay.pokemonshowdown.com/gen8ou-1198510815",
             "https://replay.pokemonshowdown.com/gen8ou-1194205240-rqu07wydwm39egc3j9j63z1ka0dcc36pw","https://replay.pokemonshowdown.com/gen8ou-1205847799",
             "https://replay.pokemonshowdown.com/gen8ou-1210228166","https://replay.pokemonshowdown.com/gen8ou-1204738264",
             "https://replay.pokemonshowdown.com/gen8ou-1201335756","https://replay.pokemonshowdown.com/gen8ou-1205930951",
             "https://replay.pokemonshowdown.com/gen8ou-1218146148","https://replay.pokemonshowdown.com/gen8ou-1222590784"]

  ins_league(lname,lformat,tlist)
  ins_users(users,lname)
  gen_round_robin(lname)
  add_pokemon_to_team(users,pkmn_teams)
  for replay in replays:
    submit_replay(replay,lname)

def ins_league(lname, lformat, tierlist):
  tierlist = session.query(DraftList).filter_by(name=tierlist).first()
  league = League(name=lname,format=lformat,dlist_id=tierlist.id)
  session.add(league)
  try:
    session.commit()
  except:
    session.rollback()
    return False
  return True

def ins_users(users, lname):
  league = session.query(League).filter_by(name=lname).first()
  for user in users:
    dname = user[0]
    tz =  user[1]
    is_coach = user[2]
    is_admin = user[3]
    usr = User(username=user[0],timezone=user[1],league_id=league.id)
    session.add(usr)
    if user[2]: # If is coach
      coach = Coach(discord_username=user[0],showdown_username=user[5])
      team = Team(league_id=league.id,coach_username=user[0],name=user[4])
      session.add(coach)
      session.add(team)
    if user[3]: # If is admin
      admin = Administrator(username=user[0])
      session.add(admin)
    try:
      session.commit()
    except:
      session.rollback()
      return False
  return True

def gen_round_robin(lname):
  l_id = session.query(League).filter_by(name=lname).first().id
  teams = fetch_team_ids(l_id) # list of teams by id
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
    ins_weekly_matches(lname, matches, week_no)
    week_no += 1
    # self.ins_match(session.query(MatchSchedule).filter_by(id=))
    teams.insert(1, teams.pop(-1))
  return matches

def fetch_team_ids(league_id):
  teams = session.query(Team).filter_by(league_id=league_id).all()
  ids = []
  for team in teams:
    ids.append(team.id)
  return ids

def ins_weekly_matches(lname, matches, week_no):
    league = session.query(League).filter_by(name=lname).first()
    for match in matches:
      if "BYE" not in match:
        m = ins_match(week_no)
        ml = ins_match_league(league.id,m.id)
        for i in range(0,len(match)):
          team = session.query(Team).filter_by(id=match[i]).first()
          t = ins_team_match(team.id, m.id)

def ins_match(week_no):
  m = Match(week_no=week_no)
  session.add(m)
  session.commit()
  return m

def ins_match_league(league_id, match_id):
  match_league = MatchLeague(league_id=league_id,match_id=match_id)
  session.add(match_league)
  session.commit()
  return match_league

def ins_team_match(team_id, match_id):
  team_match = TeamMatch(team_id=team_id, match_id=match_id)
  session.add(team_match)
  session.commit()
  return team_match

def add_pokemon_to_team(users,pkmn_teams):
    for i in range(len(pkmn_teams)):
      tm = session.query(Team).filter_by(coach_username=users[i][0]).first()
      for pkmn in pkmn_teams[i]:
        pokemon_team = PokemonTeam(pkmn_name=pkmn, team_id = tm.id)
        session.add(pokemon_team)
        try: 
          session.commit()
        except:
          session.rollback()

def submit_replay(url,lname):
  league = session.query(League).filter_by(name=lname).first()
  winner = "none"
  data = requests.get(url=url+".json").json()
  p1 = data["p1"]
  p2 = data["p2"]
  log = data["log"].split("\n")
  differential = calc_differential(log)
  teams = fetch_teams(log)
  for i in range(0,len(log)):
    if "|win|" in log[-i]:
      winner = log[-i].split("|")[-1]
  coaches = []
  if check_showdown_names([p1,p2]):
    for p in [p1,p2]:
      coaches.append(session.query(Coach).filter_by(showdown_username=p).first().discord_username)
      update_team(p,differential,winner=True) if winner==p else update_team(p,differential)
    if not update_match(coaches, url,differential,league.id, winner):
      return "Error submitting replay. This match has already been submitted!"
  else:
    return "Error submitting replay. These showdown users are not registered!"

def fetch_teams(log):
  teams = [[],[]]
  for i in range(0,len(log)):
    if "|poke|" in log[i]:
      mon = log[i].split("|")[-2].split(",")[0]
      if "p1|" in log[i]:
        teams[0].append(mon)
      elif "p2|" in log[i]:
        teams[1].append(mon)
  return teams

def calc_differential(log):
  diff = 0
  for i in range(0,len(log)):
    if "|faint|" in log[i]:
      if "p1a:" in log[i]:
        diff -= 1
      elif "p2a:" in log[i]:
        diff += 1
  return abs(diff)

def check_showdown_names(players):
  for player in players:
    coach = session.query(Coach).filter_by(showdown_username=player).first()
    if coach == None:
      return False
  return True      

def update_match(coaches,url,differential,l_id,winner):
  teams = []
  for coach in coaches:
    team = session.query(Team).filter_by(coach_username=coach, league_id=l_id).first()
    teams.append(team.id)
  t1 = session.query(TeamMatch).filter(TeamMatch.team_id==teams[0]).all()
  t2 = session.query(TeamMatch).filter(TeamMatch.team_id==teams[1]).all()
  for x in t1:
    for y in t2:
      if x.match_id == y.match_id:
        m_id = session.query(Match).filter_by(id=x.match_id).first().id
  match = session.query(Match).filter_by(id=m_id).first()
  if not match.url and match.differential == 0:
    match.differential=differential
    match.winner=winner
    match.url=url
    session.commit()
    return True
  return False

def update_team(team,differential,winner=False):
  coach = session.query(Coach).filter_by(showdown_username=team).first()
  t_diff = session.query(Team).filter_by(coach_username=coach.discord_username).first().differential
  if winner:
    t_diff = t_diff + differential
    team = session.query(Team).filter_by(coach_username=coach.discord_username).first()
    team.differential=t_diff
  else:
    t_diff = t_diff - differential
    team = session.query(Team).filter_by(coach_username=coach.discord_username).first()
    team.differential=t_diff
  session.commit()

#------------------------------------------------------------------------#
# add all pokemon to db
add_pkmn()
session.commit()

# Add initial draftlist
session.add(DraftList(name="YWNB Season 2"))
session.commit()

# Add Pokemon to draftlist
add_initial_draftlist()

if len(sys.argv) > 0:
  if '1' in sys.argv:
    dummy_league()

