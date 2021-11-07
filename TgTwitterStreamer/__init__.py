# Telegram - Twitter - Bot
# Github.com/New-dev0/TgTwitterStreamer
# GNU General Public License v3.0

import logging
from Configs import Var
from telethon import TelegramClient
from tweepy import API, OAuthHandler

LOGGER = logging.getLogger("TgTwitterStreamer")
LOGGER.setLevel(level=logging.INFO)
logging.basicConfig(
    format="[%(levelname) 5s/%(asctime)s] %(name)s: %(message)s",
    level=logging.INFO
)

# Tweepy's Client

auth = OAuthHandler(Var.CONSUMER_KEY, Var.CONSUMER_SECRET)
auth.set_access_token(Var.ACCESS_TOKEN, Var.ACCESS_TOKEN_SECRET)
Twitter = API(auth)


# Telegram's Client
# Used for sending messages to Chat.
Client = TelegramClient(
    "TgTwitterStreamer", api_id=Var.API_ID, api_hash=Var.API_HASH
).start(bot_token=Var.BOT_TOKEN)

REPO_LINK = "https://github.com/New-dev0/TgTwitterStreamer"


CUSTOM_FORMAT = """
🎊 <b><a href='{SENDER_PROFILE}'>{SENDER}</a></b> :

🍿 {TWEET_TEXT}

• Powered by <b><a href="{_REPO_LINK}">TgTwitterStreamer</a></b>
"""


if not Var.CUSTOM_TEXT:
    Client.parse_mode = "html"
    Var.CUSTOM_TEXT = CUSTOM_FORMAT

if Var.LANGUAGES:
    Var.LANGUAGES = Var.LANGUAGES.split()

# Username are easy to Fill and can easy be recognized that Unqiue Chat ids.
# And Ids should be in int form..
if Var.TO_CHAT:
    _chats = []
    for chat in Var.TO_CHAT.split():
        try:
            chat = int(chat)
        except ValueError:
            pass
        _chats.append(chat)
    Var.TO_CHAT = _chats
else:
    LOGGER.info("Please Add 'TO_CHAT' Var to Use TgTwitterStreamer!")
    LOGGER.info(
        "'TO_CHAT' : Fill Telegram Username/Chat ids,"
        + "so that you can get tweets."
    )
    LOGGER.info("Quitting Now..")
    exit()
