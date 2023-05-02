# Telegram - Twitter - Bot
# Github.com/New-dev0/TgTwitterStreamer
# GNU General Public License v3.0

import re
from telethon.tl.custom import Button
from . import LOGGER, REPO_LINK, TRACK_WORDS, TRACK_USERS

from .tstreamer import TgStreamer, Var, Client
from tweepy.asynchronous.streaming import StreamRule
from telethon.events import NewMessage, CallbackQuery


async def start_message(event):
    await event.reply(
        Var.START_MESSAGE,
        file=Var.START_MEDIA,
        buttons=[
            [Button.inline("Hello Sir, i'm Alive", data="ok")],
            [
                Button.url(
                    "Source",
                    url=REPO_LINK,
                ),
                Button.url("Support Group", url="t.me/FutureCodesChat"),
            ],
        ],
    )


async def callback_query(event):
    await event.answer("I'm Alive , No Need to click button..")


# For people, deploying multiple apps on one bot.

if not Var.DISABLE_START:
    Client.add_event_handler(start_message, NewMessage(pattern="^/start$"))
    Client.add_event_handler(callback_query, CallbackQuery(data=re.compile("ok")))


def make_rules() -> str:
    rule = ""
    if not Var.TAKE_RETWEETS:
        rule += "-is:retweet"
    if not Var.TAKE_REPLIES:
        rule += " -is:reply"
    if Var.MEDIA_ONLY:
        rule += " has:media"
    if TRACK_USERS:
        if len(TRACK_USERS) == 1:
            rule += f" from:{TRACK_USERS[0]}"
        else:
            rule += " (" + " OR ".join(f"from:{user}" for user in TRACK_USERS) + ")"
    if TRACK_WORDS:
        rule += " (" + " OR ".join(TRACK_WORDS) + ")"
    if Var.EXCLUDE:
        rule += " -".join(Var.EXCLUDE)
    if Var.LANGUAGES:
        rule += " (" + " OR ".join(f"lang:{lang}" for lang in Var.LANGUAGES) + ")"
    return rule.strip()


if __name__ == "__main__":
    Stream = TgStreamer(bearer_token=Var.BEARER_TOKEN, wait_on_rate_limit=True)

    async def run():
        rule = make_rules()
        add_rule = True
        old_rules = (await Stream.get_rules()).data

        if old_rules:
            LOGGER.debug("old rules: " + str(old_rules))
            del_ids = []
            for _rule in old_rules:
                if _rule.value != rule:
                    del_ids.append(_rule.id)
                else:
                    add_rule = False
            if del_ids:
                await Stream.delete_rules(del_ids)
        if add_rule:
            LOGGER.debug(f"Applying rule: {rule}")
            rules = (await Stream.add_rules(StreamRule(rule))).data
        else:
            rules = old_rules

        if rules:
            Stream.rule_ids = [rule.id for rule in rules]

        LOGGER.debug(f"filtering rules: {Stream.rule_ids}")

        _MAX_RECONNECT = Var.MAX_RECONNECT  # default: 20
        _RECONNECT_COUNT = 0

        while True:
            if Stream.task:
                _RECONNECT_COUNT += 1
                if _RECONNECT_COUNT > _MAX_RECONNECT:
                    break
                LOGGER.info(f"Reconnecting [{_RECONNECT_COUNT}]..")
            try:
                Stream.start()
                await Stream.task
            except (KeyboardInterrupt):
                break
            except Exception as er:
                LOGGER.exception(er)

    Client.loop.run_until_complete(run())

#    with Client:
#        Client.run_until_disconnected()  # RUN CLIENT
