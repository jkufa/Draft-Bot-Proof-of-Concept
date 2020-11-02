from tables import *

ins = users.insert()

str(ins)
'INSERT INTO users (id, name, fullname) VALUES (:id, :name, :fullname)'