const Discord = require('discord.js');
const client = new Discord.Client();
const {token} = require('./bot-token.json')
const {prefix} = require('./config.json')


client.on('ready', () => {
  console.log(`Logged in as ${client.user.tag}!`);
});

client.login(token);

if (token !== 'INSERT TOKEN') {
  client.login(token)
} else {
  console.log('\nERROR: Create & insert a token in bot-token.json')
}

// Commands
client.on('message', message => {
  // If message doesnt start with prefix or was sent by a bot, exit
  if (!message.content.startsWith(prefix) || message.author.bot) return;

  // Take argument for command
  const args = message.content.slice(prefix.length).trim().split(' ');
  const command = args.shift().toLowerCase();

  // Submit replay
  if(command === 'submit') {
    if(!args.length) {
      return message.reply('ERROR: No replay provided');
    }
    const replay = args[0]
    if(replay.includes("replay.pokemonshowdown.com")) {
      message.channel.send(`Replay at  ${replay}` );
    }
    else {
      return message.reply("ERROR: That is not a replay! make sure it's from replay.pokemonshowdown.com");

    }
  }

  // Begin Draft
});
