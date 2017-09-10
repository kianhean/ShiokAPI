from urllib.request import urlopen
from bs4 import BeautifulSoup
import json


def bann(code):
    """ If banned return True else False """
    ban_list = ['First Ride', 'New Customers', 'From SMU', 'From NTU',
                'From NUS', 'From SUTD', 'From SIM', 'First GrabHitch', 'New GrabPay',
                'First 2 Rides', 'First 4 Rides']

    for word in ban_list:
        if code.find(word) > 0:
            return True
    return False


def get_promos(url: str):
    """ Connect to Paged Promo Codes return a Dictionary of Promo Codes

    Parameters
    ----------
    url : string
        Url to scrape. Example https://www.couponese.com/store/uber.com/

    """
    # Connect to Source
    data = urlopen(url)
    soup = BeautifulSoup(data, 'html.parser')

    # Find latest Result
    loop = soup.findAll("article", {"class" : "ov-coupon"})
    output = {}

    if len(loop) >0:

        for square in loop:

            try:
                country = square.findAll("div")[1].findAll("img")[0]['title']
            except:
                country = 'Singapore'

            try:
                square.findAll("span", {"class" : "ov-expired"})[0]
                expired = True
            except:
                expired = False

            if country == 'Singapore' and expired is False:

                code = square.findAll("div")[2].findAll("strong")[0].text
                desc = square.findAll("div")[3].findAll("div", {"class" : "ov-desc"})[0].text
                expiry = square.findAll("div")[3].findAll("div",
                                                          {"class" : "ov-expiry"})[0].text[1:]

                if bann(desc) is False:
                    output[code] = [expiry, desc]
        return output

    else:

        return ''


def promo_loop(promo_list: str):
    """ Compose Message For Promo Codes as a string

    Parameters
    ----------
    promo_list : string
        promo_list to scrape in a dict as a string. Example {"uber":"https://www.couponese.com/store/uber.com/"}
    """

    final = ''

    # Convert string of Json to dict
    promo_list = json.loads(promo_list)

    # Create Generic Message
    for key in promo_list.keys():
        final += key + ", "
    output = '<b>Checking ' + final[:-2] + ' for Promos!</b>\n'

    # Loop thru Websites to Check
    for key, value in promo_list.items():

        result = get_promos(value)

        # If there are promo codes
        if len(result) > 0:
            output += '\n<b>' + key + '</b>\n\n'

            # Loop thru Promo Codes
            for promo_code, text in result.items():
                output += '<b>' + promo_code + '</b> | Expires - ' + text[0] + ' | ' + \
                          text[1] + '\n'

    return output
