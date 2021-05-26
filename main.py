import tweepy
from Configs import Var

from pyrogram import Client, filters
from pyrogram.types import (
    InlineKeyboardMarkup, 
    InlineKeyboardButton
)

import logging
logging.basicConfig(level=logging.INFO)

auth = tweepy.OAuthHandler(Var.CONSUMER_KEY, Var.CONSUMER_SECRET)
auth.set_access_token(Var.ACCESS_TOKEN, Var.ACCESS_TOKEN_SECRET)
api = tweepy.API(auth)

Client = Client("TG-Twitter Streamer", Var.API_ID,
                Var.API_HASH,
                bot_token=Var.BOT_TOKEN)


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
            disable_web_page_preview=True,
            reply_markup=InlineKeyboardMarkup([
                [InlineKeyboardButton(text="View 🔗", url=url)]
                ])
        )

    def on_error(self, status_code):
        print(status_code)


@Client.on_message(filters.command("start") & filters.chat(int(Var.TO_CHAT)))
async def sendme(client, message):
    await message.reply_text("Hi, I am Alive !")


if __name__ == "__main__":
    Stream = TgStreamer()
    myStream = tweepy.Stream(auth=api.auth, listener=Stream)
    myStream.filter(follow=TRACK_IDS, is_async=True)
    Client.run()  # Running Client
