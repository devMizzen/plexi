const Discord = require("discord.js");

exports.run = (args, message, bot, cmds) => {
	const helpembed = new Discord.RichEmbed()
		.setTitle('• Help Center •')
		//.setThumbnail(`https://media.discordapp.net/attachments/648654014593892369/649501194598875155/DQbot_help_icon.png`)
		.setDescription(`**Commands:**\n-> ${bot.config.prefix}help\n-> ${bot.config.prefix}inventory\n-> ${bot.config.prefix}report\n\nBot is currently under Development`)
		.setTimestamp()
		.setColor("#FFFFFF")
		.setFooter(`• Requested By: ${message.author.tag}`, message.author.avatarURL);
		message.channel.send(helpembed);

};
	