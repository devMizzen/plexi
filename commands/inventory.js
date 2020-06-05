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

            inventories.findOne({"_id": "userid"}).toArray().then((docs) => {
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
                        .addFields(
                            {name: "Left Hand", value : doc.lh},
                            {name: "Slot 1", value : doc.slot1},
                            {name: "Slot 2", value : doc.slot2},
                            {name: "Slot 3", value : doc.slot3},
                            {name: "Slot 4", value : doc.slot4},
                            {name: "Slot 5", value : doc.slot5},
                            {name: "Slot 6", value : doc.slot6},
                            {name: "Slot 7", value : doc.slot7},
                            {name: "Slot 8", value : doc.slot8},
                            {name: "Slot 9", value : doc.slot9},
                            {name: "Slot 10", value : doc.slot10},
                            {name: "Slot 11", value : doc.slot11},
                            {name: "Slot 12", value : doc.slot12},
                            {name: "Slot 13", value : doc.slot13},
                            {name: "Slot 14", value : doc.slot14},
                            {name: "Slot 15", value : doc.slot15},
                            {name: "Slot 16", value : doc.slot16},
                            {name: "Slot 17", value : doc.slot17}
                        )
                        .setFooter(`• Requested By: ${message.author.tag}`, message.author.avatarURL)

                        const invEmbed2 = new Discord.RichEmbed()
                        .addFields(
                            {name: "Slot 18", value : doc.slot18},
                            {name: "Slot 19", value : doc.slot19},
                            {name: "Slot 20", value : doc.slot20},
                            {name: "Slot 21", value : doc.slot21},
                            {name: "Slot 22", value : doc.slot22},
                            {name: "Slot 23", value : doc.slot23},
                            {name: "Slot 24", value : doc.slot24},
                            {name: "Slot 25", value : doc.slot25},
                            {name: "Slot 26", value : doc.slot26},
                            {name: "Slot 27", value : doc.slot27},
                            {name: "Slot 28", value : doc.slot28},
                            {name: "Slot 29", value : doc.slot29},
                            {name: "Slot 30", value : doc.slot30},
                            {name: "Slot 31", value : doc.slot31},
                            {name: "Slot 32", value : doc.slot32},
                            {name: "Head", value: doc.head},
                            {name: "Chest", value: doc.chest},
                            {name: "Torse", value: doc.torso},
                            {name: "Shoes", value: doc.shoe}
                        )
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
