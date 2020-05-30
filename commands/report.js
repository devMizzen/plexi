const Discord = require("discord.js");

exports.run = (args, message, bot, cmds) => {
    if(args[0]){
        const reportembed = new Discord.RichEmbed()
        .setColor("00FFFF")
        .setThumbnail(message.author.avatarURL)
        .setTitle('**Report**')
        .addField('User', message.author.tag)
        .addField('User ID', message.author.id)
        .addField('Channel ID', message.channel.id)
        .addField('Server', message.guild)
        .addField('Server ID', message.guild.id)
        .addField('Issue', message.content.slice(8))
        .setTimestamp()
        .setFooter(`• Requested By: ${message.author.tag}`, message.author.avatarURL)
        bot.guilds.get('697466257515085886').channels.get('715604212880244780').send("<@&715603575019143239>");
        bot.guilds.get('697466257515085886').channels.get('715604212880244780').send(reportembed);
        
        message.delete()

        const confembed = new Discord.RichEmbed()
        .setColor("#00FFFF")
        .setTitle('Report Submitted')
        .setFooter(`• Requested By: ${message.author.tag}`, message.author.avatarURL)
        message.channel.send(confembed)
          .then(msg => {
            msg.delete(5000)
          })}else{
            const err = new Discord.RichEmbed()
            .setColor("#FF0000")
            .setTitle('**Error**')
            .setDescription('Please explain the reason for your report\n'+bot.config.prefix+'report [explain your issue here]')
            .setFooter(`• Requested By: ${message.author.tag}`, message.author.avatarURL)
            message.channel.send(err)
          }
}