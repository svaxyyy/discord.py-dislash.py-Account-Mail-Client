import json, discord, asyncio, dislash
from .response import *
from .Exceptions import AccountNotFound
from dislash import *
from logging import error
from inspect import currentframe, getframeinfo




class account():
    def __init__(self,client):
        self.client = client
        self.register = account.register
        self.login = account.login
        self.logout = account.logout
        self.current = account.current
        self.logged_in = account.logged_in

    def logged_in(self, user):
        with open("database/json/accounts.json") as file:
            accdata = json.load(file)
        try:
            if accdata[str(user.id)]['logged-in'] == True:
                return True
            elif accdata[str(user.id)]['logged-in'] == False:
                return False
        except:
            return False
    

    async def register(self, inter, user):
        if not account.logged_in(self,inter.author):
            with open("database/json/accounts.json") as file:
                accdata = json.load(file)
            try:
                accdata["all-usernames"]
            except KeyError:
                accdata["all-usernames"] = []
                with open("database/json/accounts.json", "w") as f:
                    json.dump(accdata,f, indent=4)

            try:
                accdata["all-owner-ids"]
            except KeyError:
                accdata["all-owner-ids"] = []
                with open("database/json/accounts.json", "w") as f:
                    json.dump(accdata,f, indent=4)

            if user.id in accdata["all-owner-ids"]:
                return await response.reply(self, inter, content="You already have an account!", only_user=True)

                

            if not user.id in accdata["all-owner-ids"]:
                accdata[str(user.id)] = {}
                with open("database/json/accounts.json", "w") as f:
                    json.dump(accdata,f, indent=4)

                await response.reply(self, inter, content="> The Account registration will be in you DM`s!", only_user=True)

                await inter.author.send("What should be your `USERNAME`?")
    
                while True:
                    def check(inter):
                        return inter.author == inter.author and inter.author != inter.author.bot and inter.author != self.client.user 
                    msg = await self.client.wait_for("message",check=check)

                    username = str(msg.content)
                    

                    if username in accdata["all-usernames"]:
                        await inter.author.send(f"This username is already taken: {username}, please try another one!")

                    elif username not in accdata["all-usernames"]:
                        username = str(msg.content)
                        break


                await inter.author.send("What should be your `PASSWORD`?")
                msg = await self.client.wait_for("message",check=check)
                password_before = str(msg.content)
                await inter.author.send("Please repeat your `PASSWORD`.")
                msg = await self.client.wait_for("message",check=check)
                password_after = str(msg.content)

                if password_before == password_after:
                    password = password_before
                    try:
                        accdata["all-usernames"].append(username)
                        accdata["all-owner-ids"].append(user.id)
                        accdata[str(user.id)]["username"] = username
                        accdata[str(user.id)]["password"] = password
                        accdata[str(user.id)]["logged-in"] = True
                        accdata[str(user.id)]["last-username"] = username
                        accdata[str(user.id)]["mail-count"] = 0
                        accdata[str(user.id)]["mail-id-count"] = 0
                        accdata[str(user.id)]["mail-inbox"] = []
                        accdata[str(user.id)]["mail-reset"] = 0
                        accdata[str(user.id)]["pet"] = "None"
                        accdata[str(user.id)]["economy"] = {}
                        accdata[str(user.id)]["economy"]["inventory"] = []
                        
                        await inter.author.send(f"Created your account! You can see your account details with `/account`")
                    except KeyError as err:
                        raise err
                elif password_before != password_after:
                    return await inter.author.send("These passwords are different please do you registration again!")
            with open("database/json/accounts.json", "w") as f:
                json.dump(accdata,f, indent=4)


        elif account.logged_in(self,inter.author):
            return await response.reply(self, inter=inter, content=f"You are already logged into your Account! You can only create one per discord account.", only_user=True)
        






    async def login(self, inter):
        with open("database/json/accounts.json") as file:
            accdata = json.load(file)

        if not account.logged_in(self,inter.author):
            logout_user = inter.author
            dict = account.getInfo(self, logout_user)
            password = dict['password']
            username = dict['username']
            await response.reply(self, inter=inter, content=f"Please fill out the data in you DM`s!", only_user=True)
            await inter.author.send(f"Please send me your Password! \n\nAccount username: `{username}`")
            def check(inter):
                return inter.author == inter.author and inter.author != inter.author.bot and inter.author != self.client.user 
            msg = await self.client.wait_for("message",check=check)
            if (str(msg.content) == str(password)):
                try:
                    accdata[str(logout_user.id)]["logged-in"] = True
                    await inter.author.send(f"You are now logged in to the user: `{username}`!")
                except Exception as e:
                    await inter.author.send(f"Failed to login! Please try again.\nerror: ```fix\n{e}```")
            with open("database/json/accounts.json", "w") as f:
                    json.dump(accdata,f, indent=4)

        elif account.logged_in(self,inter.author):
            return await response.reply(self, inter=inter, content=f"You are already logged into your Account!", only_user=True)


    async def logout(self, inter):
        with open("database/json/accounts.json") as file:
            accdata = json.load(file)
        
        if account.logged_in(self,inter.author):
            logout_user = inter.author
            await response.reply(self, inter=inter, content=f"Please fill out the data in you DM`s!", only_user=True)
            await inter.author.send("Please send me you password so i can log you out!")
            def check(inter):
                return inter.author == inter.author and inter.author != inter.author.bot and inter.author != self.client.user 
            msg = await self.client.wait_for("message",check=check)
            dict = account.getInfo(self, logout_user)
            password = dict['password']
            username = dict['username']
            if (str(msg.content) == password):
                try:
                    accdata[str(logout_user.id)]["logged-in"] = False
                    await inter.author.send(f"You are now logged out from the user: `{username}`!")
                except Exception as e:
                    await inter.author.send(f"Failed to log you out! Please try again.\nerror: ```fix\n{e}```")
            with open("database/json/accounts.json", "w") as f:
                    json.dump(accdata,f, indent=4)

        elif not account.logged_in(self,inter.author):
            return await response.reply(self, inter=inter, content=f"You are not logged in so you cant logout!", only_user=True)

    async def current(self, inter, *, type):
        pass



    async def changeUsername(self,inter=None, *,user, new_name):
        if account.logged_in(self,inter.author):
            with open("database/json/accounts.json") as file:
                accdata = json.load(file)
            try:
                accdata[str(user.id)]["last-username"] = accdata[str(user.id)]["username"]
                accdata[str(user.id)]["username"] = new_name
                last_username = accdata[str(user.id)]["last-username"]
                username = accdata[str(user.id)]["username"]
                embed = discord.Embed(title=f"Username", description= f"Sucessfully changed your username!\n\n> old name: {last_username}\n\n> new name: {username}")
                await inter.reply(embed=embed, ephemeral=True)
                with open("database/json/accounts.json", "w") as f:
                        json.dump(accdata,f, indent=4)
            except Exception as err:
                embed = discord.Embed(title=f"Username", description= f"It seems like i failed to change your username!\n\n> error: ```fix\n{err}```")
                return await inter.reply(embed=embed, ephemeral=True)

            
            with open("database/json/accounts.json", "w") as f:
                    json.dump(accdata,f, indent=4)
            pass
        
        elif not account.logged_in(self,inter.author):
            return await response.reply(self, inter=inter, content=f"You are not logged into a account! Please login or create one with `/register`", only_user=True)


    def getInfo(self, user):
        if account.logged_in(self,user):
            with open("database/json/accounts.json") as file:
                accdata = json.load(file)
            username = accdata[str(user.id)]["username"]
            password = accdata[str(user.id)]["password"]
            logged_in = accdata[str(user.id)]["logged-in"]
            last_username = accdata[str(user.id)]["last-username"]
            mail_inbox = accdata[str(user.id)]["mail-inbox"]
            mail_reset = accdata[str(user.id)]["mail-reset"]
            mail_count = accdata[str(user.id)]["mail-count"]
            mail_id_count = accdata[str(user.id)]["mail-id-count"]
            return {
                'username' : username,
                'password' : password,
                'logged_in' : logged_in,
                'last_username' : last_username,
                'mail-count' : mail_count,
                'mail-id-count' : mail_id_count,
                'mail-inbox' : mail_inbox,
                'mail-reset' : mail_reset
            }
        
        elif not account.logged_in(self,user):
            raise AccountNotFound







