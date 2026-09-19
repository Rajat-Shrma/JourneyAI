# test_remote_weather.py

import asyncio
import os

from dotenv import load_dotenv
from fastmcp import Client


load_dotenv()

URL = os.getenv("WEATHER_MCP_URL")
TOKEN = os.getenv("MCP_AUTH_TOKEN")


async def main():

    print("URL:", URL)
    print("Token loaded:", bool(TOKEN))
    print("Token length:", len(TOKEN or ""))

    client = Client(
        URL,
        auth=TOKEN,
    )

    async with client:

        print("\nConnected!")

        tools = await client.list_tools()

        print("\nTools:")

        for tool in tools:
            print("-", tool.name)

        result = await client.call_tool(
            "get_current_weather",
            {
                "city": "Delhi"
            },
        )

        print("\nResult:")
        print(result)


if __name__ == "__main__":
    asyncio.run(main())