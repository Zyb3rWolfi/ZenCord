import httpx
import asyncio
import json

class DiscordHTTP:

    BASE_URL = "https://discord.com/api/v10"

    def __init__(self, token: str):
        self.token = token
        self.client = httpx.AsyncClient(headers={"Authorization": f"Bot {token}", "Content-Type": "application/json"})
    
    async def request(self, method: str, endpoint: str, **kwargs):

        url = f"{self.BASE_URL}{endpoint}"
        response = await self.client.request(method, url, **kwargs)
        if response.status_code == 429:
            retry_after = response.json().get("retry_after", 1)
            await asyncio.sleep(retry_after)
            return await self.request(method, endpoint, **kwargs)
        response.raise_for_status()


        try:
            return response.json()
        except:
            return
    
    async def send_message(self, channel_id: str, content: str):
        return await self.request("POST", f"/channels/{channel_id}/messages", json={"content": content})
    async def delete_message(self, channel_id: str, message_id: str): # /channels/{channel.id}/messages/{message.id}
        await self.request("DELETE", f"/channels/{channel_id}/messages/{message_id}")
    async def get_message(self, channel_id: str, message_id: str):
        await self.request("GET", f"/channels/{channel_id}/messages/{message_id}")
    async def get_messages(self, channel_id: str, message_id: str):
        return await self.request("GET", f"/channels/{channel_id}/messages?limit=5")
    async def get_channel(self, channel_id: str):
        return await self.request("GET", f"/channels/{channel_id}")