class mail():
    def __init__(self,client):
        self.client = client
        self.sendMail = mail.sendMail
        self.totalLetters = mail.totalLetters
        self.logged_in = mail.logged_in
        self.delete_all_mails = mail.delete_all_mails

    def logged_in(self, user):
        with open("database/json/accounts.json") as file:
            accdata = json.load(file)
        if accdata[str(user.id)]['logged-in'] == True:
            return True
        elif accdata[str(user.id)]['logged-in'] == False:
            return False

    def fetch_mail(self,user,mail_id):
        if account.logged_in(self,user):
            with open("database/json/accounts.json") as file:
                accdata = json.load(file)

            dict = account.getInfo(self,user=user)
            inbox = dict['mail-inbox']
            
            for mail in inbox:
                if mail[3] == mail_id:
                    return {
                        "sender-id" : mail[0],
                        "subject" : mail[1],
                        "content" : mail[2],
                        "id" : mail[3]
                    }

        elif not account.logged_in(self,user):
            raise "An Error occured in def fetch_mail()"

    def totalLetters(self, embed):
        fields = [embed.title, embed.description, embed.footer.text, embed.author.name]

        fields.extend([field.name for field in embed.fields])
        fields.extend([field.value for field in embed.fields])

        total = ""
        for item in fields:
            # If we str(discord.Embed.Empty) we get 'Embed.Empty', when
            # we just want an empty string...
            total += str(item) if str(item) != 'Embed.Empty' else ''
        return len(total)

    async def sendSystemMail(self, inter, from_user, to_user, subject_content,content):
        if account.logged_in(self,inter.author):
            with open("database/json/accounts.json") as file:
                accdata = json.load(file)
            
            if (int(to_user.id in accdata["all-owner-ids"])):
                with open("database/json/accounts.json") as file:
                    accdata = json.load(file)
                content = content

                if len(subject_content) > 51:
                    return await response.reply(self, inter=inter, content=f"Your subject content is to long there is a maximum of `50` letters!", only_user=True)
                if len(content) > 501:
                    return await response.reply(self, inter=inter, content=f"Your content is to long there is a maximum of `500` letters!", only_user=True)


                try:
                    accdata[str(to_user.id)]["mail-id-count"] += 1
                    cnt = accdata[str(to_user.id)]["mail-id-count"]
                    accdata[str(to_user.id)]["mail-inbox"].append([from_user.id, subject_content,content, accdata[str(to_user.id)]["mail-id-count"]])
                    await inter.reply(f"Sent your mail to `{to_user.name}#{to_user.discriminator}`", ephemeral=True)
                    
                    await to_user.send(f"`{to_user.name}#{to_user.discriminator}` has sent you a mail! Check `/inbox` or `/open` command.\n\n**Mail-id:** {cnt}")
                except Exception as e:
                    await inter.reply(f"Failed to send you mail to: `{to_user.name}#{to_user.discriminator}`\nerror: ```fix\n{e}```", ephemeral=True)
                    

                with open("database/json/accounts.json", "w") as f:
                        json.dump(accdata,f, indent=4)

            elif not (int(to_user.id in accdata["all-owner-ids"])):
                return await response.reply(self, inter=inter, content=f"It seems like this user has no account, go tell him to create one.", only_user=True)

        elif not account.logged_in(self,inter.author):
            return await response.reply(self, inter=inter, content=f"You are not logged into a account! Please login or create one with `/register`", only_user=True)
    
    async def inbox(self, inter):
        if account.logged_in(self,inter.author):
            with open("database/json/accounts.json") as file:
                accdata = json.load(file)
            inbox_of_user = inter.author
            dict = account.getInfo(self,inbox_of_user)

            inbox = dict["mail-inbox"]
            username = dict["username"]
            

            if inbox == None:
                return inter.reply(f"You Inbox is empty!")


            elif inbox != None:
                embed = discord.Embed(title=f"Inbox of {username} Page 1", description="Ill only show 25 mails. To see more mails delete some with `/delete` or /delete_all.")
                embed2 = discord.Embed(title=f"Inbox of {username} Page 2", description="I`ll only show 25 mails")
                embed3 = discord.Embed(title=f"Inbox of {username} Page 3", description="I`ll only show 25 mails")
                embed4 = discord.Embed(title=f"Inbox of {username} Page 4", description="I`ll only show 25 mails")
                embed_bool = True
                embed2_bool = False
                embed3_bool = False
                embed4_bool = False
                field_cnt = 0
                cnt = 0
                cnt1 = 0
                cnt2 = 0
                cnt3 = 0
                fields = 0
                for mail in inbox:
                    field_cnt += 1
                    if field_cnt < 25:
                        guild = self.client.get_guild(inter.guild.id)
                        sender = guild.get_member(mail[0])
                        embed.add_field(name=f"Sender: `{sender.name}#{sender.discriminator}`", value=f"**ID:** ||`{mail[3]}`||\n**Subject:** `{mail[1]}`\n**Content:** {mail[2]}",inline=True)
                    else:
                        break
                        
                if embed2_bool == True:
                    return await inter.reply(embeds=[embed, embed2], ephemeral=True)
                if embed3_bool == True:
                    return await inter.reply(embeds=[embed, embed2, embed3], ephemeral=True)
                if embed4_bool == True:
                    return await inter.reply(embeds=[embed, embed2, embed3, embed4], ephemeral=True)
                elif embed2_bool == False:
                    return await inter.reply(embed=embed, ephemeral=True)

                

        elif not account.logged_in(self,inter.author):
            return await response.reply(self, inter=inter, content=f"You are not logged into a account! Please login or create one with `/register`", only_user=True)


    async def send(self, inter, from_user, to_user, subject_content,content):
        if account.logged_in(self,inter.author):
            with open("database/json/accounts.json") as file:
                accdata = json.load(file)
            
            if (int(to_user.id in accdata["all-owner-ids"])):
                with open("database/json/accounts.json") as file:
                    accdata = json.load(file)
                content = content

                if len(subject_content) > 51:
                    return await response.reply(self, inter=inter, content=f"Your subject content is to long there is a maximum of `50` letters!", only_user=True)
                if len(content) > 1001:
                    return await response.reply(self, inter=inter, content=f"Your content is to long there is a maximum of `1000` letters!", only_user=True)


                try:
                    accdata[str(to_user.id)]["mail-id-count"] += 1
                    cnt = accdata[str(to_user.id)]["mail-id-count"]
                    accdata[str(to_user.id)]["mail-inbox"].append([from_user.id, subject_content,content, accdata[str(to_user.id)]["mail-id-count"]])
                    await inter.reply(f"Sent your mail to `{to_user.name}#{to_user.discriminator}`", ephemeral=True)
                    
                    await to_user.send(f"`{to_user.name}#{to_user.discriminator}` has sent you a mail! Check `/inbox` or `/open` command.\n\n**Mail-id:** {cnt}")
                except Exception as e:
                    await inter.reply(f"Failed to send you mail to: `{to_user.name}#{to_user.discriminator}`\nerror: ```fix\n{e}```", ephemeral=True)
                    

                with open("database/json/accounts.json", "w") as f:
                        json.dump(accdata,f, indent=4)

            elif not (int(to_user.id in accdata["all-owner-ids"])):
                return await response.reply(self, inter=inter, content=f"It seems like this user has no account, go tell him to create one.", only_user=True)

        elif not account.logged_in(self,inter.author):
            return await response.reply(self, inter=inter, content=f"You are not logged into a account! Please login or create one with `/register`", only_user=True)


    async def send_raw(self, inter, from_user, to_user, subject_content,content):
        if account.logged_in(self,inter.author):
            with open("database/json/accounts.json") as file:
                accdata = json.load(file)
            content = content

            if len(subject_content) > 51:
                return 
            if len(content) > 1001:
                return 


            
            accdata[str(to_user.id)]["mail-id-count"] += 1
            cnt = accdata[str(to_user.id)]["mail-id-count"]
            accdata[str(to_user.id)]["mail-inbox"].append([from_user.id, subject_content,content, accdata[str(to_user.id)]["mail-id-count"]])
            await to_user.send(f"`{to_user.name}#{to_user.discriminator}` has sent you a mail! Check `/inbox` or `/open` command.\n\n**Mail-id:** {cnt}")


                

            with open("database/json/accounts.json", "w") as f:
                    json.dump(accdata,f, indent=4)

        elif not account.logged_in(self,inter.author):
            return await response.reply(self, inter=inter, content=f"You are not logged into a account! Please login or create one with `/register`", only_user=True)

    async def delete(self, inter, id):
        if account.logged_in(self,inter.author):
            with open("database/json/accounts.json") as file:
                accdata = json.load(file)

            user = inter.author
            dict = account.getInfo(self, user)
            inbox = dict["mail-inbox"]
            

            for mail in inbox:
                if mail[3] == int(id):
                    try:
                        index = accdata[str(user.id)]["mail-inbox"].index(mail)
                        del accdata[str(user.id)]["mail-inbox"][index]
                        await response.reply(self, inter=inter, content=f"The requested mail has got deleted!\n **ID: ** `{mail[3]}`", only_user=True)
                    except Exception as e:
                        return await response.reply(self, inter=inter, content=f"Deleting mail failed! Please try again.\nerror: ```fix\n{e}```", only_user=True)

            with open("database/json/accounts.json", "w") as f:
                    json.dump(accdata,f, indent=4)

        elif not account.logged_in(self,inter.author):
            return await response.reply(self, inter=inter, content=f"You are not logged into a account! Please login or create one with `/register`", only_user=True)

    async def delete_all_mails(self, inter):
        if account.logged_in(self,inter.author):
            with open("database/json/accounts.json") as file:
                accdata = json.load(file)

            user = inter.author
            dict = account.getInfo(self, user)
            inbox = dict["mail-inbox"]
            

            for mail in inbox:
                try:
                    index = accdata[str(user.id)]["mail-inbox"].index(mail)
                    del accdata[str(user.id)]["mail-inbox"][index]
                except Exception as e:
                    return await response.reply(self, inter=inter, content=f"Deleting mail failed! Please try again.\nerror: ```fix\n{e}```", only_user=True)

            if not inbox:
                await response.reply(self, inter=inter, content=f"Deleted all you mail`s!", only_user=True)

            with open("database/json/accounts.json", "w") as f:
                    json.dump(accdata,f, indent=4)

        elif not account.logged_in(self,inter.author):
            return await response.reply(self, inter=inter, content=f"You are not logged into a account! Please login or create one with `/register`", only_user=True)

    async def open(self, inter, mail_id):
        if account.logged_in(self,inter.author):
            with open("database/json/accounts.json") as file:
                accdata = json.load(file)

            user = inter.author
            dict = account.getInfo(self, user)
            inbox = dict["mail-inbox"]
            username = dict["username"]
            for mail in inbox:
                if int(mail[3]) == int(mail_id):
                    try:
                        guild = self.client.get_guild(inter.guild.id)
                        sender = guild.get_member(mail[0])
                        dict1 = account.getInfo(self, sender)
                        sender_username = dict1['username']
                        embed = discord.Embed(title=f"Opened mail: `{mail_id}`", description=f"This mail was sent by:\nDiscord: `{sender.name}#{sender.discriminator}`\nUsername: `{sender_username}`")
                        embed.add_field(name=f"Mail:", value=f"**ID: ** ||`{mail_id}`|| \n\n***Subject:*** {mail[1]}\n\n***Content:*** {mail[2]}")
                        await inter.reply(embed=embed, ephemeral=True)
                    except Exception as e:
                        await inter.reply(f"Something went wrong!\nerror ```fix\n{e}```", ephemeral=True)


        elif not account.logged_in(self,inter.author):
            return await response.reply(self, inter=inter, content=f"You are not logged into a account! Please login or create one with `/register`", only_user=True)



    async def reseter(self,user):
        with open("database/json/accounts.json") as file:
            accdata = json.load(file)


