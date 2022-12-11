# Telegram - Twitter - Bot
# Github.com/New-dev0/TgTwitterStreamer
# GNU General Public License v3.0

import sys, os
import logging
from Configs import Var
from telethon import TelegramClient
from telethon.tl.custom import Button
from tweepy.asynchronous import AsyncClient

if not os.path.exists(Var.MEDIA_DL_PATH):
    os.mkdir(Var.MEDIA_DL_PATH)

REPO_LINK = "https://github.com/New-dev0/TgTwitterStreamer"

_DEBUG = "--debug" in sys.argv

logging.basicConfig(
    format="[%(levelname) 5s/%(asctime)s] %(name)s: %(message)s",
    level=logging.INFO if not _DEBUG else logging.DEBUG,
)

LOGGER = logging.getLogger("TgTwitterStreamer")

if Var.LOG_FILE:
    if not _DEBUG and os.path.exists(Var.LOG_FILE):
        try:
            os.remove(Var.LOG_FILE)
        except Exception as er:
            LOGGER.error(er)
    LOGGER.addHandler(logging.FileHandler(Var.LOG_FILE, encoding="utf-8"))

LOGGER.debug("Starting in debug mode..")

# Tweepy's Client
Twitter = AsyncClient(
    Var.BEARER_TOKEN,
    Var.CONSUMER_KEY,
    Var.CONSUMER_SECRET,
    Var.ACCESS_TOKEN,
    Var.ACCESS_TOKEN_SECRET,
)

# Telegram's Client
# Used for sending messages to Chat.

_Tlog = logging.getLogger("Telethon")
_Tlog.setLevel(logging.INFO)

Client = TelegramClient(
    None, api_id=Var.API_ID, api_hash=Var.API_HASH, base_logger=_Tlog
).start(bot_token=Var.BOT_TOKEN)

Client.SELF = Client.loop.run_until_complete(Client.get_me())

CUSTOM_BUTTONS = None
TRACK_USERS = None
TRACK_WORDS = None


CUSTOM_FORMAT = """
🎊 <b><a href='{SENDER_PROFILE}'>{SENDER}</a></b> :
{REPLY_TAG}
🍿 {TWEET_TEXT}

• Powered by <b><a href="{_REPO_LINK}">TgTwitterStreamer</a></b>
"""


if not Var.CUSTOM_TEXT:
    Client.parse_mode = "html"
    Var.CUSTOM_TEXT = CUSTOM_FORMAT

if Var.LANGUAGES:
    Var.LANGUAGES = Var.LANGUAGES.split()


def parse_chats(chats):
    _chats = []
    for chat in chats:
        try:
            chat = int(chat)
        except ValueError:
            pass
        _chats.append(chat)
    return _chats


# Username are easy to Fill and can easy be recognized that Unqiue Chat ids.
# And Ids should be in int form..
if Var.TO_CHAT:
    Var.TO_CHAT = parse_chats(Var.TO_CHAT.split())
else:
    LOGGER.info("Please Add 'TO_CHAT' Var to Use TgTwitterStreamer!")
    LOGGER.info(
        "'TO_CHAT' : Fill Telegram Username/Chat ids," + "so that you can get tweets."
    )
    LOGGER.info("Quitting Now..")
    exit()


if Var.CUSTOM_BUTTON:
    button = []
    try:
        for line in Var.CUSTOM_BUTTON.split("||"):
            new = []
            for but in line.split("|"):
                spli_ = but.split("-", maxsplit=1)
                new.append(Button.url(spli_[0].strip(), spli_[1].strip()))
            button.append(new)
        CUSTOM_BUTTONS = button
    except Exception as er:
        LOGGER.exception(er)


LOGGER.info("<<--- Setting Up Bot ! --->>")

CUSTOM_TRACK_CHAT = {}
TRACK_USERS = []

if Var.TRACK_USERS:
    _TRACK_USERS = Var.TRACK_USERS.strip().split(" ")
    for user in _TRACK_USERS:
        if "-" in user:
            split = user.split("-")
            last_elm = split[len(split) - 1]
            last_topid = last_elm.isdigit()
            if len(split) > 1:
                msg_id = None
                user = split[0].lower()
                chats = split[1 : len(split) - (1 if last_topid else 0)]
                if last_topid:
                    msg_id = int(last_elm)
                CUSTOM_TRACK_CHAT[user] = {"chats": chats, "topic_id": msg_id}
        TRACK_USERS.append(user)

LOGGER.debug(f"custom chats: {CUSTOM_TRACK_CHAT}")
TRACK_USERS = list(set(TRACK_USERS))
LOGGER.debug(f"track users: {TRACK_USERS}")

if Var.TRACK_WORDS:
    TRACK_WORDS = Var.TRACK_WORDS.split(" | ")
