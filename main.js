//Server
const express = require('express')
const app = express()
const port = 3000

app.get('/', (req, res) => {
  res.send('leveling system being hosted for 24/7')
})

app.listen(port, () => {
  console.log(`Server is Online`)
})
// Code
//flask server if we host on repl.it 


//discord.js imports 
const Discord = require('discord.js')
const bot = new Discord.Client();
const Levels = require('discord-xp')
const math = require("math")
Levels.setURL("here data connection")
const canvacord = require("canvacord")
const Database = require("@replit/database")
const db = new Database()

bot.on("ready", bot => {
    console.log('Bot is Online!')
})

bot.on("message", async message => {
    if (!message.guild) return;
    if (message.author.bot) return;


    if(message.content.startsWith("af leveling on" )) {
    if (!message.member.hasPermission('MANAGE_CHANNELS')) return
    await db.set(`toggle_${message.guild.id}`, "on")
    message.channel.send("> Toggled Leveling On !")
   }

    if (message.content.startsWith(`af leveling off`)) {
    if (!message.member.hasPermission('MANAGE_CHANNELS')) return
    await db.delete(`toggle_${message.guild.id}`)
    message.channel.send(`Jam eater leveling is now offile in : ${message.guild}`)
    }

    const prefix = 'af ';

    const args = message.content.slice(prefix.length).trim().split(/ +/g);
    const command = args.shift().toLowerCase();

    
    const data = await db.get(`toggle_${message.guild.id}`)
    if (data != null || data == 'on'){
        
        const randomXp = Math.floor(math.random() * 9) + 1; //Random amont of XP until the number you want + 1
        const hasLeveledUp = await Levels.appendXp(message.author.id, message.guild.id, randomXp);
        if (hasLeveledUp) {
            const user = await Levels.fetch(message.author.id, message.guild.id);
            message.channel.send(`${message.author.mention} You leveled up to ${user.level}! Keep it going , good job !`);
        }
    }



    
    //Rank
    
    if(command === "rank") {
        const data = await db.get(`toggle_${message.guild.id}`)
        if (data != null || data == 'on'){
            const user = await Levels.fetch(message.author.id, message.guild.id);
            const userLvl = Levels.xpFor(parseInt(user.level) + 1);
            const avatar = message.author.displayAvatarURL({ dynamic: false, format: 'png' });
            const rank = new canvacord.Rank()
                .setAvatar(avatar)
                .setCurrentXP(parseInt(user.xp.toLocaleString()) + 1)
                .setRequiredXP(userLvl)
                .setStatus("offline")
                .setProgressBar("#3355FF", "COLOR")
                .setUsername(message.author.username)
                .setDiscriminator(message.author.discriminator)
                .setBackground("IMAGE" , "https://www.freecodecamp.org/news/content/images/2020/04/w-qjCHPZbeXCQ-unsplash.jpg")
                .setLevel(user.level);
            
            rank.build()
                .then(data => {
                    const attachment = new Discord.MessageAttachment(data, "RankCard.png");
                    message.channel.send(attachment);
                });
            
            message.channel.send(rank)
        }else{
            message.channel.send("Jam eater leveling is offile :( in this server")
        }
    }
    
    //Leaderboard
    if(command === "leaderboard" || command === "lb") {
        const rawLeaderboard = await Levels.fetchLeaderboard(message.guild.id, 5);
        if (rawLeaderboard.length < 1) return reply("Nobody's in leaderboard yet.");

        const leaderboard = await Levels.computeLeaderboard(bot, rawLeaderboard, true); // We process the leaderboard.

        const lb = leaderboard.map(e => `${e.position}. ${e.username}#${e.discriminator}\nLevel: ${e.level}\nXP: ${e.xp.toLocaleString()}`); // We map the outputs.


        message.channel.send(`${lb.join("\n\n")}`)
    }
})



bot.login('NzkzMTU1NDE3OTQ0NDg5OTk0.X-oJiw.me2KaoW_fWjPI60IEoBuAaLKg0M')