class economy():
    def __init__(self,client):
        self.client = client
    
    def getUserData(self,user):
        with open("database/json/accounts.json") as file:
            accdata = json.load(file)  
        
        inventory = accdata[str(user.id)]["economy"]["inventory"]

        return {
            'inventory': inventory
        }

    def getItemData(self, item_id):
        """Returns a dict: 
        itemname,
        itemprice,
        itemid"""
        with open("database/json/accounts.json") as file:
            accdata = json.load(file)  
        
        items = accdata["all-economy-items"]

        for i in items:
            if (int(i[2]) == int(item_id)):
                itemprice = i[0]
                itemname = i[1]
                itemid = i[2]
                return {
                    'itemname': itemname,
                    'itemprice' : itemprice,
                    'itemid' : itemid
                }
            

    async def inventory(self,inter,user):
        if account.logged_in(self,inter.author):
            with open("database/json/accounts.json") as file:
                accdata = json.load(file)

            try:
                accdata[str(user.id)]["economy"] 
            except KeyError:
                accdata[str(user.id)]["economy"] = {}
            
            try:
                accdata[str(user.id)]["economy"]["inventory"]
            except KeyError:
                accdata[str(user.id)]["economy"]["inventory"] = []

            try:
                accdata["global-economy-id-count"]
            except KeyError:
                accdata["global-economy-id-count"] = []

            inv = accdata[str(user.id)]["economy"]["inventory"]

            embed = discord.Embed(title=f"Inventory of {user}")
            for item in inv:
                data = economy.getItemData(self, item_id=int(item["item-id"]))
                itemprice = str(data["itemprice"])
                itemid = str(data["itemid"])
                embed.add_field(name=str(data["itemname"]), value=f"price: `{itemprice}`\nitem id: `{itemid}`")
            
            await inter.reply(embed=embed)
            with open("database/json/accounts.json", "w") as f:
                json.dump(accdata,f, indent=4)

        elif not account.logged_in(self,inter.author):
            return await response.reply(self, inter=inter, content=f"You are not logged into a account! Please login or create one with `/register`", only_user=True)

    async def add_item(self,inter,user,item_id):
        if account.logged_in(self,inter.author):
            with open("database/json/accounts.json") as file:
                accdata = json.load(file)

            try:
                accdata[str(user.id)]["economy"] 
            except KeyError:
                accdata[str(user.id)]["economy"] = {}
            
            try:
                accdata[str(user.id)]["economy"]["inventory"]
            except KeyError:
                accdata[str(user.id)]["economy"]["inventory"] = []


            item = economy.getItemData(self, item_id=item_id)
            itemname = item['itemname']
            itemprice = item['itemprice']
            itemid = item['itemid']
            inv = accdata[str(user.id)]["economy"]["inventory"]

            try:
                embed = discord.Embed(title=f"Added an item!", description=f"**Item name:** `{itemname}`\n**Item price:** `{itemprice}`\n**Item ID:** `{itemid}`")
                for i in inv:
                    if i["amount"]:
                        i["amount"] + 1
                    elif not i["amount"]:
                        i["amount"] = 1



                inv.append({
                    'item-id' : int(item_id)
                })
                await inter.reply(embed=embed)
                with open("database/json/accounts.json", "w") as f:
                    json.dump(accdata,f, indent=4)
            except Exception as e:
                return await response.reply(self, inter=inter, content=f"Failed to add the item to the account!\nerror: ```fix\n{e}```", only_user=True)


        elif not account.logged_in(self,inter.author):
            return await response.reply(self, inter=inter, content=f"You are not logged into a account! Please login or create one with `/register`", only_user=True)



    async def info(self,inter,item_id):
        if account.logged_in(self,inter.author):
            with open("database/json/accounts.json") as file:
                accdata = json.load(file)

            try:
                accdata["global-economy-id-count"]
            except KeyError:
                accdata["global-economy-id-count"] = []

            try:
                accdata["all-economy-items"]
            except KeyError:
                accdata["all-economy-items"] = []



            try:

                dict = economy.getItemData(self, item_id=item_id)
                itemname = dict["itemname"]
                itemprice = dict["itemprice"]
                itemid = dict["itemid"]
                embed = discord.Embed(title=f"Info of: {item_id}",description = f"**Itemname:** `{itemname}`\n**Itemprice:** `{itemprice}`\n**Item ID:** `{itemid}`")
                await inter.reply(embed=embed)
                with open("database/json/accounts.json", "w") as f:
                    json.dump(accdata,f, indent=4)

            except Exception as e:
                frameinfo = getframeinfo(currentframe())
                return await response.reply(self, inter=inter, content=f"Something went wrong!\nline: `{frameinfo.lineno}`\n\nerror: ```fix\n{e}```", only_user=True)
        elif not account.logged_in(self,inter.author):
            return await response.reply(self, inter=inter, content=f"You are not logged into a account! Please login or create one with `/register`", only_user=True)
            

    async def create(self,inter,item_name, item_price):
        if account.logged_in(self,inter.author):
            with open("database/json/accounts.json") as file:
                accdata = json.load(file)

            try:
                accdata["global-economy-id-count"]
            except KeyError:
                accdata["global-economy-id-count"] = 0

            try:
                accdata["all-economy-items"]
            except KeyError:
                accdata["all-economy-items"] = []

            all_items = accdata["all-economy-items"]
            accdata["global-economy-id-count"] += 1
            global_count = accdata["global-economy-id-count"]


            try:
                all_items.append([item_name, item_price, global_count])
                emb = discord.Embed(name=f"Created Item:", description=f"**Itemname:** `{item_name}`\n**Itemprice:** `{item_price}`\nItem ID: `{global_count}`")
                await inter.reply(embed=emb)
                with open("database/json/accounts.json", "w") as f:
                    json.dump(accdata,f, indent=4)

            except Exception as e:
                with open("database/json/accounts.json", "w") as f:
                    json.dump(accdata,f, indent=4)
                return await response.reply(self, inter=inter, content=f"Failed to create this item, please try again!\nerror: ```fix\n{e}```", only_user=True)
        elif not account.logged_in(self,inter.author):
            return await response.reply(self, inter=inter, content=f"You are not logged into a account! Please login or create one with `/register`", only_user=True)



