import discord
from discord.ext import tasks
import os
from datetime import datetime

# =============================================
#  CONFIGURATION
# =============================================
TOKEN      = os.getenv("DISCORD_TOKEN")
CHANNEL_ID = int(os.getenv("CHANNEL_ID", "1511384702731157577"))
# =============================================

intents = discord.Intents.default()
client  = discord.Client(intents=intents)

@tasks.loop(minutes=1)
async def check_time():
    now = datetime.utcnow()
    if now.minute == 55:
        channel = client.get_channel(CHANNEL_ID)
        if channel:
            file = discord.File("shugo.jpg")
            await channel.send("@everyone C'est l'heure des Shugo, prépare-toi !!", file=file)

@client.event
async def on_ready():
    print(f"Connecté en tant que {client.user}")
    check_time.start()

client.run(TOKEN)
