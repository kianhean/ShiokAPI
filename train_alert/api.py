"""api.py: Getting and displaying train breakdowns"""

from __future__ import unicode_literals
from datetime import timedelta
import configparser
import tweepy

# Set Keys from Config
config = configparser.ConfigParser()
config.sections()
config.read('./enviroment.ini')

consumer_key = config['development']['consumer_key_twitter']
consumer_secret = config['development']['consumer_secret_twitter']
access_token = config['development']['access_token_twitter']
access_token_secret = config['development']['access_token_secret_twitter']


def connect_twitter_api(provider='@SMRT_Singapore'):
    """ Connect to Twitter API and Get Result """

    auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(access_token, access_token_secret)

    api = tweepy.API(auth)

    final = {}

    # Get latest 20 tweets from SMRT_SINGAPORE
    result = api.user_timeline(provider, count=5)

    return result


def get_breakdowns(provider='@SMRT_Singapore'):
    """ Parse Breakdowns """

    result = connect_twitter_api(provider)

    final = {}

    for tweet in result:

        # Only record the breakdowns/update
        if provider == '@SMRT_Singapore':
            detect = '[EWL' in tweet.text or '[NSL' in tweet.text or '[CCL' in tweet.text
        else:
            detect = 'SORRY' in tweet.text.upper() and ('NEL' in tweet.text.upper() or 'DTL' in tweet.text.upper())

        if detect:
            output = {}
            created_at = (tweet.created_at + timedelta(hours=8)).strftime('%Y %b %d, at %I %M %S %p')
            output[tweet.id_str] = {'tweet':tweet.text,
                                    'created_at':created_at}
            final.update(output)

    return final


def all_breakdowns():
    """ all breakdowns """
    final = {}
    final.update(get_breakdowns('@SMRT_Singapore'))
    final.update(get_breakdowns('@SBSTransit_Ltd'))
    return final
