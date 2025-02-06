import httpx
import asyncio

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
        return response.json()
    
    async def send_message(self, channel_id: str, content: str):
        return await self.request("POST", f"/channels/{channel_id}/messages", json={"content": content})