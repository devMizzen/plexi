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

            const datb = cluster.db("Containers");
            const inventories = datb.collection("Inventories")

            inventories.find({"_id": userid}).toArray().then((docs) => {
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
                            .addField("Left Hand", doc.lh)
                            .addField("Slot 1", doc.slot1)
                            .addField("Slot 2", doc.slot2)
                            .addField("Slot 3", doc.slot3)
                            .addField("Slot 4", doc.slot4)
                            .addField("Slot 5", doc.slot5)
                            .addField("Slot 6", doc.slot6)
                            .addField("Slot 7", doc.slot7)
                            .addField("Slot 8", doc.slot8)
                            .addField("Slot 9", doc.slot9)
                            .addField("Slot 10", doc.slot10)
                            .addField("Slot 11", doc.slot11)
                            .addField("Slot 12", doc.slot12)
                            .addField("Slot 13", doc.slot13)
                            .addField("Slot 14", doc.slot14)
                            .addField("Slot 15", doc.slot15)
                            .addField("Slot 16", doc.slot16)
                            .addField("Slot 17", doc.slot17)
                        .setFooter(`• Requested By: ${message.author.tag}`, message.author.avatarURL)

                        const invEmbed2 = new Discord.RichEmbed()
                            .addField("Slot 18", doc.slot18)
                            .addField("Slot 19", doc.slot19)
                            .addField("Slot 20", doc.slot20)
                            .addField("Slot 21", doc.slot21)
                            .addField("Slot 22", doc.slot22)
                            .addField("Slot 23", doc.slot23)
                            .addField("Slot 24", doc.slot24)
                            .addField("Slot 25", doc.slot25)
                            .addField("Slot 26", doc.slot26)
                            .addField("Slot 27", doc.slot27)
                            .addField("Slot 28", doc.slot28)
                            .addField("Slot 29", doc.slot29)
                            .addField("Slot 30", doc.slot30)
                            .addField("Slot 31", doc.slot31)
                            .addField("Slot 32", doc.slot32)
                            .addField("Head", doc.head)
                            .addField("Chest", doc.chest)
                            .addField("Torse", doc.torso)
                            .addField("Shoes", doc.shoe)
                        
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
