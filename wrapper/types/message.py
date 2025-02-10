from ..http import DiscordHTTP

class Message:

    def __init__(self, message_json, token):
        self.bot_token = token
        self.http = DiscordHTTP(token)
        self.message_obj = message_json
        
        self.content = message_json["content"]
        self.id = message_json["id"]
        self.author = Author(message_json["author"])
        self.guild_id = message_json["guild_id"]
        self.channel_id = message_json["channel_id"]
    
    # Sends a message in the same channel as the message using HTTP
    async def send_message(self, content):
        await self.http.send_message(self.channel_id, content)
    
class Author:

    def __init__(self, author):
        self.id = author["id"]
        self.username = author["username"]
        self.global_name = author["global_name"]
        self.discriminator = author["discriminator"]