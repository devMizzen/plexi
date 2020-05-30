const Discord = require("discord.js");

exports.run = (args, message, bot, cmds) => {
    async function purge() {
        message.delete();
        if (isNaN(args[0])) {
            message.channel.send('Please use a number as your arguments. \n Usage: ' + bot.config.prefix + 'purge <amount>');
            return;
        }

        const fetched = await message.channel.fetchMessages({limit: args[0]});
        console.log(fetched.size + ' messages found, deleting...');

        message.channel.bulkDelete(fetched)
            .catch(error => message.channel.send(`Error: ${error}`));

    }

    if(message.channel.type === 'dm'){
        purge()
    }else{
        purge()
    }
    
}