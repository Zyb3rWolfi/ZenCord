import asyncio
import websockets
import aiohttp
import json
from .types.guild import Guild
from .types.message import Message

class DiscordGateaway:

    GATEAWAY_URL = "wss://gateway.discord.gg/?v=10&encoding=json"

    def __init__(self, token, on_message_callback, handle_event):
        self.token = token
        self.session_id = None
        self.on_message_callback = on_message_callback
        self.bot_id = None
        self.event_handler = handle_event
        self.guilds = {}
    
    # Connect to the discord gateaway
    async def connect(self):

        async with websockets.connect(self.GATEAWAY_URL) as ws:
            
            await self.identify(ws)
            async for message in ws:
                await self.handle_event(ws, message)

    # Used to identify the client  
    async def identify(self, ws):
        
        payload = {
            "op": 2,
            "d": {
                "token": self.token,
                "intents": 513 | (1 << 15),  # Adjust intents based on needed events
                "properties": {
                    "$os": "linux",
                    "$browser": "wrapper",
                    "$device": "wrapper"
                }
            }
        }
        await ws.send(json.dumps(payload))
        response = json.loads(await ws.recv())
    
    # Handling gateaway events
    async def handle_event(self, ws, message):

        data = json.loads(message)

        if data["op"] == 10:  # Hello event (keep connection alive)
            self.session_id = data["d"].get("session_id")
            heartbeat_interval = data["d"]["heartbeat_interval"] / 1000
            asyncio.create_task(self.heartbeat(ws, heartbeat_interval))
        elif data["t"] == "READY":
            self.bot_id = data["d"]["user"]["id"]
            await self.event_handler("on_ready", data["d"])
        elif data["t"] == "MESSAGE_CREATE": # Message created event
            if self.on_message_callback:
                await self.event_handler("on_message", Message(data["d"], self.token))
        elif data["t"] == "GUILD_CREATE":
            guild = Guild(data["d"])
            self.guilds[guild.id] = guild

    
    # Manages the heartbeat between the bot and Discord
    async def heartbeat(self, ws, interval):

        while True:
            await asyncio.sleep(interval)
            if self.session_id:  # Ensure the session_id is set
                await ws.send(json.dumps({"op": 1, "d": self.session_id}))


    async def listen(self):

        async with websockets.connect(self.GATEWAY_URL) as ws:
            await self.identify(ws)
            async for message in ws:
                await self.handle_event(ws, message)