import discord
import json

# load in JSON files
with open('bot-token.json','r') as myfile:
  data = myfile.read()
token_data = json.loads(data)
with open('config.json','r') as myfile:
  data = myfile.read()
config_data = json.loads(data)

client = discord.Client()
token = token_data['token']
prefix  = config_data['prefix']

@client.event
async def on_ready():
  print('Logged in as {0.user}'.format(client))

@client.event
async def on_message(message):
  # Return if message is sent by bot
  if(message.author == client.user):
    return
  if(config_data["adminrole"].lower() in [y.name.lower() for y in message.author.roles]):
      await message.channel.send("User has role " + config_data["adminrole"])
  else:
      print(message.author.roles)
      print(config_data["adminrole"])
  # See if command is being run
  if(message.content.startswith(prefix)):
    args = message.content[1:].split(' ')
    if(args[0] == ''):
      await message.channel.send("ERROR: No command was given!")
      return
    command = args.pop(0) # Pop first index, it will always be the command

    #See what command was given
    if(command.lower() == "select"):
      if(not args):
        await message.channel.send("ERROR: You're missing parameters. Type !help for more info")
        return
      await message.channel.send("TODO: !" + command.lower())
      await message.channel.send(args[0])
    elif(command.lower() == "submit"):
      await message.channel.send("TODO: !" + command.lower())
    elif(command.lower() == "redraft"):
      await message.channel.send("TODO: !" + command.lower())
    elif(command.lower() == "delete"):
      await message.channel.send("TODO: !" + command.lower())
    elif(command.lower() == "userinfo"):
      await message.channel.send("TODO: !" + command.lower())
    elif(command.lower() == "rankings"):
      await message.channel.send("TODO: !" + command.lower())
    elif(command.lower() == "matchesplayed"):
      await message.channel.send("TODO: !" + command.lower())
    elif(command.lower() == "pokemon"):
      await message.channel.send("TODO: !" + command.lower())
    elif(command.lower() == "average" or command.lower() == "avg"):
      await message.channel.send("TODO: !" + command.lower())
    else:
      await message.channel.send("Hey, that's not a valid command!")


client.run(token)