import csv

def init_draftlist():
  rows = []
  with open("ywnb_2.csv","r") as csv_file:
    content = csv.reader(csv_file, delimiter=',')
    mon_values=next(content)
    print(mon_values)
    for row in content:
      rows.append(row)

    for i in range(0,len(rows[0])):
      parse_rows(rows,i)

def parse_rows(rows, i):
  for row in rows:
    if(row[i] == ''):
      return
    get_url(row[i])
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
  print(url)




init_draftlist()