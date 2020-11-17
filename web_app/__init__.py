from flask import Flask, render_template, request, redirect
# from web_app.py.queries import init_league

app = Flask(__name__)
app.debug=True

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
    # POST variables
    req = request.form
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
      # init_league(league_name,league_format,users,timezones,is_coach,is_admin,tierlist)
    return redirect(request.url)
  return render_template('./admin/create_league.html')

@app.route('/manage_leagues', methods=["GET", "POST"])
def manage_leagues():
  return render_template('./admin/manage_leagues.html')

if __name__ == '__main__':
  app.run()
