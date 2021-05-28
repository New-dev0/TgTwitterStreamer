import tweepy
from Configs import Var

from telethon.sync import TelegramClient
from telethon.tl.custom import Button

import logging
logging.basicConfig(level=logging.INFO)


Client = TelegramClient("TG-Twitter Streamer", Var.API_ID,
                Var.API_HASH).start(bot_token=Var.BOT_TOKEN)


print("Setting Up Bot !")
TRACK_IDS = []
for userid in Var.TRACK_USERS.split(" "):
    try:
        user = api.get_user(screen_name=userid)._json
        TRACK_IDS.append(str(user["id"]))
        print(f"Added {user['screen_name']} to TRACK - LIST !")
    except Exception as e:
        print(e)


class TgStreamer(tweepy.Stream):
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


if __name__ == "__main__":
    Stream = TgStreamer(Var.CONSUMER_KEY,Var.CONSUMER_SECRET,Var.ACCESS_TOKEN,Var.ACCESS_TOKEN_SECRET)
    Stream.filter(follow=TRACK_IDS)
    with Client:
        Client.run_until_disconnected()  # Running Client
