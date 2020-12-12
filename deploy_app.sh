#!/bin/sh
export FLASK_APP=./web_app/__init__.py
# export FLASK_ENV=development # Comment out when testing for production
flask run