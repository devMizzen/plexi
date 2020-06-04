const Discord = require("discord.js");
//const inventory = require("./inventory.json")
const spawn = require("child_process").spawn;
const fs = require('fs');

exports.run = (args, message, bot, cmds, cluster) => {
    const userid = `${message.author.id}`;

    cluster.connect(err => {

        console.log('Connected... Transmission Successful!')
        const pythonProcess = spawn('python',["./commands/inventory.py", message, userid]);
        pythonProcess.stdout.on('data', (inv) => {

            console.log('Received Data... inventory.py Check!')
            const inventoryembed = new Discord.RichEmbed()
            .setTitle(`${message.author.username}'s Inventory`)
            .setDescription("For the sake of privacy of your inventory, it has been sent to your direct messages.")
            .setFooter(`• Requested By: ${message.author.tag}`, message.author.avatarURL)
            message.channel.send(inventoryembed);
        
        });
    });
}
