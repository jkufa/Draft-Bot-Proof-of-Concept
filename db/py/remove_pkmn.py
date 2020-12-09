file = open('../gen8.txt')
data = file.read()
mons = data.split(', ')

file = open('remove.txt')
data = file.read()
remove_mons = data.split('\n')

for mon in remove_mons:
  if mon in mons:
    mons.remove(mon)

out = ""
for mon in mons:
  out = out + mon + ","
  if mon == mons[-1]:
    out = out[0:-1]
print(out)
