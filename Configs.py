# Telegram - Twitter - Bot
# Github.com/New-dev0/TgTwitterStreamer
# GNU General Public License v3.0

from decouple import config


class Var:
    # Telegram's API ID
    API_ID = config("API_ID", default=6)
    # Telegram's API HASH
    API_HASH = config("API_HASH", default="eb06d4abfb49dc3eeb1aeb98ae0f581e")
    # Telegram Bot's token
    BOT_TOKEN = config("BOT_TOKEN", None)

    # Twitter Vars
    BEARER_TOKEN = config("BEARER_TOKEN", None)
    CONSUMER_KEY = config("CONSUMER_KEY", None)
    CONSUMER_SECRET = config("CONSUMER_SECRET", None)
    ACCESS_TOKEN = config("ACCESS_TOKEN", None)
    ACCESS_TOKEN_SECRET = config("ACCESS_TOKEN_SECRET", None)

    # Telegram Chat id(s), where to send Tweets
    TO_CHAT: str = config("TO_CHAT", None)

    # Username of Twitter User, whose Tweets should be tracked
    # and posted to chat filled in TO_CHAT.
    TRACK_USERS = config("TRACK_USERS", None)

    # TRACK_WORDS: To filter Tweets by word
    # Should be seperated by "|"
    TRACK_WORDS = config("TRACK_WORDS", None)

    # Custom Text format to be used, while sending Tweets.
    CUSTOM_TEXT = config("CUSTOM_TEXT", None)
    # Text to Display on Button, Attached to Message Posted on Telegram.
    BUTTON_TITLE = config("BUTTON_TITLE", "View on Twitter🔗")
    # Set DISABLE_BUTTON to True, to disable that Button.
    CUSTOM_BUTTON = config("CUSTOM_BUTTON", default=None)
    DISABLE_BUTTON = config("DISABLE_BUTTON", default=False, cast=bool)

    # Media Url, to be send with '/start' message.
    START_MEDIA = config("START_MEDIA", "TgTwitterStreamer/assets/START.webp")
    if START_MEDIA == "None":
        START_MEDIA = None
    # Caption/text of '/start' message.
    START_MESSAGE = config("START_MESSAGE", None)
    DISABLE_START = config("DISABLE_START", default=False, cast=bool)

    REPLIED_NOTE = config(
        "REPLY_FORMAT",
        default="[Replied to this post]({REPLY_URL})\n"
        if CUSTOM_TEXT
        else "<a href='{REPLY_URL}'>[Replied to this Post]</a>\n",
    )

    # Whether should take messages, which are reply to other post.
    TAKE_REPLIES = config("TAKE_REPLIES", default=True, cast=bool)
    # Whether to Take Retweets or not.
    TAKE_RETWEETS = config("TAKE_RETWEETS", default=False, cast=bool)
    # Whether to just include tweets containing media.
    MEDIA_ONLY = config("MEDIA_ONLY", default=False, cast=bool)

    # An Addition word checking filters.
    MUST_INCLUDE = config("MUST_INCLUDE", default=None)
    EXCLUDE = config("EXCLUDE_WORDS", default=None)
    if EXCLUDE:
        EXCLUDE = EXCLUDE.split("|")

    # Automations
    AUTO_LIKE = config("AUTO_LIKE", default=False, cast=bool)
    AUTO_RETWEET = config("AUTO_RETWEET", default=False, cast=bool)
    AUTO_PIN = config("AUTO_PIN", default=False, cast=bool)

    # Filter Language of Tweets
    LANGUAGES = config("LANGUAGES", default="en")
    if LANGUAGES == "None":
        LANGUAGES = None

    MEDIA_DL_PATH = config("MEDIA_DL_PATH", default="media")
    LOG_FILE = config("LOG_FILE", default="Stream.log")
    MAX_RECONNECT = config("MAX_RECONNECT", cast=int, default=20)
