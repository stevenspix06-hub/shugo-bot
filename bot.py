import discord
from discord.ext import tasks
import os
from datetime import datetime

# =============================================
#  CONFIGURATION — remplis ces deux valeurs
# =============================================
TOKEN      = os.getenv("DISCORD_TOKEN", "MTUxMTM4ODcxMzU1NTU5NTM4NA.GOEKNX.yVb2sPx3mfWTWMbYBd85NloQ-FvtSB78bl6q4s")
CHANNEL_ID = int(os.getenv("CHANNEL_ID", "1511384702731157577"))
# =============================================

intents = discord.Intents.default()
client  = discord.Client(intents=intents)

@tasks.loop(minutes=1)
async def check_time():
    now = datetime.utcnow()  # UTC — ajuste si ton serveur est en heure locale
    if now.minute == 55:
        channel = client.get_channel(CHANNEL_ID)
        if channel:
            await channel.send("@everyone c'est l'heure des shugo !")

@client.event
async def on_ready():
    print(f"Connecté en tant que {client.user}")
    check_time.start()

client.run(TOKEN)
