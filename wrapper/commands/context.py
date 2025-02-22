from wrapper.message import Message
from wrapper.client import DiscordClient

class Context:

    def __init__(self, message: Message, client: DiscordClient):
        
        self.message = message
        self.bot = client
    

    async def send(self, content):

        await self.message.send_message(content)

