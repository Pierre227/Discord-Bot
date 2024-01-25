import discord
from discord import app_commands
from discord.ext import commands, tasks
from api import *
import json

# records = {}
# records['Eclow#EUW'] = ('PLATINUM', 'IV', 49, 26, 26)
# records['dead leaf lover#EUW'] = ('GOLD', 'II', 75, 15, 22)
# records['NONOZ woof#EUW'] = ('DIAMOND', 'IV', 17, 6, 8)
# records['Carjack Chiraq#7487'] = ()

# with open('data.json', 'w') as json_file:
#     json.dump(records, json_file)

with open('bot_key.txt', 'r') as file:
    bot_key = file.read().strip()

with open('data.json', 'r') as json_file:
    records = json.load(json_file)

# print(records)

bot = commands.Bot(command_prefix='/', intents = discord.Intents.all())

@bot.event
async def on_ready():
    print("Bot is up and running!")
    try:
        synced = await bot.tree.sync()
        print(f"Synced {len(synced)} commands")
        tracking.start()
    except Exception as e:
        print(e)

@bot.tree.command(name="elo")
@app_commands.describe(username = "Type your IGN", tag = "Type your TAG (ex: EUW)")
async def link(interaction: discord.Interaction, username: str, tag: str):
    tier, rank, leaguePoints, wins, losses = get_rank(username, tag)
    if tier:
        await interaction.response.send_message(f"{interaction.user.mention} is: {tier, rank, leaguePoints, wins, losses}")
    else:
        await interaction.response.send_message(f"{interaction.user.mention} NOT FOUND Sadge")

@tasks.loop(hours=3)
async def tracking():
    print("Tracking !")
    await tracking_user('Eclow', 'EUW')
    await tracking_user('dead leaf lover', 'EUW')
    await tracking_user('NONOZ woof', 'EUW')
    await tracking_user('Carjack Chiraq', '7487')
    await tracking_user('blue dung zz', 'EUW')

async def tracking_user(username, tag):
    rank = get_rank(username, tag)
    if rank and rank!=records[username+'#'+tag]:
        target_channel = bot.get_channel(700315670751084586)
        await target_channel.send(f":rotating_light: {username} went from : {records[username+'#'+tag][0]} {records[username+'#'+tag][1]} {records[username+'#'+tag][2]} lp to {rank[0]} {rank[1]} {rank[2]} lp. He won {rank[3] - records[username+'#'+tag][3]} and lost {rank[4] - records[username+'#'+tag][4]} games :joy_cat:")
        records[username+'#'+tag] = rank

bot.run(bot_key)