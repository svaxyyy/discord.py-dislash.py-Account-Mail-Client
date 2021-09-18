from colorama.ansi import clear_screen
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





class manager(commands.Cog):
    def __init__(self, client):
        self.client = client #IMPORTANT: use self.client instead of client
                             #InteractionClient is accessible via self.bot.slash

    @slash_command(
        description="Reloads a extension (cog)",
        options=[
            Option("filename", "Enter the filename", required=True)
            # By default, Option is optional
            # Pass required=True to make it a required arg
        ]
    )
    async def reload(self,inter, filename=None):
        try:
            filename[4]
        except IndexError:
            return await inter.reply(f"Filename haves to be longer than `3` spots!", ephemeral=True)
        else:
            try:
                self.client.reload_extension(f'database.cogs.{filename[:-3]}')
            except commands.ExtensionNotFound:
                return await inter.reply(f"Cannot find: `./database/cogs/{filename}`", ephemeral=True)
            except commands.ExtensionFailed as error:
                return await inter.reply(f"Extension failed: `./database/cogs/{filename}`\n\nerror: ```fix\n{error}```", ephemeral=True)
            except commands.ExtensionNotLoaded:
                return await inter.reply(f"Extension not Loaded: `./database/cogs/{filename}`", ephemeral=True)
            else:
                await inter.reply(f"Reloaded: `./database/cogs/{filename}`", ephemeral=True)



    @slash_command(
        description="Unloads a extension (cog)",
        options=[
            Option("filename", "Enter the filename", required=True)
            # By default, Option is optional
            # Pass required=True to make it a required arg
        ]
    )
    async def unload(self,inter, filename=None):
        try:
            filename[4]
        except IndexError:
            return await inter.reply(f"Filename haves to be longer than `3` spots!", ephemeral=True)
        else:
            try:
                self.client.unload_extension(f'database.cogs.{filename[:-3]}')
            except commands.ExtensionAlreadyLoaded:
                return await inter.reply(f"file already loaded: `./database/cogs/{filename}`", ephemeral=True)
            except commands.ExtensionNotFound:
                return await inter.reply(f"Cannot find: `./database/cogs/{filename}`", ephemeral=True)
            except commands.ExtensionFailed as error:
                return await inter.reply(f"Extension failed: `./database/cogs/{filename}`\n\nerror: ```fix\n{error}```", ephemeral=True)
            except commands.ExtensionNotLoaded:
                return await inter.reply(f"Extension not Loaded: `./database/cogs/{filename}`", ephemeral=True)
            else:
                await inter.reply(f"Unloaded: `./database/cogs/{filename}`", ephemeral=True)

    @slash_command(
        description="Loads a extension (cog)",
        options=[
            Option("filename", "Enter the filename", required=True)
            # By default, Option is optional
            # Pass required=True to make it a required arg
        ]
    )
    async def load(self,inter, filename=None):
        try:
            filename[4]
        except IndexError:
            return await inter.reply(f"Filename haves to be longer than `3` spots!", ephemeral=True)
        else:
            try:
                self.client.load_extension(f'database.cogs.{filename[:-3]}')
            except commands.ExtensionAlreadyLoaded:
                return await inter.reply(f"file already loaded: `./database/cogs/{filename}`", ephemeral=True)
            except commands.ExtensionNotFound:
                return await inter.reply(f"Cannot find: `./database/cogs/{filename}`", ephemeral=True)
            except commands.ExtensionFailed as error:
                return await inter.reply(f"Extension failed: `./database/cogs/{filename}`\n\nerror: ```fix\n{error}```", ephemeral=True)
            except commands.ExtensionNotLoaded:
                return await inter.reply(f"Extension not Loaded: `./database/cogs/{filename}`", ephemeral=True)
            else:
                await inter.reply(f"Loaded: `./database/cogs/{filename}`", ephemeral=True)

    @slash_command(
        description="Shows all extensions (cogs)",
        options=[]
    )

    async def cogs(self,inter, filename=None):
        pass

def setup(client):
    client.add_cog(manager(client))