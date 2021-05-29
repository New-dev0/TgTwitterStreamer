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

    def get_urls(self, media):
        if not media:
            return []
        return [m['media_url_https'] for m in media if m['type'] == 'photo']

    async def on_status(self, status):
        tweet = status._json
        if tweet["text"].startswith("RT "):
            return
        user = tweet["user"]
        if not str(user["id"]) in TRACK_IDS:
            return
        try:
            entities = tweet.get('entities', {}).get('media')
            extended_entities = tweet.get('extended_entities', {}).get('media')
            extended_tweet = tweet.get('extended_tweet', {}).get('entities', {}).get('media')
            all_urls = set()
            for media in (entities, extended_entities, extended_tweet):
                urls = self.get_urls(media)
                print(urls)
                all_urls.update(set(urls))
            print(all_urls)
        except BaseException:
            pass
        text = f"[{user['name']}](https://twitter.com/{user['screen_name']})"
        mn = " Tweeted :"
        text += mn + "\n\n" + f"`{tweet['text']}`"
        url = f"https://twitter.com/{user['screen_name']}/status/{tweet['id']}"
        multichat = Var.TO_CHAT.split()
        for chat in multichat:
            try:
                chat = int(chat)
            except BaseException:
                pass
            await Client.send_message(
                chat,
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
