import tweepy
from Configs import Var

from telethon.sync import TelegramClient
from telethon.tl.custom import Button

import logging
logging.basicConfig(level=logging.INFO)

auth = tweepy.OAuthHandler(Var.CONSUMER_KEY, Var.CONSUMER_SECRET)
auth.set_access_token(Var.ACCESS_TOKEN, Var.ACCESS_TOKEN_SECRET)
api = tweepy.API(auth)

Client = TelegramClient("TG-Twitter Streamer", Var.API_ID,
                Var.API_HASH).start(bot_token=Var.BOT_TOKEN)


print("Setting Up Bot !")
TRACK_IDS = []
for userid in Var.TRACK_USERS.split(" "):
    try:
        user = api.get_user(userid)._json
        TRACK_IDS.append(str(user["id"]))
        print(f"Added {user['screen_name']} to TRACK - LIST !")
    except Exception as e:
        print(e)


class TgStreamer(tweepy.StreamListener):
    def on_status(self, status):
        tweet = status._json
        user = tweet["user"]
        if not user["id"] in TRACK_IDS:
            return
        text = f"[{user['name']}](https://twitter.com/{user['screen_name']})"
        mn = " ReTweeted :"
        if not tweet["retweeted"]:
            mn = " Tweeted :"
        text += mn + "\n\n" + f"`{tweet['text']}`"
        url = f"https://twitter.com/{user['screen_name']}/status/{tweet['id']}"
        Client.send_message(
            Var.TO_CHAT, text,
            link_preview=False,
            buttons=Button.url(text="View 🔗", url=url))
    def on_error(self, status_code):
        print(self, status_code)


@Client.on(events.NewMessage(pattern=r"/start"))
async def sendme(event):
    await event.reply("Hi, I am Alive !")


if __name__ == "__main__":
    Stream = TgStreamer()
    myStream = tweepy.Stream(auth=api.auth, listener=Stream)
    myStream.filter(follow=TRACK_IDS, is_async=True)
    Client.run()  # Running Client
