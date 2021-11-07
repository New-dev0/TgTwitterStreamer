## - Mandatory Var

### - Twitter Vars 
- Below Vars can be taken from [developers.twitter.com](https://developers.twitter.com)

```
-    CONSUMER_KEY
-    CONSUMER_SECRET
-    ACCESS_TOKEN
-    ACCESS_TOKEN_SECRET
```
```
 -   TRACK_USERS - Username of Twitter Users to Track (User to Take Tweets from)
 ```

### - Telegram Vars
```
- API_ID
- API_HASH
These Two Vars can be Taken from my.telegram.org
```

```
- BOT_TOKEN - Telegram Bot token, get it from @botfather.
```
```
- TO_CHAT - Chat id where to send Tweets...
```


#### Note : `TO_CHAT` and `TRACK_USERS` can be Sepeated by space for Multiple Chat/User....


## - Optional Var
- ` - TRACK_WORDS - Track word overall on Twitter, overlapping 'TRACK_USERS' Var. (eg - 'hello | bye | another word')`

- ` - TAKE_REPLIES - to Take Tweets Which are reply to User. Fill (True/False).`
- ` - TAKE_RETWEETS - To Take Tweets, which are Retweets, done by User. Fill (True/False)`
- ` - TAKE_OTHERS_REPLY - To Take reply on posts of user filled in 'TRACK_USERS'. Fill (True/False)`
- ` - CUSTOM_TEXT - Custom Tweet Format` - [Click Here to Detailed Info](./formatting.md)
- ` - BUTTON_TITLE - text to show on Button`
- ` - DISABLE_BUTTON - Disable the button attached to the posts. Fill True/False`
- ` - FILTER_LEVEL - Level on which number of tweets to get and set depends. Fill 'low' or 'medium'.`
- ` - LANGUAGES - list of languages, in which tweet should be return. (eg - 'en ru')`
- ` - DISABLE_START - Disable '/start' message.`
- ` - MUST_INCLUDE - word which should be included in Tweet Text.`
- ` - MUST_EXCLUDE - word which should be excluded in Tweet Text.`