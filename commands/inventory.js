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

            const datb = cluster.db("Database");
            const inventories = datb.collection("Injectors")

            const invsent = new Discord.RichEmbed()
            .setTitle(`${message.author.username}'s Inventory`)
            .setDescription('Due to the privacy of your inventory it has been sent to dms')
            .setTimestamp()
            .setFooter(`• Requested By: ${message.author.tag}`, message.author.avatarURL)
            message.channel.send(invsent)

            inventories.find({"_id": "inventory"}).toArray().then((docs) => {
            //inventories.findOne({"_id": "userid"}).toArray().then((docs) =>{}
                console.log('Available Documents:');
                docs.forEach((doc, idx, array) => { 
                    const isEmpty = doc.isEmpty;
                    if(isEmpty === true){
                        const inventoryembed1 = new Discord.RichEmbed()
                        .setTitle(`${message.author.username}'s Inventory`)
                        .setDescription("Your inventory is empty.")
                        .setFooter(`• Requested By: ${message.author.tag}`, message.author.avatarURL)
                        message.author.send(inventoryembed1);
                    }
                    else{
                        const inventoryembed1 = new Discord.RichEmbed()
                        .setTitle(`${message.author.username}'s Inventory`)
                        .setDescription("Contents of your inventory.")
                            .addField("Left Hand", doc.lh, true)
                            .addField("Slot 1", doc.slot1, true)
                            .addField("Slot 2", doc.slot2, true)
                            .addField("Slot 3", doc.slot3, true)
                            .addField("Slot 4", doc.slot4, true)
                            .addField("Slot 5", doc.slot5, true)
                            .addField("Slot 6", doc.slot6, true)
                            .addField("Slot 7", doc.slot7, true)
                            .addField("Slot 8", doc.slot8, true)
                            .addField("Slot 9", doc.slot9, true)
                            .addField("Slot 10", doc.slot10, true)
                            .addField("Slot 11", doc.slot11, true)
                            .addField("Slot 12", doc.slot12, true)
                            .addField("Slot 13", doc.slot13, true)
                            .addField("Slot 14", doc.slot14, true)
                            .addField("Slot 15", doc.slot15, true)
                            .addField("Slot 16", doc.slot16, true)
                            .addField("Slot 17", doc.slot17, true)
                        .setFooter(`• Requested By: ${message.author.tag}`, message.author.avatarURL)

                        const invEmbed2 = new Discord.RichEmbed()
                            .addField("Slot 18", doc.slot18, true)
                            .addField("Slot 19", doc.slot19, true)
                            .addField("Slot 20", doc.slot20, true)
                            .addField("Slot 21", doc.slot21, true)
                            .addField("Slot 22", doc.slot22, true)
                            .addField("Slot 23", doc.slot23, true)
                            .addField("Slot 24", doc.slot24, true)
                            .addField("Slot 25", doc.slot25, true)
                            .addField("Slot 26", doc.slot26, true)
                            .addField("Slot 27", doc.slot27, true)
                            .addField("Slot 28", doc.slot28, true)
                            .addField("Slot 29", doc.slot29, true)
                            .addField("Slot 30", doc.slot30, true)
                            .addField("Slot 31", doc.slot31, true)
                            .addField("Slot 32", doc.slot32, true)
                            .addField("Head", doc.head, true)
                            .addField("Chest", doc.chest, true)
                            .addField("Torse", doc.torso, true)
                            .addField("Shoes", doc.shoe, true)
                        
                        .setFooter(`• Requested By: ${message.author.tag}`, message.author.avatarURL)
                        message.author.send(inventoryembed1);
                        message.author.send(invEmbed2);
                    }
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
})
}
