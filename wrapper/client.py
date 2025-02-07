import asyncio
from .http import DiscordHTTP
from .gateaway import DiscordGateaway
from .commands import CommandHandler
from .message import Message
from .guild import Guild

class DiscordClient:

    def __init__(self, token, prefix="!"):
        self.token = token # Bot token
        self.http = DiscordHTTP(token) # the HTTP class
        self.command_handler = CommandHandler(prefix) # Command handler class
        self.gateaway = DiscordGateaway(token, self.on_message) # Discord gateaway class


    # ??
    def command(self, name):
        return self.command_handler.command(name)

    # Responsible for starting the bot
    async def start(self):
        
        await asyncio.gather(self.gateaway.connect())
    
    # Runs the command handler everytime theres a message
    async def on_message(self, message):
        message = Message(message)
        if (self.gateaway.bot_id == message.author.id):
            return
        await self.command_handler.handle_command(message, self)

    # Responsible for sending messages
    async def send_message(self, channel_id, content):

        await self.http.send_message(channel_id, content)

    # Responsible for getting a guild object and returning it to the user using gateaway guilds dictionary
    def get_guild(self, guild_id):

        return self.gateaway.guilds[guild_id]