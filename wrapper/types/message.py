from typing import TypedDict, NotRequired
from .user import User

class Message(TypedDict):
    id: str
    author: User
    content: str
    content: str
    channel_id: str
    guild_id: str

