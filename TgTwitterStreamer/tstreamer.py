# Telegram - Twitter - Bot
# Github.com/New-dev0/TgTwitterStreamer
# GNU General Public License v3.0


import os
import asyncio

from html import unescape
from telethon.tl.custom import Button, Message
from telethon.errors.rpcerrorlist import (
    FloodWaitError,
    WebpageCurlFailedError,
    MediaInvalidError,
)
from tweepy.asynchronous import AsyncStreamingClient
from . import (
    Twitter,
    Client,
    REPO_LINK,
    Var,
    LOGGER,
    CUSTOM_BUTTONS,
    CUSTOM_FORMAT,
)
from .functions import download_from_url


class TgStreamer(AsyncStreamingClient):
    async def on_connect(self):
        LOGGER.info("<<<---||| Stream Connected |||--->>>")

    def get_urls(self, medias):
        if not medias:
            return []
        List = []
        for media in medias:
            if media.data.get("variants"):
                link = media.data["variants"][0]["url"]
            else:
                link = media.url or media.preview_image_url
            if link and not "tweet_video_thumb" in link:
                List.append(link)
        return List

    async def _favorite(self, id_: str):
        try:
            await Twitter.create_favorite(id_)
        except Exception as er:
            LOGGER.info("Error while creating a tweet as favorite.")
            LOGGER.exception(er)

    async def _do_retweet(self, id_: str):
        try:
            await Twitter.retweet(id=id_)
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

    def format_tweet(*args, **kwargs):
        try:
            return Var.CUSTOM_TEXT.format(**kwargs)
        except KeyError:
            LOGGER.error("Your 'CUSTOM_TEXT' seems to be wrong!\nPlease Correct It!")
            Var.CUSTOM_TEXT = CUSTOM_FORMAT
            Client.parse_mode = "html"
            return CUSTOM_FORMAT.format(**kwargs)

    async def on_response(self, response):
        try:
            await self._on_response(response)
        except Exception as er:
            LOGGER.exception(er)

    async def _on_response(self, response):
        include = response.includes
        tweet = response.data
        user = include.get("users", [])[0]

        if not Var.TAKE_REPLIES and tweet.in_reply_to_user_id:
            return

        pic = self.get_urls(include.get("media"))
        hashtags = None
        _entities = tweet.get("entities", {})
        if _entities and _entities.get("hashtags"):
            hashtags = " ".join(f"#{a['tag']}" for a in _entities["hashtags"])

        username = user["username"]
        sender_url = "https://twitter.com/" + username
        TWEET_LINK = f"{sender_url}/status/{tweet['id']}"

        text = tweet["text"]

        # Clear unexpected tags with html.unescape()
        text = unescape(text)
        for url in _entities.get("urls", []):
            if url["expanded_url"].startswith("https://twitter.com/") and url[
                "expanded_url"
            ].split("/")[-2] in ["photo", "video"]:
                replace = ""
            else:
                replace = url["expanded_url"]
            text = text.replace(url["url"], replace)

        # Twitter Repeats Media Url in Text.
        # So, Its somewhere necessary to seperate out links.
        # to Get Pure Text.

        if not (text or pic):
            return

        text = self.format_tweet(
            SENDER=user["name"],
            SENDER_USERNAME="@" + username,
            TWEET_TEXT=text,
            TWEET_LINK=TWEET_LINK,
            SENDER_PROFILE=sender_url,
            SENDER_PROFILE_IMG_URL=user["profile_image_url"],
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
            await self._favorite(tweet["id"])

        if Var.AUTO_RETWEET:
            await self._do_retweet(tweet["id"])

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
