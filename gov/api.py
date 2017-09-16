"""api.py: Getting and displaying gov data"""

from __future__ import unicode_literals
import configparser
import json
import requests


def connnect_gov_api(url_string):
    """ Conntect to Gov and return request object """

    # Set Keys from Config
    config = configparser.ConfigParser()
    config.sections()
    config.read('./enviroment.ini')

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
    forecast = data['items'][0]['general']['forecast']
    high_ = data['items'][0]['general']['temperature']['high']
    low_ = data['items'][0]['general']['temperature']['low']

    # Create Response
    final_string = "In General the weather will be looking like " + forecast + \
                    " with a high of " + str(high_) + \
                    "°C and a low of " + str(low_) + "°C\n\n<b>Forecast Next 12 Hrs</b>\n\n"

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
