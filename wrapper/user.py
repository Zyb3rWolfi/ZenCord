from .types.user import User

class User:

    def __init__(self, data: User):
        self.id = data["id"]
        self.username = data["username"]
        self.discriminator = data["discriminator"]
        self.global_name = data.get("global_name")