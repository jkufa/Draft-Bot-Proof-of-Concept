#!/bin/sh
rm ./db/pokemon_draft_league.db
python3.9 ./db/py/init_db.py
python3.9 ./db/init_data.py