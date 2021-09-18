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
def load():
    with open("database/json/bot_config.json", "r") as file:
        return json.load(file)
data = load()

def colorInvisible():
    return 0x2f3136

color = colorInvisible()



from .response import *



class captcha(commands.Cog):
    def __init__(self, client):
        self.client = client #IMPORTANT: use self.client instead of client
                             #InteractionClient is accessible via self.bot.slash

    @slash_command(
        description="Setup your Captcha system!",
        options = [
            Option("role", "Select the Role i should add if he is a human.", OptionType.ROLE, required=True)
        ]      


    )

    async def setup_captcha(self, inter, role = None):
        with open("database/json/captcha-configs.json", "r") as f:
            setupdata = json.load(f)

        embed = discord.Embed(title="Captcha System Setup", description=f"Sucessfully finished the Setup!\n\n> role: {role.mention}", color=color)
        embed.set_footer(text=inter.guild.name, icon_url=f"{inter.guild.icon_url}")
        msg1 = await inter.reply(embed=embed)
        await msg1.add_reaction("✅")
        setupdata[str(inter.guild.id)] = {}
        setupdata[str(inter.guild.id)]["verified-role-id"] = int(role.id)
        with open("database/json/captcha-configs.json", "w") as f:
            json.dump(setupdata,f)

    




    @slash_command(
        name = "captcha",
        description = "Verifies you as a human",
        options = []
    )
    async def captcha(self, inter):
        with open("database/json/captcha-configs.json", "r") as f:
            setupdata = json.load(f)
        
        await response.reply(self, inter, content="Complete the Captcha in your DM`s!👀")
        
        guild = self.client.get_guild(inter.guild.id)
        member = guild.get_member(inter.author.id)
        role = guild.get_role(setupdata[str(guild.id)]["verified-role-id"])
        number = randrange(9999)
        num1=randrange(1,1999)
        num2=randrange(2000,3999)
        num3=randrange(4000, 5999)
        num4=randrange(6000,9999)
        print(number)
        image = ImageCaptcha(width = 280, height = 90)
        data = image.generate(f"{number}")
        image.write(f"{number}", 'database/captcha/captcha.png')
        file = discord.File('database/captcha/captcha.png')
        await inter.author.send(file=file)
        embed = Embed(title="Captcha🤖", description="Please select the Code which is on the Picture!")
        msg = await inter.author.send(embed=embed, components=[SelectMenu(placeholder="Select here!",max_values=1,options=[
            SelectOption(
                label=f"{num1}",
                value="1",
                description="Option 1",
                emoji="↗️"
            ),
            SelectOption(
                label=f"{num2}",
                value="2",
                description="Option 2",
                emoji="↗️"
            ),
            SelectOption(
                label=f"{num3}",
                value="3",
                description="Option 3",
                emoji="↗️"
            ),
            SelectOption(
                label=f"{num4}",
                value="4",
                description="Option 4",
                emoji="↗️"
            ),
            SelectOption(
                label=f"{number}",
                value="5",
                description="Option 5",
                emoji="↗️"
            )
            ])])

        def check(inter):
            return inter.author == inter.author

        inter1 = await msg.wait_for_dropdown(check)


        labels = [option.label for option in inter1.select_menu.selected_options]
        if labels[0] == f"{num1}":
            await response.respond(self, inter1, type=6)
            emb = Embed(title="Captcha🤖", description="`Captcha failed!` It seems like you have 1IQ or you are a bot!❌")
            msg1 = await inter1.author.send(embed=emb)
            await msg1.add_reaction("❌")
            await inter1.message.add_reaction("❌")
            await msg.edit(components=[])


        if labels[0] == f"{num2}":
            await response.respond(self, inter1, type=6)
            emb = Embed(title="Captcha🤖", description="`Captcha failed!` It seems like you have 1IQ or you are a bot!❌")
            msg1 = await inter1.author.send(embed=emb)
            await msg1.add_reaction("❌")
            await inter1.message.add_reaction("❌")
            await msg.edit(components=[])


        if labels[0] == f"{num3}":
            await response.respond(self, inter1, type=6)
            emb = Embed(title="Captcha🤖", description="`Captcha failed!` It seems like you have 1IQ or you are a bot!❌")
            msg1 = await inter1.author.send(embed=emb)
            await msg1.add_reaction("❌")
            await inter1.message.add_reaction("❌")
            await msg.edit(components=[])

        if labels[0] == f"{num4}":
            await response.respond(self, inter1, type=6)
            emb = Embed(title="Captcha🤖", description="`Captcha failed!` It seems like you have 1IQ or you are a bot!❌")
            msg1 = await inter1.author.send(embed=emb)
            await msg1.add_reaction("❌")
            await inter1.message.add_reaction("❌")
            await msg.edit(components=[])
            

        if labels[0] == f"{number}":
            await response.respond(self, inter1, type=6)
            try:
                await member.add_roles(role)
            except commands.MissingPermissions as err:
                return await inter.reply(f"Missing Permissions to add the role `{role.name}`\n\n> Error: {err}")
            else:
                emb = Embed(title="Captcha🤖", description=f"`Captcha Sucessfully!` You are now sucessfully verified as a human!✅\n\n> Added `{role.name}` to your roles in `{inter.guild.name}`.")
                msg1 = await inter1.author.send(embed=emb)
                await msg1.add_reaction("✅")
                await msg.edit(components=[])
                await inter1.message.add_reaction("✅")


            
def setup(client):
    client.add_cog(captcha(client))