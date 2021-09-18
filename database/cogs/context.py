from discord.ext import commands
from dislash import InteractionClient, ContextMenuInteraction




class context(commands.Cog):
    def __init__(self, client):
        self.client = client

def setup(client):
    client.add_cog(context(client))