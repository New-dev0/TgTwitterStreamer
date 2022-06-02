# Telegram - Twitter - Bot
# Github.com/New-dev0/TgTwitterStreamer
# GNU General Public License v3.0

import logging
from Configs import Var
from telethon import TelegramClient
from telethon.tl.custom import Button
from tweepy import API, OAuthHandler
from tweepy.errors import Unauthorized

REPO_LINK = "https://github.com/New-dev0/TgTwitterStreamer"

LOGGER = logging.getLogger("TgTwitterStreamer")
LOGGER.setLevel(level=logging.INFO)
logging.basicConfig(
    format="[%(levelname) 5s/%(asctime)s] %(name)s: %(message)s", level=logging.INFO
)

# Tweepy's Client

auth = OAuthHandler(Var.CONSUMER_KEY, Var.CONSUMER_SECRET)
auth.set_access_token(Var.ACCESS_TOKEN, Var.ACCESS_TOKEN_SECRET)
Twitter = API(auth)


# Telegram's Client
# Used for sending messages to Chat.

Client = TelegramClient(
    None,
    api_id=Var.API_ID,
    api_hash=Var.API_HASH,
).start(bot_token=Var.BOT_TOKEN)


CUSTOM_BUTTONS = None
TRACK_IDS = None
CUSTOM_FORMAT = """
📌 <b><a href='{SENDER_PROFILE}'>{SENDER}</a></b> :

📃 {TWEET_TEXT}
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


if Var.TRACK_USERS:
    TRACK_IDS = []
    for username in Var.TRACK_USERS.split(" "):
        try:
            user = Twitter.get_user(screen_name=username)._json
            TRACK_IDS.append(user["id_str"])
            LOGGER.info(f"<<--- Added {user['screen_name']} to TRACK - LIST ! --->>")
        except Unauthorized as er:
            LOGGER.exception(er)
            exit()
        except Exception as e:
            LOGGER.exception(e)


TRACK_WORDS = Var.TRACK_WORDS.split(" | ") if Var.TRACK_WORDS else None
