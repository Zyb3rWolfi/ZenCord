import asyncio
from .http import DiscordHTTP
from .gateaway import DiscordGateaway
from .commands import CommandHandler

class DiscordClient:

    def __init__(self, token, prefix="!"):
        self.token = token
        self.http = DiscordHTTP(token)
        self.command_handler = CommandHandler(prefix)
        self.gateaway = DiscordGateaway(token, self.on_message)


    def command(self, name):
        return self.command_handler.command(name)

    async def start(self):
        
        await asyncio.gather(self.gateaway.connect())

    async def on_message(self, message):

        await self.command_handler.handle_command(message, self)
        print("test")

    async def send_message(self, channel_id, content):

        await self.http.send_message(channel_id, content)