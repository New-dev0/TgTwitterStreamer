from decouple import config

class Var(object):
    API_ID = config("API_ID", cast=int)
    API_HASH = config("API_HASH")
    BOT_TOKEN = config("BOT_TOKEN")
    ACCESS_TOKEN = config("ACCESS_TOKEN")
    ACCESS_TOKEN_SECRET = config("ACCESS_TOKEN_SECRET")
    CONSUMER_KEY = config("CONSUMER_KEY")
    CONSUMER_SECRET = config("CONSUMER_SECRET")
    TRACK_USERS = config("TRACK_USERS")
    TO_CHAT = config("TO_CHAT", cast=int)
