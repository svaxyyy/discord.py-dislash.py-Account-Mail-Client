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


from .response import response
from .accountManager import account, economy, mail
from .exceptions import AccountNotFound




class accounts(commands.Cog):
    def __init__(self, client):
        self.client = client #IMPORTANT: use self.client instead of client

                             #InteractionClient is accessible via self.bot.slash



    def is_admin():
        with open("database/json/accounts.json") as file:
            accdata = json.load(file)
        def predicate(inter):
            try:
                accdata["all-admin-ids"]
            except:
                accdata["all-admin-ids"] = []
                accdata["all-admin-ids"].append(445666466440675328)
                with open("database/json/accounts.json") as file:
                    json.dump(accdata,file,indent=4)
            admins = accdata["all-admin-ids"]
            return inter.author.id in admins
        return check(predicate)

    @slash_command(
        description="Shows your the current account !",
        options = []      


    )

    async def account(self, inter):
        user = inter.author
        try:
            dict = account.getInfo(self,user=user)
        except AccountNotFound:
            return await inter.reply(f"Cannot find you in my databank",ephemeral=True)
        username=dict["username"]
        last_username = dict["last_username"]
        password = dict["password"]
        emb = Embed(title="Account", description= f"> username: `{username}`\n> last username: `{last_username}`\n> password: ||`{password}`||")
        await inter.reply(embed=emb, ephemeral=True)

    @slash_command(
        description="Register you!",
        options = []      


    )

    async def register(self, inter):
        with open("database/json/accounts.json") as file:
            accdata = json.load(file)

        user = inter.author 

        await account.register(self,inter=inter,user=user)
        
    

    @slash_command(
        name = "set_username",
        description="Change you username.",
        options = [
            Option(name="username", description="Enter the username i should change it to.", required=True)
        ]  
    )

    async def set_username(self,inter, username=None):
        with open("database/json/accounts.json") as file:
            accdata = json.load(file)

        if username in accdata["all-usernames"]:
            return await inter.send(f"This username is already taken: {username}, please try again!")
        user = inter.author 
        await account.changeUsername(self, inter=inter, user=user, new_name=username)

    @slash_command(
        name = "mail",
        description="Sends a mail to a user.",
        options = [
            Option(name="to", description="Enter the username i should change it to.", type=OptionType.USER, required=True),
            Option(name="subject", description="Enter what you want the subject of the mail.", required=True),
            Option(name="content", description="Enter your mail content.", required=True)
        ]  
    )

    async def mail(self,inter, to=None, subject=None, content=None):
        user = inter.author 
        await mail.send(self,inter=inter, from_user=user,to_user=to,subject_content=subject,content=content)

    @slash_command(
        name = "inbox",
        description="Shows your mail inbox.",
        options = []  
    )

    async def inbox(self,inter):
        user = inter.author 
        await mail.inbox(self, inter=inter)

    @slash_command(
        name = "logout",
        description="Logout your account",
        options = []  
    )

    async def logout(self,inter):
        await account.logout(self, inter=inter)

    @slash_command(
        name = "login",
        description="Login to your account.",
        options = []  
    )

    async def login(self,inter):
        await account.login(self, inter=inter)

    @slash_command(
        name = "delete_all",
        description="Deletes all your mails.",
        options = []  
    )

    async def delete_all(self,inter):
        await mail.delete_all_mails(self, inter=inter)

    @slash_command(
        name = "delete",
        description=f"Deletes a mail from your inbox",
        options = [
            Option(name="mail_id", description="Enter the id of the mail i should delete", required=True)
        ]  
    )

    async def delete(self,inter, mail_id=None):
        await mail.delete(self, inter=inter,id = mail_id)

    @slash_command(
        name = "open",
        description=f"Deletes a mail from your inbox",
        options = [
            Option(name="mail_id", description="Enter the id of the mail i should delete", required=True)
        ]  
    )

    async def open(self,inter, mail_id=None):
        await mail.open(self, inter=inter,mail_id = mail_id)

    @is_admin()
    @slash_command(
        name = "mail_everyone",
        description="Sends a mail to a user.",
        options = [
            Option(name="subject", description="Enter what you want the subject of the mail.", required=True),
            Option(name="content", description="Enter your mail content.", required=True)
        ]  
    )

    async def mail_everyone(self,inter, subject=None, content=None):
        with open("database/json/accounts.json") as file:
            accdata = json.load(file)
        user = inter.author 
        ids = accdata["all-owner-ids"]
        try:
            for id in ids:
                guild = self.client.get_guild(inter.guild.id)
                member = guild.get_member(id)
                await mail.send_raw(self,inter=inter, from_user=user,to_user=member,subject_content=subject,content=content)
            
            await response.reply(self, inter=inter,content=f"Sent your mail to every user!", ephemeral=True)
                
        except Exception as e:
            return response.reply(self, inter=inter, content=f"Something went wrong!\nerror: ```fix\n{e}```", ephemeral=True)

    @is_admin()
    @slash_command(
        name = "admin",
        description="Add or removes a user from the admin list.",
        options = [
            Option(name="user", description="Enter the user i should add or remove from the admin list.",type=OptionType.USER, required=True)
        ]  
    )

    async def admin(self,inter, user=None):
        with open("database/json/accounts.json", "r") as file:
            accdata = json.load(file)
        ids = accdata["all-owner-ids"]


        try:
            for id in ids:
                if id == user.id:
                    index = accdata["all-owner-ids"].index(id)
                    del accdata["all-owner-ids"][index]
                    with open("database/json/accounts.json", "w") as f:
                        json.dump(accdata,f, indent=4)
                    return await response.reply(self, inter=inter,content=f"Removed {user.mention} from the admin list!")

            if not user.id in ids:
                accdata["all-owner-ids"].append(user.id)
                with open("database/json/accounts.json", "w") as f:
                    json.dump(accdata,f, indent=4)
                return await response.reply(self, inter=inter,content=f"Added {user.mention} to the admin list!")


        except Exception as e:
            return await response.reply(self, inter=inter, content=f"I wasnt able to remove/add a admin!\nerror: ```fix\n{e}```")


        with open("database/json/accounts.json", "w") as f:
                json.dump(accdata,f, indent=4)


    @slash_command(
        name = "inv",
        description="Shows what you have in you inventory.",
        options = []  
    )

    async def inventory(self,inter):
            await economy.inventory(self, inter=inter, user=inter.author)

    @is_admin()
    @slash_command(
        name = "create",
        description="Creates a economy item.",
        options = [
            Option(name="item_name", description="Enter the item name.", required=True),
            Option(name="item_price", description="Enter the item price.", required=True)
        ]  
    )

    async def create(self,inter,item_name=None,item_price=None):
            await economy.create(self, inter=inter,item_name=item_name,item_price=item_price)


    @slash_command(
        name = "info",
        description="Shows the info of the economy item.",
        options = [
            Option(name="item_id", description="Enter the item id.", required=True)
        ]  
    )

    async def info(self,inter,item_id=None):
            await economy.info(self, inter=inter, item_id=item_id)

    @is_admin()
    @slash_command(
        name = "add_item",
        description="Shows the info of the economy item.",
        options = [
            Option(name="user", description="Pick the user.", type=OptionType.USER, required=True),
            Option(name="item_id", description="Enter the item id.", required=True)
        ]  
    )
    

    async def add_item(self,inter,user=None,item_id=None):
        if account.logged_in(self,inter.author):
            with open("database/json/accounts.json") as file:
                accdata = json.load(file)
            items = accdata["all-economy-items"]
            for i in items:
                if (int(i[2]) == int(item_id)):
                    await economy.add_item(self,inter,user=user,item_id=item_id)
                    return 
                


                

            await inter.reply(f"I dont have the following item ID in my database: {item_id}")


def setup(client):
    client.add_cog(accounts(client))