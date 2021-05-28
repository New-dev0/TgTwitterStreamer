import tweepy
from Configs import Var

from telethon import TelegramClient
from telethon.tl.custom import Button

from tweepy.asynchronous import AsyncStream
import logging
logging.basicConfig(level=logging.INFO)


Client = TelegramClient("TG-Twitter Streamer", Var.API_ID,
                Var.API_HASH).start(bot_token=Var.BOT_TOKEN)

auth = tweepy.OAuthHandler(Var.CONSUMER_KEY, Var.CONSUMER_SECRET)
auth.set_access_token(Var.ACCESS_TOKEN, Var.ACCESS_TOKEN_SECRET)
api = tweepy.API(auth)


print("Setting Up Bot !")
TRACK_IDS = []
for userid in Var.TRACK_USERS.split(" "):
    try:
        user = api.get_user(screen_name=userid)._json
        TRACK_IDS.append(str(user["id"]))
        print(f"Added {user['screen_name']} to TRACK - LIST !")
    except Exception as e:
        print(e)


class TgStreamer(AsyncStream):
    async def on_connect(self):
        print("<<<---||| Stream Connected |||--->>>")
    async def on_status(self, status):
        tweet = status._json
        user = tweet["user"]
        print("Users", user)
        if not user["id"] in TRACK_IDS:
            return
        print(user["id"])
        text = f"[{user['name']}](https://twitter.com/{user['screen_name']})"
        mn = " ReTweeted :"
        if not tweet["retweeted"]:
            mn = " Tweeted :"
        text += mn + "\n\n" + f"`{tweet['text']}`"
        url = f"https://twitter.com/{user['screen_name']}/status/{tweet['id']}"
        await Client.send_message(
            Var.TO_CHAT, text,
            link_preview=False,
            buttons=Button.url(text="View 🔗", url=url))
    
    async def on_connection_error(self):
        print("Connection Error, Disconnecting...")
    
    async def on_exception(self, exception):
        print(exception)


if __name__ == "__main__":
    Stream = TgStreamer(Var.CONSUMER_KEY,Var.CONSUMER_SECRET,Var.ACCESS_TOKEN,Var.ACCESS_TOKEN_SECRET)
    Stream.filter(follow=TRACK_IDS)
    with Client:
        Client.run_until_disconnected()  # Running Client
