# Telegram - Twitter - Bot
# Github.com/New-dev0/TgTwitterStreamer
# GNU General Public License v3.0

import re
from telethon.tl.custom import Button
from . import REPO_LINK, TRACK_WORDS

from .tstreamer import TgStreamer, TRACK_IDS, Var, Client
from telethon.events import NewMessage, CallbackQuery


async def start_message(event):
    await event.reply(
        Var.START_MESSAGE,
        file=Var.START_MEDIA,
        buttons=[
            [
                Button.url(
                    "Channel",
                    url="https://t.me/CryptoNite_News",
                ),
                Button.url("Group", url="https://t.me/Cryptonite_club"),
            ],
        ],
    )


async def callback_query(event):
    await event.answer("I'm Alive , No Need to click button..")


# For people, deploying multiple apps on one bot. (including "me")

if not Var.DISABLE_START:
    Client.add_event_handler(start_message, NewMessage(pattern="^/start$"))
    Client.add_event_handler(callback_query, CallbackQuery(data=re.compile("ok")))


if __name__ == "__main__":
    Stream = TgStreamer(
        Var.CONSUMER_KEY, Var.CONSUMER_SECRET, Var.ACCESS_TOKEN, Var.ACCESS_TOKEN_SECRET
    )
    Stream.filter(
        follow=TRACK_IDS,
        track=TRACK_WORDS,
        filter_level=Var.FILTER_LEVEL,
        languages=Var.LANGUAGES,
    )

    with Client:
        Client.run_until_disconnected()  # Running Client
