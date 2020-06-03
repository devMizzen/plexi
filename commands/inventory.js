const Discord = require("discord.js");
//const inventory = require("./inventory.json")
const spawn = require("child_process").spawn;
const fs = require('fs');

exports.run = (args, message, bot, cmds, cluster) => {
    const userid = `${message.author.id}`;

    cluster.connect(err => {

    
    
    console.log('Connected... Transmission Successful!')
    const pythonProcess = spawn('python',["./commands/inventory.py", userid]);
    pythonProcess.stdout.on('data', (inv) => {

        const db = cluster.db('plexi_users')
        const player = db.collection(userid);
        const dependancies = db.collection("Dependancies")
        
        const inventory = player.findOne({'_id': 'inventory'})
        player.find({'_id': 'inventory'}).toArray((err, items) => {console.log(items)});
        const userList = dependancies.findOne({_id: "UserList"});

        /*player.find({'_id': 'inventory'}).toArray((err, items) => {   
            console.log(items)
          })

        console.log(Object.values(userList));*/

        console.log(inventory);
        console.log(inventory.isEmpty)

        const inventoryembed = new Discord.RichEmbed()
        .setTitle(`${message.author.username}'s Inventory`)
        .setDescription("For the sake of privacy of your inventory, it has been sent to your direct messages.")
        .setFooter(`• Requested By: ${message.author.tag}`, message.author.avatarURL)
        message.channel.send(inventoryembed);
        
        //message.reply(inventory.check)
        //if(inv.toString() === 0){
        
        if(inventory.isEmpty === true){
        //if(inventory.check === '-'){
        const inventorycheck = new Discord.RichEmbed()
        .setTitle(`${message.author.username}'s Inventory`)
        .setDescription("Your inventory is currently empty! Go fill me in!!")
        .setFooter(`• Requested By: ${message.author.tag}`, message.author.avatarURL)
        message.author.send(inventorycheck);
        } 
        //message.reply(inventory.check)
        //if(inv.toString() === 0){
        if(inventory.isEmpty === false){     
        
            const inventoryshow1 = new Discord.RichEmbed()
            .setTitle(`${message.author.username}'s Inventory`)  
            .addField('Left Hand', inventory.lh, true)
            .addField('Slot 1', inventory.slot1, true)
            .addField('Slot 2', inventory.slot2, true)
            .addField('Slot 3', inventory.slot3, true)
            .addField('Slot 4', inventory.slot4, true)
            .addField('Slot 5', inventory.slot5, true)
            .addField('Slot 6', inventory.slot6, true)
            .addField('Slot 7', inventory.slot7, true)
            .addField('Slot 8', inventory.slot8, true)
            .addField('Slot 9', inventory.slot9, true)
            .addField('Slot 10', inventory.slot10, true)
            .addField('Slot 11', inventory.slot11, true)
            .addField('Slot 12', inventory.slot12, true)
            .addField('Slot 13', inventory.slot13, true)
            .addField('Slot 14', inventory.slot14, true)
            .addField('Slot 15', inventory.slot15, true)
            .addField('Slot 16', inventory.slot16, true)
            .addField('Slot 17', inventory.slot17, true)
            .setTimestamp()
            .setFooter(`• Requested By: ${message.author.tag}`, message.author.avatarURL)    
            const inventoryshow2 = new Discord.RichEmbed()
            .addField('Slot 18', inventory.slot18, true)
            .addField('Slot 19', inventory.slot19, true)
            .addField('Slot 20', inventory.slot20, true)
            .addField('Slot 21', inventory.slot21, true)
            .addField('Slot 22', inventory.slot22, true)
            .addField('Slot 23', inventory.slot23, true)
            .addField('Slot 24', inventory.slot24, true)
            .addField('Slot 25', inventory.slot25, true)
            .addField('Slot 26', inventory.slot26, true)
            .addField('Slot 27', inventory.slot27, true)
            .addField('Slot 28', inventory.slot28, true)
            .addField('Slot 29', inventory.slot29, true)
            .addField('Slot 30', inventory.slot30, true)
            .addField('Slot 21', inventory.slot31, true)
            .addField('Slot 32', inventory.slot32, true)
            .addField('Head', inventory.head, true)
            .addField('Chest', inventory.chest, true)
            .addField('Torso', inventory.torso, true)
            .addField('Shoe', inventory.shoe, true)
            .setTimestamp()
            .setFooter(`• Requested By: ${message.author.tag}`, message.author.avatarURL)
            message.author.send(inventoryshow1)
            message.author.send(inventoryshow2)

        }
        //cluster.close();
     });
    });
}
