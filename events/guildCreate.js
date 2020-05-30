const Discord = require("discord.js");
module.exports = (bot, guild) => {
    console.log(`New guild joined: ${guild.name} (id: ${guild.id}). This guild has ${guild.memberCount} members!`);
    let channelID;
    let channels = guild.channels;
    channelLoop:
    for (let c of channels) {
        let channelType = c[1].type;
        if (channelType === "text") {
            channelID = c[0];
            break channelLoop;
        }
    }

    let channel = bot.channels.get(guild.systemChannelID || channelID);
    const guildcreate = new Discord.RichEmbed()
    .setTitle('Plexi')
    .setColor('#0ABDE5')
    .setDescription('Thanks for inviting me into this server!\n\n-> Kindly create the channels exactly named as follows for the full functionality of the bot:\n-> #plexi-announcements')
    .setTimestamp()
    .setFooter('• Plexi Minecraft Bot •')
    channel.send(guildcreate);
};