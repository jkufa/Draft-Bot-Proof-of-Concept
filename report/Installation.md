# Installation Instructions

## How to Setup
Setting up Drafty locally is a breeze! First, ensure the following prerequisites are met:
* Python version 3.9 is installed along with pip (Any version that is 3.6+ will likely work, but 3.9 was used during development)
* A compatible OS is being used (Fedora 33 was used during development)
* A Discord account
* Drafty is downloaded locally

### Step 0: Initialize a Virtual Environment (Optional)
Before running the app, it is recommended that a virtual environment is used. To use a virtual environment, first install `virtualenv` using `pip install virtualenv`
* First, ensure you're in the Draft-Bot directory
* Run `virtualenv venv` where `venv` is the name of your choice for the virtual environment
* Run `. venv/bin/activate`

You should now be in a virtual environment!

### Step 1: Install Packages
To make the process of installing dependencies easier, a `requirements.txt` file exists. Simply run `pip install -r requirements.txt` to download all necessary packages.

### Step 1.5: Reset the Database (Optional)
The database comes initialized with some dummy data to be used for queries. If you would like to clear the database and initialize it with only the barebones data, simply perform the following:
* Run the file with `./deploy_app.sh`
If the script fails to run, try giving it permissions using `chmod -x deploy_db.sh`

If you would like to add back the dummy data, simply run the same script with a parameter 1: `./deploy_app.sh 1`.

### Step 2: Run the Web App
To locally run the web application, perform the following:
* Run the file with `./deploy_app.sh`. If the script fails to run, try giving it permissions using `chmod -x deploy_app.sh`
* Go to http://127.0.0.1:5000/ in your web browser

Inside the web app you are able to create and manage leagues, as well as view draft lists for these leagues. To read a tutorial on navigating the web application, see the separate documentation under "User Manual."

### Step 3: Run the Discord Bot
To run the Discord Bot, either end the current web application with ctrl+c, or run the bot in a new terminal window. One instance of the discord bot is tied to a single league.
* Run the file with `./deploy_bot.sh`. If the script fails to run, try giving it permissions using `chmod -x deploy_bot.sh`
* After running, the program will prompt you to enter a league name. League names are case sensitive!
* Follow the url that is posted to join the discord server, and begin interacting with Drafty!

If instead you would like to add Drafty to your own discord, please follow the separate documentation under "User Manual."