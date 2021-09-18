import discord
import traceback
import sys
from discord.ext import commands


class slowmode(commands.Cog):

    def __init__(self, client):
        self.client = client


    @commands.command()
    @commands.has_permissions(administrator=True)
    @commands.cooldown(1, 5, commands.BucketType.user)
    async def slowmode(ctx, seconds: int):
        await ctx.channel.edit(slowmode_delay=seconds)
        await ctx.send(f"{ctx.channel.mention} slowmode got changed to: {seconds}")


    @slowmode.error
    async def slowmode_error(ctx, error):
        if isinstance(error, commands.CommandOnCooldown):
            embed = discord.Embed(
                title=f"Slowmode",
                description=
                f">try again in `{error.retry_after:.2f}s.` ",
                color=discord.Colour.red(),
                timestamp=ctx.message.created_at)
            embed.set_footer(text=f'',
                            icon_url=ctx.author.avatar_url)
            await ctx.send(embed=embed)

        if isinstance(error, commands.MissingRequiredArgument):
            embed = discord.Embed(title='Missing a required argument',
                                description='')
            await ctx.send(embed=embed)
        if isinstance(error, commands.MissingPermissions):
            embed = discord.Embed(title='Error',
                                description='Missing permissions')

            await ctx.send(embed=embed)


def setup(client):
    client.add_cog(slowmode(client))
