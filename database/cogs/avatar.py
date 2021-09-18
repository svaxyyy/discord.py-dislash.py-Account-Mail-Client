from dislash import *
from discord.ext import commands
import discord
import json
import colorama
import datetime
import asyncio
from colorama import Fore, Back, Style, init
init(autoreset=True)
import os
def load():
    with open("database/json/bot_config.json", "r") as file:
        return json.load(file)
data = load()





class avatar(commands.Cog):
    def __init__(self, client):
        self.client = client #IMPORTANT: use self.client instead of client
                             #InteractionClient is accessible via self.bot.slash

    @slash_command(
        description="Shows the avatar of the user",
        options=[
            Option("user", "Enter the user", OptionType.USER)
            # By default, Option is optional
            # Pass required=True to make it a required arg
        ]
    )
    async def avatar(self,inter, user = None):
        # If user is None, set it to inter.author
        user = user or inter.author
        # We are guaranteed to receive a discord.User object,
        # because we specified the option type as Type.USER

        emb = discord.Embed(
            title=f"{user}'s avatar",
            color=discord.Color.blue()
        )
        emb.set_image(url=user.avatar_url)
        await inter.reply(embed=emb)

def setup(client):
    client.add_cog(avatar(client))