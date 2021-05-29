# Telegram - Twitter - Bot
# Github.com/New-dev0/TgTwitterStreamer
# GNU General Public License v3.0


import tweepy
from Configs import Var
from telethon import TelegramClient, events
from telethon.tl.custom import Button

from tweepy.asynchronous import AsyncStream

import logging
logging.basicConfig(level=logging.INFO)


Client = TelegramClient("TG-Twitter Streamer", Var.API_ID, Var.API_HASH).start(
    bot_token=Var.BOT_TOKEN
)

auth = tweepy.OAuthHandler(Var.CONSUMER_KEY, Var.CONSUMER_SECRET)
auth.set_access_token(Var.ACCESS_TOKEN, Var.ACCESS_TOKEN_SECRET)
api = tweepy.API(auth)

print("<<--- Setting Up Bot ! --->>")
TRACK_IDS = []
for userid in Var.TRACK_USERS.split(" "):
    try:
        user = api.get_user(screen_name=userid)._json
        TRACK_IDS.append(str(user["id"]))
        print(f"<<--- Added {user['screen_name']} to TRACK - LIST ! --->>")
    except Exception as e:
        print(e)


class TgStreamer(AsyncStream):
    async def on_connect(self):
        print("<<<---||| Stream Connected |||--->>>")

    async def on_status(self, status):
        tweet = status._json
        print(tweet)
        user = tweet["user"]
        if not str(user["id"]) in TRACK_IDS:
            return
        if tweet["text"].startswith("RT "):
            return
        text = f"[{user['name']}](https://twitter.com/{user['screen_name']})"
        mn = " Tweeted :"
        text += mn + "\n\n" + f"`{tweet['text']}`"
        url = f"https://twitter.com/{user['screen_name']}/status/{tweet['id']}"
        await Client.send_message(
            Var.TO_CHAT,
            text,
            link_preview=False,
            buttons=Button.url(text="View 🔗", url=url),
        )

    async def on_connection_error(self):
        print("<<---|| Connection Error ||--->>")

    async def on_exception(self, exception):
        print(exception)


@Client.on(events.NewMessage(pattern=r"/start"))
async def startmsg(event):
    await event.reply(
        "Hi, I am Alive !",
        buttons=[
            [
                Button.url(
                    "TgTwitterStreamer",
                    url="https://github.com/New-dev0/TgTwitterStreamer",
                )
            ],
            [Button.url("Support Group", url="t.me/FutureCodesChat")],
        ],
    )


if __name__ == "__main__":
    Stream = TgStreamer(
        Var.CONSUMER_KEY,
        Var.CONSUMER_SECRET,
        Var.ACCESS_TOKEN,
        Var.ACCESS_TOKEN_SECRET
    )
    Stream.filter(follow=TRACK_IDS)

    with Client:
        Client.run_until_disconnected()  # Running Client
