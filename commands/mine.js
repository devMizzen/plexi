const Discord = require("discord.js");
const ms = require('ms')
const spawn = require("child_process").spawn;
const talkedRecently = new Set();

exports.run = (args, message, bot, cmds) => {
        const hours = ms(args[0])
        const minutes = ms(args[1])
        const seconds = ms(args[2])

        const millisec = parseInt(hours) + parseInt(minutes) + parseInt(seconds)
        const sec = millisec/1000



        const endhrs = ms(hours / 3600000)
        const endmin = ms(minutes / 60000)
        const endsec = ms(seconds / 1000)

        var today = new Date();
        var date = today.getFullYear()+'-'+(today.getMonth()+1)+'-'+today.getDate();
        var time = today.getHours() + ":" + today.getMinutes() + ":" + today.getSeconds();
        var minestarttime = time+' '+date;

        message.reply(`You started mining at ${time}`)

        var currenthr = today.getHours()
        var currentmin = today.getMinutes()
        var currentsec = today.getSeconds()

        console.log(`${currenthr} : ${currentmin} : ${currentsec}`)
        
        var endhours = parseInt(endhrs) + parseInt(currenthr)
        var endminutes = parseInt(endmin) + parseInt(currentmin)
        var endseconds = parseInt(endsec) + parseInt(currentsec)
        var endtime = endhours + ':' + endminutes + ':' + endseconds;
        message.reply(`You will end mining at ${endtime}`)

    /*if (talkedRecently.has(message.author.id)) {
        
        const minecooldown = new Discord.RichEmbed()
        .setTitle('Mine')
        .setColor(bot.config.error)
        .setDescription(`You are already mining for ${args[0]} ${args[1]} ${args[2]}`)
        message.channel.send(minecooldown)
    } else {
        if (!args[0] || !args[1] || !args[2]){
        const minearg = new Discord.RichEmbed()
        .setTitle('**Error**')
        .setColor(bot.config.error)
        .setDescription('Missing arguments!! Kindly see below for correct usage.')
        .addField('Usage:', `${bot.config.prefix}mine [hours] [minutes] [seconds]`)
        .setTimestamp()
        .setFooter(`• Requested By: ${message.author.tag}`, message.author.avatarURL)
        message.channel.send(minearg)
    }else{
        const hours = ms(args[0])
        const minutes = ms(args[1])
        const seconds = ms(args[2])

        const millisec = parseInt(hours) + parseInt(minutes) + parseInt(seconds)
        const sec = millisec/1000
        if(sec < 0){
            const mineerror = new Discord.RichEmbed()
            .setTitle('Mine Error')
            .setColor(bot.config.error)
            .setDescription('The time cannot be in negative')
            .setTimestamp()
            .setFooter(`• Requested By: ${message.author.tag}`, message.author.avatarURL)
        }else{
        message.reply(sec)
        }

    
    }talkedRecently.add(message.author.id);
    setTimeout(() => {
      // Removes the user from the set after a minute
      talkedRecently.delete(message.author.id);
    }, millisec);
}*/
}