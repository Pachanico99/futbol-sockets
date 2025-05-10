import asyncio
from api.client.FutbolSocketsClient import FutbolWebsocketsClient

async def main():
    server_uri = "wss://machuca.com.ar:4000"
    client = FutbolWebsocketsClient(server_uri)
    await client.run()

if __name__ == "__main__":
    asyncio.run(main())