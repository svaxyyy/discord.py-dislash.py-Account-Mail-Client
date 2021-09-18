from dislash import InteractionClient
from discord.ext import commands
import discord
import json
import colorama
import datetime
import asyncio
from colorama import Fore, Back, Style, init
init(autoreset=True)
import os
from dislash import *
from discord.ext import commands
import discord
import json
import colorama
import datetime
import asyncio
from discord.embeds import Embed
from colorama import Fore, Back, Style, init
from captcha.image import ImageCaptcha
from io import *
from datetime import *
init(autoreset=True)
import os
from random import randrange, random

intents = discord.Intents.default()
intents.members = True
Farben = [0x2f3136]
async def save(path,ob):
    """await save("database/json/bot_config.json", setupdata)"""
    with open(path, "w") as f:
        json.dump(ob,f, indent = 4)
def load():
    with open("database/json/bot_config.json", "r") as file:
        return json.load(file)
data = load()
client = commands.Bot(command_prefix=data["prefix"], intents=intents)
client.remove_command("help")

dislash = InteractionClient(client, test_guilds=[768231984685907975, 821329885703831573])

# app code



@client.event
async def on_ready():


    print(' ')
    print(Fore.LIGHTYELLOW_EX + "[bot] " + Fore.RESET + f"Ready as " + Fore.GREEN + f'{client.user.name}' + Fore.RESET)
    print(' ')


def colorInvisible():
    return 0x2f3136



nlist = ["response.py", "accountManager.py", "Exceptions.py"]


for filename in os.listdir('./database/cogs'):
    if filename.endswith('.py'):
        if filename in nlist:
            print("Ignored file import: " + filename)
        else:
            print(Fore.LIGHTYELLOW_EX + "[import] " + Fore.RESET + f"loaded " + Fore.CYAN + f'{filename[:-3]}' + Fore.RESET)
            client.load_extension(f'database.cogs.{filename[:-3]}')



@dislash.message_command(name="Guild ID")
async def guildid(inter: ContextMenuInteraction):
    # User commands always have only this ^ argument
    await inter.respond(
        f"Guild ID: `{inter.message.guild.id}`" # Make the message visible only to the author
    )

@dislash.message_command(name="Message ID")
async def msgid(inter: ContextMenuInteraction):
    await inter.respond(f"Message ID: `{inter.message.id}`")


client.run(data["token"])
