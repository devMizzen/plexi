const Discord = require("discord.js");
//const inventory = require("./inventory.json")
const spawn = require("child_process").spawn;
const fs = require('fs');

exports.run = (args, message, bot, cmds, cluster) => {
    const userid = `${message.author.id}`;

    cluster.connect(err => {

        const pythonProcess = spawn('python',["./commands/inventory.py", userid]);
        console.log('Connected... Transmission Successful!')
        pythonProcess.stdout.on('data', (inv) => {

            const db = cluster.db("testdb");

            db.listCollections().toArray().then((docs) => {
                console.log('Available collections:');
                docs.forEach((doc, idx, array) => { console.log(doc.name) });
            }).catch((err) => {
                console.log(err);
            }).finally(() => {
                cluster.close();
            });
            
            console.log('Received Data... inventory.py Check!')

            const inventoryembed = new Discord.RichEmbed()
            .setTitle(`${message.author.username}'s Inventory`)
            .setDescription("For the sake of privacy of your inventory, it has been sent to your direct messages.")
            .setFooter(`• Requested By: ${message.author.tag}`, message.author.avatarURL)
            message.channel.send(inventoryembed);
        
        });
    });
}
