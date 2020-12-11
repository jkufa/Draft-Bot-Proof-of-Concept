from db.py.tables import DraftList
import os, re, csv
from flask import Flask, render_template, request, redirect
from web_app.py.queries import Query

base_file_path = os.path.abspath(os.getcwd())
file_path = base_file_path+"/db/pokemon_draft_league.db"

app = Flask(__name__)
app.debug=True
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///'+ file_path

def read_draftlist(csv_name):
  rows = []
  with open(base_file_path+"/db/tierlists/"+csv_name+".csv","r") as csv_file:
    data = csv.reader(csv_file, delimiter=',')
    headings = next(data)
    for row in data:
      rows.append(row)
      print(row)
  return headings,rows

@app.route('/')
def index():
  return render_template('index.html')

@app.route('/draftlists', methods=['GET','POST'])
def leagues():
  q = Query(file_path)
  leagues = q.fetch_leagues()
  if request.method =="POST":
    req = request.form
    get_lg = req.get("sel-league")
    draftlist = q.fetch_league_dlist(get_lg)
    tiers,rows = read_draftlist(draftlist.name.replace(' ',''))
    return render_template('draftlists.html',leagues=leagues,tiers=tiers,rows=rows,button_pressed=True)
  return render_template('draftlists.html',leagues=leagues,button_pressed=False)

@app.route('/how_to_setup')
def howto():
  return render_template('howto.html')

@app.route('/contact')
def contact():
  return render_template('contact.html')

@app.route('/create_league', methods=["GET", "POST"])
def create_league():
  q = Query(file_path)
  if request.method == "POST":
    req = request.form
    # POST variables
    league_name = req.get("leaguename")
    league_format = req.get("format")
    user_num = int(req.get("create_league"))+1 # get num of users
    users = []
    timezones = []
    is_coach = []
    is_admin = []
    tierlist = req.get("tierlist")
    for i in range(0,user_num):
      users.append(req.get("discord_username"+str(i)))
      timezones.append(req.get("timezone"+str(i)))
      if(req.get("check-coach"+str(i)) != None):
        is_coach.append(True)
      else:
        is_coach.append(False)
      if(req.get("check-admin"+str(i)) != None):
        is_admin.append(True)
      else:
        is_admin.append(False)
    # Send data to database
    # print(users, timezones, is_coach, is_admin)
    q.ins_league(league_name, league_format, tierlist)
    q.ins_users(users,timezones,is_coach,is_admin,league_name)
    q.init_teams(league_name)
    matches = q.gen_round_robin(league_name)
    # q.ins_weekly_matches(league_name, matches)
    return redirect(request.url)
  return render_template('./admin/create_league.html')

@app.route('/manage_leagues', methods=["GET", "POST"])
def manage_leagues():
  q = Query(file_path)
  lgs = q.fetch_leagues()
  users = q.fetch_users()
  if request.method == "POST":
    req = request.form
    user = req.get("del-user")
    league = req.get("del-league")
    if user:
      print("deleting " + str(user))
      q.del_user(user)
    elif league:
      print("deleting " + str(league))
      q.del_league(league)
    return redirect(request.url)
  return render_template('./admin/manage_leagues.html', lgs=lgs, users=users)

if __name__ == '__main__':
  app.run()
