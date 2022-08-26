# Telegram - Twitter - Bot
# Github.com/New-dev0/TgTwitterStreamer
# GNU General Public License v3.0

from aiohttp import ClientSession
from Configs import Var


async def download_from_url(url, name=None):
    """
    Download file to local
    """
    if isinstance(url, list):
        return [await download_from_url(_) for _ in url]

    if not name:
        name = url.split("/")[-1]
        if "?tag=" in name:
            name = name.split("?tag=")[0]
    name = f"{Var.MEDIA_DL_PATH}/{name}"
    async with ClientSession() as ses:
        async with ses.get(url) as out:
            with open(name, "wb") as f:
                f.write(await out.read())
        return name
