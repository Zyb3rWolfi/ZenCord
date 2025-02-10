class Guild:

    def __init__(self, guild_json):
        
        self.id = guild_json["id"]
        self.name = guild_json["name"]
        self.members = {}
    
        for member_data in guild_json.get("members", []):

            member = Member(member_data)
            self.members[member.id] = member
    
    def get_member(self, member_id):
        return self.members.get(member_id)


class Member:

    def __init__(self, data):
        self.id = data["user"]["id"]
        self.name = data["user"]["username"]
    
