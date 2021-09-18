class response():
    def __init__(self,client):
        self.client = client
        self.reply = response.reply
        self.respond = response.respond

    
    async def reply(self, inter, *, content, only_user=False):
        try:
            await inter.reply(str(content), ephemeral=bool(only_user))
        except Exception as err:
            raise err

    async def respond(self, inter, *, type):
        try:
            await inter.create_response(type=int(type))
        except Exception as err:
            raise err