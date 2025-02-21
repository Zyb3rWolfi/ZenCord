from typing import TypedDict, NotRequired

class User(TypedDict):

    id: str
    username: str
    discriminator: str
    global_name: NotRequired[str]
