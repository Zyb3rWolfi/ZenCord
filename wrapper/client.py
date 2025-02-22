import asyncio
import json
from .http import DiscordHTTP
from .gateaway import DiscordGateaway
from .commands.commands import CommandHandler
from .message import Message
from .types.guild import Guild

class DiscordClient:

    def __init__(self, token, prefix="!"):
        self.token = token # Bot token
        self.http = DiscordHTTP(token) # the HTTP class
        self.command_handler = CommandHandler(prefix) # Command handler class
        self.gateaway = DiscordGateaway(token, self.on_message, self._handle_event) # Discord gateaway class
        self.events = {}


    def event(self, func):

        self.events[func.__name__] = func
        return func

    async def _handle_event(self, event_name, data):
        """Internal method to call registered events."""
        if event_name in self.events:
            await self.events[event_name](data)

    # Manages the command decorater
    def command(self, name):
        return self.command_handler.command(name)

    # Responsible for starting the bot
    async def start(self):
        
        await asyncio.gather(self.gateaway.connect())
    
    # Runs the command handler everytime theres a message
    async def on_message(self, message: dict):
            from .commands.context import Context
            message = Message(message, self.http)
            context = Context(message, self)
            if (self.gateaway.bot_id == message.author.id):
                return
            await self.command_handler.handle_command(context, self)



    # Functions utilising HTTP requests

    async def send_message(self, channel_id, content):

        await self.http.send_message(channel_id, content)

    async def delete_message(self, channel_id, message_id):

        await self.http.delete_message(channel_id, message_id)
    
    async def get_message(self, channel_id, message_id):

        message = await self.http.get_message(channel_id, message_id)
        return message
    
    async def get_messages(self, channel_id, message_id):

        messages = await self.http.get_messages(channel_id, message_id)
        messagess = Message(messages[0], self.token)
        return messages[0]
    
    # Functions utilising the Discord Gateaway

    def get_guild(self, guild_id):

        return self.gateaway.guilds[guild_id]
    
    def get_bot_id(self):

        return self.gateaway.bot_id

    def get_channel(self, channel_id):
        
        return self.http.get_channel(channel_id)
