const Discord = require("discord.js");
const fs = require("fs");
const Enmap = require("enmap");
const bot = new Discord.Client();
const config = bot.config = require("./config.json");

const express = require('express')
const path = require('path')
const PORT = process.env.PORT || 5000

const MongoClient = require('mongodb').MongoClient;
const uri = process.env.MONGOLAB_URL;
const cluster = new MongoClient(uri, { useNewUrlParser: true });


express()
  .use(express.static(path.join(__dirname, 'public')))
  .set('views', path.join(__dirname, 'views'))
  .set('view engine', 'ejs')
  .get('/', (req, res) => res.render('pages/index'))
  .listen(PORT, () => console.log(`Listening on ${ PORT }`))
bot.commands = new Enmap();
bot.functions = new Enmap();
bot.events = new Enmap();

fs.readdir("./events/", (err, files) => {
  if (err) return console.error(err);
  files.forEach(file => {
    const event = require(`./events/${file}`);
    let eventName = file.split(".")[0];
    bot.on(eventName, event.bind(null, bot));
    console.log(`Event ${eventName} Established!`);
  });
});

fs.readdir("./commands/", (err, files) => {
  if (err) return console.error(err);
  files.forEach(file => {
    if (!file.endsWith(".js")) return;
    if (file.startsWith('-')) return;
    let props = require(`./commands/${file}`);
    let commandName = file.split(".")[0];
    bot.commands.set(commandName, props);
    console.log(`Command ${commandName} Initialized!`);
  });
});

fs.readdir("./functions/", (err, files) => {
  if (err) return console.error(err);
  files.forEach(file => {
    if (!file.endsWith(".js")) return;
    if (file.startsWith('-')) return;
    let props = require(`./functions/${file}`);
    let functionName = file.split(".")[0];
    bot.functions.set(functionName, props);
    console.log(`Function ${functionName} Initialized!`);
  });
});

fs.readdir("./events/", (err, files) => {
  if (err) return console.error(err);
  files.forEach(file => {
    if (!file.endsWith(".js")) return;
    if (file.startsWith('-')) return;
    let props = require(`./events/${file}`);
    let eventName = file.split(".")[0];
    bot.events.set(eventName, props);
    console.log(`Event ${eventName} Initialized!`);
  });
});

bot.login(process.env.token);