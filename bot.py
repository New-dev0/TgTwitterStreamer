import contextlib
import os, asyncio
import logging, json
from asyncio import run
from Configs import Var

logging.basicConfig(
    level=logging.INFO,
    handlers=[logging.FileHandler(Var.LOG_FILE), logging.StreamHandler()],
)
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from tweeterpy import TweeterPy, config
from telethon import TelegramClient, Button
from itertools import cycle
from urllib.parse import urlparse
from decouple import RepositoryEnv
from aiohttp import ClientSession

LOGS = logging.getLogger("TgTwitterStreamer")
REPO_LINK = "https://github.com/New-dev0/TgTwitterStreamer"


Client = TelegramClient("tgtwitter", api_id=Var.API_ID, api_hash=Var.API_HASH)
Client.start(bot_token=Var.BOT_TOKEN)

Client.SELF = Client.loop.run_until_complete(Client.get_me())

CUSTOM_BUTTONS = None
TRACK_USERS = list({x.strip() for x in Var.TRACK_USERS.split()})
TRACK_WORDS = None

CUSTOM_FORMAT = """
🎊 <b><a href='{SENDER_PROFILE}'>{SENDER}</a></b> :

🍿 {TWEET_TEXT}

• Powered by <b><a href="{_REPO_LINK}">TgTwitterStreamer</a></b>
"""
if not Var.CUSTOM_TEXT:
    Client.parse_mode = "html"
    Var.CUSTOM_TEXT = CUSTOM_FORMAT


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
        LOGS.exception(er)


twitterClients = []
if Var.ACCOUNTS_FILE and os.path.exists(Var.ACCOUNTS_FILE):
    newAccountFile = ""
    with open(Var.ACCOUNTS_FILE, "r") as f:
        for line in f.read().split("\n"):
            if "|" in line:
                split = line.strip().split("|")
                twitter_client = TweeterPy()

                if len(split) == 3:
                    email, password, session_path = split
                    twitter_client.load_session(session_path)
                else:
                    email, password = split
                    twitter_client.login(email, password)
                    sessionPath = twitter_client.save_session()
                twitterClients.append(twitter_client)
elif Var.TWITTER_SESSION_PATH:
    twitter_client = TweeterPy()
    twitter_client.load_session(Var.TWITTER_SESSION_PATH)
    twitterClients.append(twitter_client)
elif Var.TWITTER_USERNAME and Var.TWITTER_PASSWORD:
    twitter_client = TweeterPy()
    twitter_client.login(Var.TWITTER_USERNAME, Var.TWITTER_PASSWORD)
    session_path = twitter_client.save_session()
    twitterClients.append(twitter_client)
    dumpData = RepositoryEnv(".env").data
    dumpData["TWITTER_SESSION_PATH"] = session_path
    with open(".env", "w") as f:
        for x, y in dumpData.items():
            f.write(f"{x}={y}\n")
else:
    LOGS.error(
        "Please fill 'TWITTER_USERNAME' and 'TWITTER_PASSWORD' or 'ACCOUNTS_FILE'"
    )
    exit()


def parse_chats(chats):
    _chats = []
    for chat in chats:
        with contextlib.suppress(ValueError):
            chat = int(chat)
        _chats.append(chat)
    return _chats


if Var.TO_CHAT:
    Var.TO_CHAT = parse_chats(Var.TO_CHAT.split())
else:
    LOGS.info("Please fill 'TO_CHAT' to receive your tweets!")
    exit()


twitter = cycle(twitterClients)


async def downloadFile(url, path=None):
    if not path:
        path = url.rpartition("/")[-1].split("?")[0]
    async with ClientSession() as ses:
        async with ses.get(url) as res:
            with open(path, "wb") as f:
                f.write(await res.read())
    return path


