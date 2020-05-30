const Discord = require('discord.js');

module.exports = (bot, guild) => {
    return console.log(`I have been removed from: ${guild.name} (id: ${guild.id})`);
};