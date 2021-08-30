from decouple import config


class Var:
    API_ID = config("API_ID", default=6)
    API_HASH = config("API_HASH", None)
    BOT_TOKEN = config("BOT_TOKEN", None)
    CONSUMER_KEY = config("CONSUMER_KEY", None)
    CONSUMER_SECRET = config("CONSUMER_SECRET", None)
    ACCESS_TOKEN = config("ACCESS_TOKEN", None)
    ACCESS_TOKEN_SECRET = config("ACCESS_TOKEN_SECRET", None)
    TO_CHAT = config("TO_CHAT", None)
    TRACK_USERS = config("TRACK_USERS", None)

    CUSTOM_TEXT = config("CUSTOM_TEXT", None)
    BUTTON_TITLE = config("BUTTON_TITLE", "View on Twitter🔗")

    START_MEDIA = config("START_MEDIA", "TgTwitterStreamer/assets/START.webp")
    START_MESSAGE = config("START_MESSAGE", None)

    TAKE_REPLIES = config("TAKE_REPLIES", default=False, cast=bool)
    TAKE_RETWEETS = config("TAKE_RETWEETS", default=False, cast=bool)
