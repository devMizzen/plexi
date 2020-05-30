const Discord = require('discord.js');

module.exports = (bot) => {
    bot.user.setActivity(`Type ${bot.config.prefix}help`, { type: 'PLAYING' });
    let [ tsmembers, tsguilds, tschannels ] = [ 0, 0, 0 ];
    bot.guilds.forEach(guild => {
      tsmembers += guild.memberCount;   
      tsguilds++;
      tschannels += guild.channels.size;
    });
    console.log(`->> Guilds: ${tsguilds}\n->> Users: ${tsmembers}\n->> Channels: ${tschannels}`);
    return console.log(`Bot started ${bot.user.id}`);
};