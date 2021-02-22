from quart import Quart, render_template, request, session, redirect, url_for,jsonify
from quart_discord import DiscordOAuth2Session
from discord.ext import ipc
import html
import json


app = Quart(__name__)
ipc_client = ipc.Client(secret_key = "JamEater")

app.config["SECRET_KEY"] = "test123"
app.config["DISCORD_CLIENT_ID"] = 813008914207080449
app.config["DISCORD_CLIENT_SECRET"] = "zn-ifplp8Z8XVatyFN5DGmRsiOMmdnsJ"
app.config["DISCORD_REDIRECT_URI"] = "https://127.0.0.1:5000/callback"

discord = DiscordOAuth2Session(app)

@app.route("/")
async def home():
	return await render_template("index.html")

@app.route("/login")
async def login():
	return await discord.create_session()

@app.route("/invite/<guildid>")
async def invite(guildid):
	return await discord.create_session(scope=["bot"], permissions=8, guild_id=guildid, disable_guild_select=True)

@app.route("/callback")
async def callback():
	try:
		await discord.callback()
	except:
		return redirect(url_for("login"))

	user = await discord.fetch_user()
	return redirect(url_for("servers"))

@app.route("/dashboard/<serverid>")
async def dashboard(serverid):
	nickname = await ipc_client.request("getnickname", guildid=int(serverid))
	prefix = await ipc_client.request("getprefix", guildid=int(serverid))
	return await render_template("dashboard.html", something=nickname, prefix=prefix,limit=limit,channels=json.dumps(channels), welchannels=json.dumps(welchannels), leachannels=json.dumps(leachannels))

@app.route("/servers")
async def servers():
	guild_count = await ipc_client.request("get_guild_count")
	guild_ids = await ipc_client.request("get_guild_ids")

	try:
		user_guilds = await discord.fetch_guilds()
		user = await discord.fetch_user()
	except:
		return redirect(url_for("login"))


	return await render_template("serverselect.html", user = f"{user.name}#{user.discriminator}", guilds =[guild for guild in user_guilds if ((guild.permissions.value & 0x00000020) == 0x00000020) or ((guild.permissions.value & 0x00000008) == 0x00000008)])

@app.route("/switchto/<serverid>")
async def switchto(serverid):
	res = await ipc_client.request("checkforguild",guildid=int(serverid))
	if res == None:
		return redirect(f"/invite/{serverid}")
	return redirect(f"/dashboard/{serverid}")

@app.route("/change/<method>/<serverid>", methods=["POST"])
async def nick(method,serverid):
	if method == "nicknameSave":
		data = await request.form
		print(data["data"])
		await ipc_client.request("changenick", guildid=int(serverid), name=data["data"])
		return redirect(f"/dashboard/{serverid}")
	if method == "prefixSave":
		data = await request.form
		await ipc_client.request("changeprefix", guildid=int(serverid), newprefix=data["data"])
		return redirect(f"/dashboard/{serverid}")

if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0")

