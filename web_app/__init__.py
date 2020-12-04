import os, re
from flask import Flask, render_template, request, redirect
from web_app.py.queries import Query

file_path = os.path.abspath(os.getcwd())+"/db/pokemon_draft_league.db"
app = Flask(__name__)
app.debug=True
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///'+ file_path
q = Query(file_path)


@app.route('/')
def index():
  return render_template('index.html')

@app.route('/view_leagues')
def leagues():
  return render_template('leagues.html')

@app.route('/how_to_setup')
def howto():
  return render_template('howto.html')

@app.route('/contact')
def contact():
  return render_template('contact.html')

@app.route('/create_league', methods=["GET", "POST"])
def create_league():
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
    print(users, timezones, is_coach, is_admin)
    q.ins_league(league_name, league_format, tierlist)
    q.ins_users(users,timezones,is_coach,is_admin,league_name)
    q.gen_round_robin(league_name)
    return redirect(request.url)
  return render_template('./admin/create_league.html')

@app.route('/manage_leagues', methods=["GET", "POST"])
def manage_leagues():
  lgs = q.select_leagues()
  lg_names = []
  for lg in lgs:
    lg_names.append(re.sub("[(),']",'',str(lg.name)))
  print(lg_names)
  return render_template('./admin/manage_leagues.html', lg_names=lg_names)

if __name__ == '__main__':
  app.run()
