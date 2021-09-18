"""
If you are not using this inside a cog, add the event decorator e.g:
@client.event
async def on_command_error(ctx, error)
For examples of cogs see:
https://gist.github.com/EvieePy/d78c061a4798ae81be9825468fe146be
For a list of exceptions:
https://discordpy.readthedocs.io/en/latest/ext/commands/api.html#exceptions
"""
import discord
import traceback
import sys
from discord.ext import commands


class CommandErrorHandler(commands.Cog):

    def __init__(self, client):
        self.client = client

    @commands.Cog.listener()
    async def on_command_error(self, ctx, error):
        if isinstance(error, commands.CommandOnCooldown):
            embed = discord.Embed(
                title=f"> **Slowmode error**",
                description=
                f"> try again in: `{error.retry_after:.2f}s.`",
                color=discord.Colour.red(),
                timestamp=ctx.message.created_at)
            embed.set_footer(text=f'',
                            icon_url=ctx.author.avatar_url)
            await ctx.send(f'{ctx.author.mention}', embed=embed) 

        elif isinstance(error, commands.MissingRequiredArgument):
            embed = discord.Embed(title='> **Error**',
                                description='> Du hast nicht genügend Angaben für den Command gegeben, z.B. @member', color=discord.Colour.green())
            await ctx.send(f'{ctx.author.mention}', embed=embed) 
        elif isinstance(error, commands.MissingPermissions):
            embed = discord.Embed(title='> **Error**', description='> Du hast leider nicht genügend Rechte.', color=discord.Colour.green())
            await ctx.send(f'{ctx.author.mention}', embed=embed) 
        elif isinstance(error, commands.BadArgument):
            embed = discord.Embed(title='> **Error**', description='> Du has ein falsches Argument angegeben!\r\n`Bitte gebe den richtigen Argument ein, z. B. @member.`', color=discord.Colour.green())
            await ctx.send(f'{ctx.author.mention}', embed=embed) 
        elif isinstance(error, commands.CommandNotFound):
            embed = discord.Embed(title='> **Error**', description='> It seems like you spelled this command wrong or he doesnt exists.', color=discord.Colour.green())
            await ctx.send(f'{ctx.author.mention}', embed=embed) 
        elif isinstance(error, commands.MemberNotFound):
            embed = discord.Embed(title='> **Error**', description='> Den angegebenen User wurde nicht gefunden.', color=discord.Colour.green())
            await ctx.send(f'{ctx.author.mention}', embed=embed) 
        elif isinstance(error, commands.ChannelNotFound):
            embed = discord.Embed(title='> **Error**', description='> Den angegebenen Channel wurde nicht gefunden.', color=discord.Colour.green())
            await ctx.send(f'{ctx.author.mention}', embed=embed)        
        elif isinstance(error, commands.BotMissingPermissions):
            embed = discord.Embed(title='> **Error**', description='> Der Bot hat nicht genügend Rechte um den Command auszuführen!', color=discord.Colour.green())
            await ctx.send(f'{ctx.author.mention}', embed=embed)               
        else:
            await ctx.send(f"Fehler beim Command `{ctx.command}`:\n````{error}```")


def setup(client):
    client.add_cog(CommandErrorHandler(client))
