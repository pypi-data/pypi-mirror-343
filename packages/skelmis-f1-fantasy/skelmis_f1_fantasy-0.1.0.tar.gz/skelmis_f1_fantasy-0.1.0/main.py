import asyncio
import os

from fantasy import Client


async def main():
    client: Client = await Client.login(os.environ["username"], os.environ["password"])


if __name__ == "__main__":
    asyncio.run(main())