class group():
    def __init__(self,client):
        self.client = client

class pet():
    def __init__(self,client):
        self.client = client

    
    
    async def create(self, inter):

        if account.logged_in(self, inter.author):
            with open("database/json/accounts.json") as file:
                accdata = json.load(file)
            user = inter.author
            try:
                accdata["pets"]
            except KeyError:
                accdata["pets"] = []
                with open("database/json/accounts.json", "w") as f:
                        json.dump(accdata,f, indent=4)


            try:
                accdata["pet-owner-ids"]
            except KeyError:
                accdata["pet-owner-ids"] = []
                with open("database/json/accounts.json", "w") as f:
                        json.dump(accdata,f, indent=4)


            pets = accdata["pets"]
            await response.reply(self, inter=inter, content=f"Configurate you pet in your DM`s!", only_user=True)

            embed = discord.Embed(title=f"Pet",description=f"Please choose a pet from below.")
            

            for pet in pets:
                picture = pet["picture"]
                pet_name = pet["name"]
                embed.add_field(name=f"{pet_name}", value=f"Picture: \n{picture}")
            
            msg = await user.send(embed=embed, components=[SelectMenu(
                placeholder="Select your pet here",
                min_values=1,
                max_values=1,
                options=[
                    SelectOption(
                        label=f"giraffe",
                        value="1",
                        description="If you click this you select the giraffe as you pet.",
                        emoji="🦒"
                    )
                ]
            )])

            def check(inter):
                return inter.author == inter.author and inter.author != inter.author.bot and inter.author != self.client.user

            inter1 = await msg.wait_for_dropdown(check)


            labels = [option.label for option in inter1.select_menu.selected_options]
            if labels[0] == f"giraffe":
                await response.respond(self, inter=inter1, type=6)
                embed = discord.Embed(title=f"Your choice was: {labels[0]}", description=f"Good choice im now building a house and database.")
                embed.set_image(url=f"https://cdn.discordapp.com/attachments/768231984685907978/883433788028375080/Z.png")
                await msg.edit(components=[SelectMenu(
                placeholder="Select your pet here",
                min_values=1,
                max_values=1,
                disabled=True,
                options=[
                    SelectOption(
                        label=f"giraffe",
                        value="1",
                        description="If you click this you select the giraffe as you pet.",
                        emoji="🦒"
                    )
                ]
            )])
                await inter.author.send(embed=embed)
                try:
                    accdata[str(user.id)]["pet"]
                except KeyError:
                    accdata[str(user.id)]["pet"] = {}
                    with open("database/json/accounts.json", "w") as f:
                            json.dump(accdata,f, indent=4)

                accdata["pet-owner-ids"].append(user.id)
                accdata[str(user.id)]["pet"]["name"] = str(labels[0]) #change
                accdata[str(user.id)]["pet"]["picture"] = "https://cdn.discordapp.com/attachments/768231984685907978/883433788028375080/Z.png"
                with open("database/json/accounts.json", "w") as f:
                        json.dump(accdata,f, indent=4)


        with open("database/json/accounts.json", "w") as f:
                json.dump(accdata,f, indent=4)


    async def feed(self, inter, user):

        if account.logged_in(self, inter.author):
            with open("database/json/accounts.json") as file:
                accdata = json.load(file)
            
            if accdata[str(user.id)]["pet"]:
                pass
                