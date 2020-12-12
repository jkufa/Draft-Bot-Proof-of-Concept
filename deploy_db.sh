#!/bin/sh
rm ./db/pokemon_draft_league.db
python db/py/init_db.py
python db/py/init_data.py