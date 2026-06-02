import discord
from discord.ext import tasks
import os
import json
from datetime import datetime

TOKEN = os.getenv("DISCORD_TOKEN")

intents = discord.Intents.default()
intents.message_content = True
client = discord.Client(intents=intents)

# Fichier pour sauvegarder les channels enregistrés
SAVE_FILE = "channels.json"

def load_channels():
    if os.path.exists(SAVE_FILE):
        with open(SAVE_FILE, "r") as f:
            return json.load(f)
    return []

def save_channels(channels):
    with open(SAVE_FILE, "w") as f:
        json.dump(channels, f)

channel_ids = load_channels()

@tasks.loop(minutes=1)
async def check_time():
    now = datetime.utcnow()
    if now.minute == 55:
        for channel_id in channel_ids:
            channel = client.get_channel(channel_id)
            if channel:
                file = discord.File("shugo.jpg")
                await channel.send("@everyone C'est l'heure des Shugo, prépare-toi !!", file=file)

@client.event
async def on_message(message):
    if message.author.bot:
        return

    # Commande !shugo pour enregistrer le channel
    if message.content.lower() == "!shugo":
        if message.channel.id not in channel_ids:
            channel_ids.append(message.channel.id)
            save_channels(channel_ids)
            await message.channel.send("✅ Ce channel recevra désormais les notifications Shugo toutes les heures à :55 !")
        else:
            await message.channel.send("Ce channel est déjà enregistré !")

    # Commande !stopshugo pour se désinscrire
    if message.content.lower() == "!stopshugo":
        if message.channel.id in channel_ids:
            channel_ids.remove(message.channel.id)
            save_channels(channel_ids)
            await message.channel.send("❌ Ce channel ne recevra plus les notifications Shugo.")
        else:
            await message.channel.send("Ce channel n'est pas enregistré.")

@client.event
async def on_ready():
    print(f"Connecté en tant que {client.user}")
    print(f"Channels actifs : {channel_ids}")
    check_time.start()

client.run(TOKEN)