class TgTwitterStreamer:

    def getStoredData(self):
        if os.path.exists(Var.CACHE_FILE):
            with open(Var.CACHE_FILE, "r") as f:
                storedIds = json.load(f)
        else:
            storedIds = {}
        return storedIds

    def setStoredData(self, data):
        with open(Var.CACHE_FILE, "w") as f:
            json.dump(data, f)

    async def sendToChats(self, message, thumb=None):
        print(message)

        for chat in Var.TO_CHAT:
            try:
                await Client.send_message(chat, message, file=thumb)
            except Exception as er:
                LOGS.exception(er)
            await asyncio.sleep(Var.SEND_SLEEP)

    def format_tweet(self, **kwargs):
        try:
            return Var.CUSTOM_TEXT.format(**kwargs)
        except KeyError:
            LOGS.error("Your 'CUSTOM_TEXT' seems to be wrong!\nPlease Correct It!")
            Var.CUSTOM_TEXT = CUSTOM_FORMAT
            Client.parse_mode = "html"
            return CUSTOM_FORMAT.format(**kwargs)

    async def fetchNewTweets(self):
        storedIds = self.getStoredData()

        for x in TRACK_USERS:
            client: TweeterPy = next(twitter)
            firstRun = not bool(storedIds.get(x))
            tweets = client.get_user_tweets(
                x, with_replies=Var.TAKE_REPLIES, total=Var.TWEET_FETCH_LIMIT
            )
            initialId = storedIds.get(x)

            itemsBox = []
            for media in tweets["data"]:
                if not media.get("content", {}).get("items"):
                    items = [media["content"]]
                else:
                    items = media["content"]["items"]

                for item in items:
                    try:
                        if item.get("itemContent"):
                            result = item["itemContent"]["tweet_results"]["result"]
                        else:

                            result = item["item"]["itemContent"]["tweet_results"][
                                "result"
                            ]

                        itemsBox.append(result)
                    except KeyError as er:
                        LOGS.error(er)

            itemsBox = itemsBox[::-1]
            if not firstRun:
                if findIndex := list(
                    filter(
                        lambda tdata: (
                            tdata[1].get("legacy")
                            or tdata[1].get("tweet", {}).get("legacy")
                        )["id_str"]
                        == storedIds[x],
                        enumerate(itemsBox),
                    )
                ):
                    index = findIndex[0][0]
                    itemsBox = itemsBox[index + 1 :]
            if not itemsBox:
                continue

            storedIds[x] = itemsBox[-1]["legacy"]["id_str"]
            self.setStoredData(storedIds)

            if firstRun:
                continue

            for result in itemsBox:
                try:
                    legacyInfo = result.get("legacy") or result.get("tweet", {}).get(
                        "legacy"
                    )
                    userInfo = (
                        result.get("core", {}).get("user_results", {}).get("result", {})
                    ).get("legacy")
                    twId = legacyInfo["id_str"]

                    if initialId and initialId == twId:
                        break

                    entities = legacyInfo["entities"].get("media", [])
                    entities.extend(
                        legacyInfo.get("extended_entities", {}).get("media", [])
                    )
                    hashtags = None
                    if entities and entities.get("hashtags"):
                        hashtags = " ".join(
                            f"#{a['tag']}" for a in entities["hashtags"]
                        )

                    extra_text = None
                    if result.get("quoted_status_result"):
                        try:
                            data = result["quoted_status_result"]["result"]["legacy"]
                            entities.extend(data.get("entities", {}).get("media", []))
                            entities.extend(
                                data.get("extended_entities", {}).get("media", [])
                            )
                            extra_text = data.get("full_text")
                        except Exception as eR:
                            print(eR)

                    videoFormat = list(filter(lambda x: x["type"] == "video", entities))
                    photoFormat = list(filter(lambda x: x["type"] == "photo", entities))
                    thumb = None
                    name = None
                    text = legacyInfo.get("full_text", "")
                    if extra_text:
                        text += f"\n\n{extra_text}"
                    for y in entities:
                        if y["expanded_url"].startswith("https://twitter.com/") and y[
                            "expanded_url"
                        ].split("/")[-2] in [
                            "photo",
                            "video",
                        ]:
                            replace = ""
                        else:
                            replace = y["expanded_url"]
                        text = text.replace(y["url"], replace)
                    for ny in text.split():
                        url = urlparse(ny)
                        if (url.netloc and url.scheme) and "//t.co/" in ny:
                            async with ClientSession() as ses:
                                request = await ses.get(ny)
                                newurl = request.url
                            text = text.replace(ny, newurl)
                    if videoFormat:
                        file = videoFormat[0]
                        Info = file.get("video_info")
                        if Info.get("variants"):
                            variant = Info["variants"]
                            url = None
                            if mp4 := list(
                                filter(
                                    lambda x: x["content_type"] == "video/mp4",
                                    variant,
                                )
                            ):
                                url = mp4[0]["url"]
                            else:
                                url = variant[0]["url"]
                            name = await downloadFile(url)
                    if photoFormat:
                        thumb = await downloadFile(photoFormat[0]["media_url_https"])
                        if not name:
                            name = thumb
                    username = userInfo["screen_name"]
                    sender_url = "https://twitter.com/" + username
                    TWEET_LINK = f"{sender_url}/status/{legacyInfo['id_str']}"

                    text = self.format_tweet(
                        SENDER=userInfo["name"],
                        SENDER_USERNAME="@" + username,
                        TWEET_TEXT=text,
                        TWEET_LINK=TWEET_LINK,
                        # REPLY_TAG=(
                        #     ""
                        #     if not repta
                        #     else Var.REPLIED_NOTE.format(REPLY_URL=repta)
                        # ),
                        SENDER_PROFILE=sender_url,
                        SENDER_PROFILE_IMG_URL=userInfo["profile_image_url_https"],
                        _REPO_LINK=REPO_LINK,
                        HASHTAGS=hashtags,
                        BOT_USERNAME=Client.SELF.username,
                    )
                    await self.sendToChats(text, name)
                    if name:
                        os.remove(name)
                except Exception as er:
                    LOGS.exception(er)
            await asyncio.sleep(Var.WAIT_DELAY)
                    


sched = AsyncIOScheduler()
streamer = TgTwitterStreamer()

sched.add_job(streamer.fetchNewTweets, "interval", minutes=Var.DELAY_MINUTES)
sched.start()

if __name__ == "__main__":
    Client.run_until_disconnected()
