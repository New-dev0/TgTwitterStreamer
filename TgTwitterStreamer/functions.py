# Telegram - Twitter - Bot
# Github.com/New-dev0/TgTwitterStreamer
# GNU General Public License v3.0

import aiofiles
from aiohttp import ClientSession


async def download_from_url(url, name: None):
    """
    Download file to local
    """
    if isinstance(url, list):
        return [await download_from_url(_) for _ in url]

    if not name:
        name = url.split("/")[-1]

    async with ClientSession() as ses:
        async with ses.get(url) as out:
            file = await aiofiles.open(name, "wb")
            await file.write(await out.read())
            await file.close()
        return name
