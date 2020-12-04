from itertools import combinations 
import numpy as np
import random

teams = ["Heavy Duty -<BOOTYS>-","Bethlehem Baltoys","Rolla Regards","Graceful Greninjas", "Tubular Toobys"]

pairings = list(combinations(teams,2))

# n = number of competitors
# n/2(n-1) games
# n-1 rounds


# week = []
# for match in pairings:
#   print(match)
# week1 = pairings[::len(teams)]
# print(*week1)

print(teams)
random.shuffle(teams)
print(teams)
if len(teams) % 2 != 0:
  teams.append("BYE")
week_no = 0
for i in range(0,len(teams)-1):
  matches = []
  for i in range(0,len(teams)//2):
    match = teams[i],teams[-(i+1)]
    matches.append(match)
  week_no += 1
  for m in matches:
    print(m[0], m[1])
  teams.insert(1, teams.pop(-1))
