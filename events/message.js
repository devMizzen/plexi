const Discord = require('discord.js');
const fs = require('fs');

module.exports = (bot, message) => {
  if (message.author.bot) return;
  let prefixes = JSON.parse(fs.readFileSync("./prefixes.json", "utf8"));
  let prefix = undefined;
  if (message.guild != null) {
    if (!prefixes[message.guild.id]) {
      prefixes[message.guild.id] = {
        prefixes: bot.config.prefix
      };
    };
    prefix = prefixes[message.channel.guild.id].prefixes;
  } else prefix = bot.config.prefix;
  if (!message.content.toLowerCase().startsWith(prefix)) return;
  let args = message.content.toLowerCase().slice(prefix.length).trim().split(' ');
  let cmd = bot.commands.get(args[0].toLowerCase());
  let cmds = args.shift().toLowerCase();
  if (cmd == undefined) return;
  cmd.run(args, message, bot, cmds, cluster);
};