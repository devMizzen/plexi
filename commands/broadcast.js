const Discord = require("discord.js");
const spawn = require("child_process").spawn;

exports.run = (args, message, bot, cmds) => {
    /*const pythonProcess = spawn('python',["./commands/inventory.py", bot, message, args]);
    pythonProcess.stdout.on('data', (inv) => {
            console.log('success')
        })*/
        message.channel.send("🕑 Please wait...")
        const guilds = bot.guilds.size
        console.log(guilds)
       const channelf =  message.guild.channels.find(channel => channel.name === "plexi-announcements");
        if(channelf){
            console.log('found')
        }else{
            console.log('nope')
        }
}