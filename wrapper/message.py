from .http import DiscordHTTP
from .types.message import Message
from .user import User

class Message:

    def __init__(self, data: Message, http: DiscordHTTP) -> None:
        
        self.content = data["content"]
        self.id = data["id"]
        self.guild_id = data["guild_id"]
        self.author = User(data["author"])
        self.channel_id = data["channel_id"]
        self.http = http
    
    # Sends a message in the same channel as the message using HTTP
    async def send_message(self, content):
        await self.http.send_message(self.channel_id, content)
    async def delete(self):
        await self.http.delete_message(self.channel_id, self.id)

