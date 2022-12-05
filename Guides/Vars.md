## - Mandatory Var

### - Twitter Vars 
- Below Vars can be taken from [developers.twitter.com](https://developers.twitter.com)

### Mandatory
```
-    BEARER_TOKEN
```
#### Optional [Required only, if AUTO_RETWEET or AUTO_LIKE]
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
- ` - MEDIA_ONLY - Only include tweets containing media.`
- ` - CUSTOM_TEXT - Custom Tweet Format` - [Click Here for Detailed Info](./formatting.md)
- ` - REPLY_FORMAT - format of REPLY_TAG (If tweet is in reply to some post.) (can contain REPLY_URL in it)`
- ` - BUTTON_TITLE - text to show on Button`
- ` - DISABLE_BUTTON - Disable the button attached to the posts. Fill True/False`
- ` - CUSTOM_BUTTON - Custom Url button to attach to Post.`
- ` - LANGUAGES - list of languages, in which tweet should be return. (eg - 'en ru') (default- en)`
    `(set to 'None' to disable language filter.)`
- ` - DISABLE_START - Disable '/start' message.`
- ` - MUST_INCLUDE - word which should be included in Tweet Text.`
- ` - EXCLUDE - word which should be excluded in Tweet Text.`


### CUSTOM_BUTTON
- Button text and url are seperated by "-"
- Two or more Buttons are seperated by "|"
- Use "||" to seperate Button rows.

-   #### Example
-
    - `Button-https://google.com || Button2-https://telegram.org
    `
    - It will create a 2 buttons one below another.
- 
    - `Button-https://google.com | Button2-https://telegram.org || Button-https://google.com | Button2-https://telegram.org`

    - It will create 2 rows, and 2 same button in each.