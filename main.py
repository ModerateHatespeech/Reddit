"""
Toxicity Content Bot Script by ModerateHatespeech.com
@description Scans subreddit(s) for content that is considered toxic and reports the comment to moderators
@version 1.0.0
@last_updated 2/13/2022
"""

import praw
import requests
import json
import traceback
import logging
import re

logging.basicConfig(filename='report.log', format='%(asctime)s - %(message)s', level=logging.INFO) # action log

def load_config():
  """ Load configuration file """
  with open("config.json", "r") as f:
    config = json.load(f)
    missing = ["client_id", "client_secret", "subreddit", "api_token","username", "password","threshold"] - config.keys()
    if len(missing) > 0:
      raise KeyError("Missing keys in config.json {0}".format(str(missing)))
    return config

def login(config):
  """ Login to Reddit """
  reddit = praw.Reddit(
      user_agent = "ToxicContentBot (by u/toxicitymodbot)",
      client_id = config['client_id'],
      client_secret = config['client_secret'],
      password = config['password'],
      username = config['username']
  )
  return reddit

def moderate(text, thresh):
  """ Call API and return response list with boolean & confidence score """
  text = re.sub(r'>[^\n]+', "", text) # strip out quotes
  response = requests.post("https://api.moderatehatespeech.com/api/v1/moderate/", json={"token":config['api_token'], "text":text}).json()

  if response['response'] != "Success":
    if response['response'] != "Authentication failure":
      raise AttributeError('Invalid response: {0}'.format(response['response']))
    else:
      raise RuntimeError('Fatal response: {0}'.format(response['response']))

  if response['class'] == "flag" and float(response['confidence']) > thresh:
    return [True, round(float(response['confidence']), 3)]

  return [False, round(float(response['confidence']), 3)]

if __name__ == "__main__":
  config = load_config()
  reddit = login(config)
  subreddit = reddit.subreddit(config['subreddit'])

  for comment in subreddit.stream.comments():
    try:
      result = moderate(comment.body, config['threshold'])
      if result[0]:
        logging.info('Comment ({0}) reported @ {1}% confidence'.format(comment.permalink, result[1] * 100))
        comment.report("Automatic report from u/{0} for toxicity @ {1}% confidence".format(config['username'], result[1] * 100))
    except (AttributeError, KeyError):
      logging.warning(traceback.format_exc())
      traceback.print_exc()
