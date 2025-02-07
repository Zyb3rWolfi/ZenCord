class Message:

    def __init__(self, message_json):
        self.message_obj = message_json
        self.content = message_json["content"]
        self.id = message_json["id"]
        self.author = Author(message_json["author"])
        self.guild_id = message_json["guild_id"]
        self.channel_id = message_json["channel_id"]
    
class Author:

    def __init__(self, author):
        self.id = author["id"]
        self.username = author["username"]
        self.global_name = author["global_name"]
        self.discriminator = author["discriminator"]