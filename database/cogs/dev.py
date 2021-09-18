import discord
from discord.ext import commands
import random
import traceback
import os
import asyncio






class info(commands.Cog):

    def __init__(self, client):
        self.client = client


    @commands.command(aliases=['guilds'])
    @commands.cooldown(1, 5, commands.BucketType.user)
    async def servers(self, ctx):
        counter = 0
        msg = '```js\n'
        msg += '{!s:19s} | {!s:>5s} | {} | {}\n'.format('ID', 'Member', 'Name', 'Owner')
        for guild in self.client.guilds:
            msg += '{!s:19s} | {!s:>5s}| {} | {}\n'.format(guild.id, guild.member_count, guild.name, guild.owner)
            counter += 1
        msg += '```'
        await ctx.send(msg)
        await ctx.send(f'Ich bin auf {counter} Server / Servern')


    @commands.command(aliases=["gi"])
    @commands.cooldown(1, 5, commands.BucketType.user)
    async def invite(self, ctx):
        serverid = ctx.channel.id
        server = self.client.get_guild(int(serverid))
        invite = await random.choice(server.text_channels).create_invite(max_uses=0, unique=True)
        msg = f'Invite für **{server.name}** ({server.id})\n{invite.url}'
    
        await ctx.send(msg)

            





def setup(client):
    client.add_cog(info(client))