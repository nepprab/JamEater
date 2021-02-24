# JamEater
[![License Badge](https://img.shields.io/badge/license-MIT-blue.svg)](LICENSE)
[![Maintenance](https://img.shields.io/badge/Maintained%3F-yes-green.svg)](CHANGELOG)

A discord bot coded in `Python` for reducing the total number of bots needed to add in a discord server.  
The bot's default command prefix is `jm `.  
discord.py version : `1.6.0`

## Downloading

```
git clone https://github.com/ProGamer368/JamEater
cd JamEater/
chmod +x main.py
```

## Requirements

```
cd JamEater/
sudo pip3 install -r requirements.txt
```
OR
```
cd JamEater/
sudo python3 -m pip install -r requirements.txt
```  

You would also need to edit a few files to run: 

- `bot-config/credentials.json` - Contains the bot's token, and owner ids.
- `bot-config/bot-emojis.json` - Contains all the emojis the bot uses.

## Running the bot

```
cd JamEater/
python3 main.py
```


## Supported Commands

### Fun Commands

|        Commmand         |                                 Description                                                       |
|:-----------------------:|:--------------------------------------------------------------------------------------------------:
| `8ball`                 | Gives a yes, no or a maybe to a question asked, completely random but fun                         |
| `meme`                  | Send your the SPICIEST memes from r/memes                                                         |
| `akinator`              | Starts an akinator game, it basically asks questions of your character than it'll try to guess it |
| `asciify`               | ASCIIfies your message.                                                                           |
| `apod`                  | Gets you an Astronomy Picture of the Day.                                                         |
| `joke`                  | Similar to the meme command, no pictures                                                          |



### Moderation Commands

|        Commands             |                                         Description                                                |
|:---------------------------:|:--------------------------------------------------------------------------------------------------:|
| `kick`                      | Kicks the mentioned user!                                                                          |
| `ban | hardban`             | Bans the mentioned userd!                                                                          |
| `unban`                     | Unbans the user from the guild.                                                                    |
| `mute`                      | Mutes the mentioned user.                                                                          |
| `unmute`                    | Unmutes the mentioned user, if muted.                                                              |
| `clear, remove, purge`      | Clears messages from the channel where the command has been used.                                  |
| `addrole`                   | adds the role to the user, if present in the guild (**CASE SENSITIVE**)                            |
| `removerole, purgerole`     | Removes the role from the user, if present in the guild and if the user has it (**CASE SENSITIVE**)|


### Utility commands

|            Commands               |                                          Description                                           |
|:---------------------------------:|:----------------------------------------------------------------------------------------------:|
| `avatar`,  `av`                   | Shows the avatar of the user mentioned.                                                        |
| `userinfo`                        | Gives the info of the user entered.                                                            |
| `serverinfo`                      | Gives the info of the server.                                                                  |
| `servercount`                     | Shows you how many servers the bot is in and total number of members in those servers combined.|
| `wikipedia`, `wiki`               | Gets you information from the wiki.                                                            |
| `afk` or `away_from_keyboard`     | Helps other people know you're afk when they mention you.                                      |



### Support commands

|       Commands        |                          Description                                  |
|:---------------------:|:---------------------------------------------------------------------:|
| `bug, bugs`           | Report any bugs found in the bot.                                     |
| `invite`              | Sends the invite link for the bot.                                    |
| `source, sourcecode`  | Sends you a link the redirects you to this github page.               |
| `supportserver, ss`   | Gets the link to the support server so you can ask doubts there.      |


