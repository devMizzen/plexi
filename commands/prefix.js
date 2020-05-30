const Discord = require("discord.js");
const fs = require("fs");

exports.run = (args, message, bot, cmds) => {
    if (!message.member.hasPermission("MANAGE_SERVER")) return message.reply("You do not have the required permission MANAGE_SERVER to use this command.");
    if (args[0]) {
        let prefixes = JSON.parse(fs.readFileSync("./prefixes.json", "utf8"));
        prefixes[message.guild.id] = {
            prefixes: args[0]
        };
        fs.writeFile("./prefixes.json", JSON.stringify(prefixes), (err) => {
            if (err) console.log(err)
        });

        let embed = new Discord.RichEmbed()
        .setColor("#FF9900")
        .setTitle("Prefix Set!")
        .setDescription(`New prefix ${args[0]}`);
        message.channel.send(embed);
        console.log(`Prefix changed to ${args[0]} in ${message.guild.name}`)
    } else return message.reply(`Usage: ${bot.config.prefix}prefix <new prefix here>`);
};
