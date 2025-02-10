class Guild:

    def __init__(self, guild_json):
        
        self.id = guild_json["id"]
        self.name = guild_json["name"]
    
