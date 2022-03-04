# Telegram - Twitter - Bot
# Github.com/New-dev0/TgTwitterStreamer
# GNU General Public License v3.0

import os
import asyncio
from aiohttp import ClientSession

from html import unescape
from telethon.tl.custom import Button, Message
from telethon.errors.rpcerrorlist import (
    FloodWaitError,
    WebpageCurlFailedError,
    MediaInvalidError,
)
from tweepy.asynchronous import AsyncStream
from . import (
    Twitter,
    Client,
    REPO_LINK,
    Var,
    LOGGER,
    CUSTOM_BUTTONS,
    TRACK_IDS,
    CUSTOM_FORMAT,
)
from .functions import download_from_url


class TgStreamer(AsyncStream):
    async def on_connect(self):
        LOGGER.info("<<<---||| Stream Connected |||--->>>")

    def get_urls(self, medias):
        if not medias:
            return []

        List = []

        for media in medias:
            if media.get("video_info") and media["video_info"].get("variants"):
                link = media["video_info"]["variants"][0]["url"]
            elif media["type"] == "photo":
                link = media["media_url_https"]
            else:
                link = None
            if link and "tweet_video_thumb" not in link:
                List.append(link)
        return List

    def _favorite(self, id_: str):
        try:
            Twitter.create_favorite(id_)
        except Exception as er:
            LOGGER.info("Error while creating a tweet as favorite.")
            LOGGER.exception(er)

    def _do_retweet(self, id_: str):
        try:
            Twitter.retweet(id=id_)
        except Exception as er:
            LOGGER.info("ERROR while Retweeting a Tweet.")
            LOGGER.exception(er)

    async def _pin(self, msg: Message):
        try:
            await msg.pin()
        except FloodWaitError as fw:
            LOGGER.info("Flood wait error while auto pin!")
            LOGGER.exception(fw)
            await asyncio.sleep(fw.seconds + 10)
        except Exception as er:
            LOGGER.info(f"Error while pin: {er}")

    async def on_status(self, status):
        tweet = status._json
        user = tweet["user"]
        # LOGGER.info(tweet)

        if (
            not Var.TRACK_WORDS
            and Var.TRACK_USERS
            and not Var.TAKE_OTHERS_REPLY
            and not user["id_str"] in TRACK_IDS
        ):
            return

        if not Var.TAKE_REPLIES and tweet["in_reply_to_status_id"]:
            return

        if not Var.TAKE_RETWEETS and tweet.get("retweeted_status"):
            return

        pic, content, hashtags = [], "", ""
        _entities = tweet.get("entities", {})
        entities = _entities.get("media", [])
        extended_entities = tweet.get("extended_entities", {}).get("media")
        extended_tweet = (
            tweet.get("extended_tweet", {}).get("entities", {}).get("media")
        )
        all_urls = set()
        for media in (entities, extended_entities, extended_tweet):
            urls = self.get_urls(media)
            all_urls.update(set(urls))
        for pik in all_urls:
            pic.append(pik)
        if _entities and _entities.get("hashtags"):
            hashtags = "".join(f"#{a['text']} " for a in _entities["hashtags"])
        content = tweet.get("extended_tweet", {}).get("full_text")

        username = user["screen_name"]
        sender_url = "https://twitter.com/" + username
        TWEET_LINK = f"{sender_url}/status/{tweet['id']}"

        if content and (len(content) < 1000):
            text = content
        else:
            text = tweet["text"]

        # Clear unexpected tags with html.unescape()
        text = unescape(text)

        if Var.MUST_INCLUDE and Var.MUST_INCLUDE.lower() not in text.lower():
            return

        if Var.MUST_EXCLUDE and Var.MUST_EXCLUDE.lower() in text.lower():
            return

        spli = text.split()
        async with ClientSession() as ses:
            for on in spli:
                # replace t.co urls
                if on.startswith("https://t.co/"):
                    async with ses.get(on) as out:
                        text = text.replace(on, str(out.url))

        # Twitter Repeats Media Url in Text.
        # So, Its somewhere necessary to seperate out links.
        # to Get Pure Text.

        if pic:
            for word in text.split():
                if word.startswith("https://twitter.com"):
                    spli_ = word.split("/")
                    if len(spli_) >= 2 and spli_[-2] in ["photo", "video"]:
                        text = text.replace(word, "")

        try:
            text = Var.CUSTOM_TEXT.format(
                SENDER=user["name"],
                SENDER_USERNAME="@" + username,
                TWEET_TEXT=text,
                TWEET_LINK=TWEET_LINK,
                SENDER_PROFILE=sender_url,
                SENDER_PROFILE_IMG_URL=user["profile_image_url_https"],
                _REPO_LINK=REPO_LINK,
                HASHTAGS=hashtags,
                BOT_USERNAME=Client.SELF.username,
            )
        except KeyError:
            LOGGER.error("Your 'CUSTOM_TEXT' seems to be wrong!\nPlease Correct It!")
            Var.CUSTOM_TEXT = CUSTOM_FORMAT
            Client.parse_mode = "html"
            text = CUSTOM_FORMAT.format(
                SENDER=user["name"],
                SENDER_USERNAME="@" + username,
                TWEET_TEXT=text,
                TWEET_LINK=TWEET_LINK,
                SENDER_PROFILE=sender_url,
                SENDER_PROFILE_IMG_URL=user["profile_image_url_https"],
                _REPO_LINK=REPO_LINK,
                HASHTAGS=hashtags,
                BOT_USERNAME=Client.SELF.username,
            )
        if pic == []:
            pic = None

        button, MSG = None, None

        if CUSTOM_BUTTONS:
            button = CUSTOM_BUTTONS

        elif not Var.DISABLE_BUTTON:
            button = Button.url(text=Var.BUTTON_TITLE, url=TWEET_LINK)

        is_pic_alone = bool(not pic or len(pic) == 1)
        _photos = pic[0] if (pic and is_pic_alone) else pic
        if _photos == []:
            _photos = None
        for chat in Var.TO_CHAT:
            try:
                MSG = await Client.send_message(
                    chat,
                    text if (is_pic_alone or Var.DISABLE_BUTTON) else None,
                    link_preview=False,
                    file=_photos,
                    buttons=button,
                )
                msg_id = MSG[0].id if isinstance(MSG, list) else MSG.id
                if not is_pic_alone and text and button:
                    await Client.send_message(
                        chat, text, reply_to=msg_id, link_preview=False, buttons=button
                    )
            except (WebpageCurlFailedError, MediaInvalidError) as er:
                LOGGER.info(f"Handling <{er}>")
                try:
                    _photos = await download_from_url(_photos)
                    MSG = await Client.send_message(
                        chat,
                        text if (is_pic_alone or Var.DISABLE_BUTTON) else None,
                        link_preview=False,
                        file=_photos,
                        buttons=button,
                    )
                    msg_id = MSG[0].id if isinstance(MSG, list) else MSG.id
                    if not is_pic_alone and text and button:
                        await Client.send_message(
                            chat,
                            text,
                            reply_to=msg_id,
                            link_preview=False,
                            buttons=button,
                        )

                    for path in _photos:
                        os.remove(path)

                except Exception as er:
                    LOGGER.exception(er)
            except FloodWaitError as fw:
                LOGGER.exception(fw)
                await asyncio.sleep(fw.seconds + 10)
            except Exception as er:
                LOGGER.exception(er)

        if Var.AUTO_LIKE:
            self._favorite(tweet["id"])

        if Var.AUTO_RETWEET:
            self._do_retweet(tweet["id"])

        if Var.AUTO_PIN and MSG:
            single_msg = MSG if not isinstance(MSG, list) else MSG[0]
            await self._pin(single_msg)

    async def on_request_error(self, status_code):
        LOGGER.error(f"Stream Encountered HTTP Error: {status_code}")
        if status_code == 420:
            # Tweepy already makes Connection sleep for 1 minute on 420 Error.
            # So, Here making it sleep for more 10 seconds.
            await asyncio.sleep(10)
        LOGGER.info(
            "Refer https://developer.twitter.com/ja/docs/basics"
            + "/response-codes to know about error code."
        )

    async def on_connection_error(self):
        LOGGER.info("<<---|| Connection Error ||--->>")
