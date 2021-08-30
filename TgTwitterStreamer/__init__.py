# Telegram - Twitter - Bot
# Github.com/New-dev0/TgTwitterStreamer
# GNU General Public License v3.0


from Configs import Var

REPO_LINK = "https://github.com/New-dev0/TgTwitterStreamer"


CUSTOM_FORMAT = """:🎊 **[{SENDER}]({SENDER_PROFILE}) :**

🍿 {TWEET_TEXT}

• Powered by **[TgTwitterStreamer]({_REPO_LINK})**"""


if not Var.CUSTOM_TEXT:
    Var.CUSTOM_TEXT = CUSTOM_FORMAT