# Reddit
Automatically moderate subreddits via API

## Purpose
The following python script create a Reddit bot that will auto-report content flagged as "Toxic" by our API to the subreddit's moderators.

## Requirements
Install requirements:
```apt-get install python3
pip3 install praw requests
```

Required config.json file:
```json
{
  "subreddit": "subreddit",
  "client_id": "REDDIT_APPLICATION_CLIENT_ID",
  "client_secret": "REDDIT_APPLICATION_CLIENT_SECRET",
  "username": "REDDIT_BOT_ACCOUNT_USERNAME",
  "password": "REDDIT_BOT_ACCOUNT_PASSWORD",
  "api_token": "MODERATE_HATESPEECH_API_TOKEN",
  "threshold": 1
}
```

The subreddit(s) to scan can be passed as a list of subreddits joined with a "+" -- for example, "reddit+politics+news." An example config file is provided below:
```json
{
  "subreddit": "news+worldnews",
  "client_id": "G23Ap9HxVzZGW9cvH68a",
  "client_secret": "q-MScVnSE5i4UfnMucGZZs3avyX",
  "username": "toxicitymodbot",
  "password": "jH^cFU%V%Pf7&MMPA",
  "api_token": "f7835af37818e44fa22b5393e3330811",
  "threshold": 0.9
}
```

