"""api.py: Getting and displaying gov data"""

from __future__ import unicode_literals
from datetime import datetime
from datetime import timedelta
import json
import requests

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


def weather_get():
    """ Get Latest Weather Map From @SGWeatherToday """
    username = "@SGWeatherToday"
    auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(access_token, access_token_secret)

    result = tweepy.API(auth).user_timeline(username, count=15)
    final = []

    for tweet in result:
        if 'Weather Radar Update' in tweet.text and 'media' in tweet.entities:
            final.append(tweet.entities['media'][0]['media_url_https'])

    return final[0]

def weather_nea():
    """ Get Weather Forecast from @NEAsg
    If date posted == Todays date

    """
    username = "@NEAsg"
    auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(access_token, access_token_secret)

    result = tweepy.API(auth).user_timeline(username, count=20)
    final = []

    for tweet in result:
        posted_time = tweet.created_at + timedelta(hours=8)
        if 'Issued' in tweet.text and posted_time.date() == datetime.today().date():
            final.append(tweet.text)

    return final[0]


def weather_warning_get():
    """ Get Weather Warning from @SGWeatherToday
    If date posted == Todays date

    """
    username = "@PUBsingapore"
    auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(access_token, access_token_secret)

    result = tweepy.API(auth).user_timeline(username, count=30)
    final = []

    for tweet in result:
        posted_time = tweet.created_at + timedelta(hours=8)
        if 'NEA:' in tweet.text and '#sgflood' in tweet.text and posted_time.date() == datetime.today().date():
            final.append(tweet.text)

    if len(final) == 0:
        return "No Warnings!"
    else:
        text_ = "<b>Heavy Rain Warning</b>\n"
        final_text = ""
        for _ in final:
            _date = _.split('Issued')[1].replace("hours.", "").replace(":", "") + "H"
            _ = _.split('Issued')[0]
            _ = _.replace('NEA', '[NEA@' + _date.replace(" ", "") + ']')
            final_text += _.split('Issued')[0] + "\n"
        return text_ + final_text.replace("#sgflood", "")


def connnect_gov_api(url_string):
    """ Conntect to Gov and return request object """

    govt_key = config['development']['gov_api']

    # Get Data
    headers = {'api-key': govt_key}
    request = requests.get(url_string, headers=headers)

    return request


def psi3hour_get():
    """ Get Latest Singapore PSI """

    connnect_gov_api_r = connnect_gov_api('https://api.data.gov.sg/v1/environment/psi')
    data = json.loads(connnect_gov_api_r.text)

    # Load data into Dictionary and get reading
    hourly = data['items'][0]['readings']['psi_twenty_four_hourly']
    timestampp = data['items'][0]['timestamp'][:19].replace("T", " ")

    # Create Response
    final_string = "<b>The 24 hourly PSI Reading at " + timestampp + " is actually</b> \n\n"

    for key in sorted(hourly):
        final_string = final_string + (str(key) + " " + \
                                        str(hourly[key]) + "\n")
    return final_string + "\nHotspots at our neighbours there are like that!"


def weathernow_get():
    """ Get Latest Singapore Weather """

    connnect_gov_api_r = connnect_gov_api(
        'https://api.data.gov.sg/v1/environment/24-hour-weather-forecast')
    data = json.loads(connnect_gov_api_r.text)

    # Load data into Dictionary and get reading
    #forecast = data['items'][0]['general']['forecast']
    forecast = weather_nea()
    high_ = data['items'][0]['general']['temperature']['high']
    low_ = data['items'][0]['general']['temperature']['low']

    # Create Response
    final_string = forecast + \
                    " Temperatures are expected to range from a high of " + str(high_) + \
                    "°C to a low of " + str(low_) + "°C\n\n<b>Forecast Next 12 Hrs</b>\n\n"

    # Add 12 hr cast
    nowcast = data['items'][0]['periods'][0]['regions']
    for key in sorted(nowcast):
        final_string = final_string + (str(key) + \
                                        " - " + str(nowcast[key]) + "\n")
    final_string = final_string + "\n<b>Forecast Tomorrow</b>\n\n"

    # Add 24 hr cast
    nowcast = data['items'][0]['periods'][1]['regions']
    for key in sorted(nowcast):
        final_string = final_string + (str(key) + " - " + str(nowcast[key]) + "\n")

    return final_string + "\nShow you radarrrr somemore! Got colour means raining!"
