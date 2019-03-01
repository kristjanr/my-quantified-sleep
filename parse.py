import datetime

import brotli
import json
import pytz
import requests

from night import Night
from secrets import garmin_connect_request_headers
from spreadsheet import add_rows_to_sleep_tab


# plan:
# 1) check if the awake time is received via request - done and added
# 2) check if an api exists. somehow, tapiriik is doing it! - sent an email to get access
# 3) data to google spreadsheet - done
# TODO:
# 4) proper formatting in sheet
# 5) delete this env and recreate an isolated env, install and document dependencies - pyenv!
# 6) automate fully via heroku? First just create a job to run once a day, every morning and see if it works.
# 7) Refactor - create proper classes and a main file that could be run from command line
# which takes start and end date  and cookie as input
# Later, take care about authentication (Garming connect website cookie expiring).

def download(start_date, end_date):
    headers = {
        'cookie': '',
        'referer': '',
        'accept-encoding': 'gzip, deflate, br',
        'accept-language': 'en-SG,en;q=0.9,et-EE;q=0.8,et;q=0.7,ru-RU;q=0.6,ru;q=0.5,en-US;q=0.4',
        'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/72.0.3626.119 Safari/537.36',
        'nk': 'NT',
        'accept': 'application/json, text/javascript, */*; q=0.01',
        'authority': 'connect.garmin.com',
        'x-requested-with': 'XMLHttpRequest',
        'x-app-ver': '4.15.2.0',
        'x-lang': 'en-US',
    }
    secret_headers = garmin_connect_request_headers()
    headers['cookie'] = secret_headers['cookie']
    headers['referer'] = secret_headers['referer']

    params = (
        ('startDate', start_date),
        ('endDate', end_date),
        ('_', '1551416560723'),
    )

    response = requests.get('https://connect.garmin.com/modern/proxy/wellness-service/wellness/dailySleepsByDate',
                            headers=headers, params=params)
    if response.status_code != 200:
        print('Status code: %d' % response.status_code)
        print('Content: %s' % brotli.decompress(response.content))
        raise Exception
    return response


def download_to_json(start_date, end_date):
    response = download(start_date, end_date)
    decompressed = brotli.decompress(response.content)
    return json.loads(decompressed)


def download_to_file():
    data = download_to_json()
    with open('data.json', 'w') as fp:
        json.dump(data, fp)


def load_data():
    with open('data.json') as fp:
        return json.load(fp)


def converter(data):
    nights = []
    for d in data:
        bed_time = datetime.datetime.fromtimestamp(d['sleepStartTimestampGMT'] / 1000, pytz.utc)
        wake_time = datetime.datetime.fromtimestamp(d['sleepEndTimestampGMT'] / 1000, pytz.utc)
        wakeup_date = datetime.date(*[int(datepart) for datepart in d['calendarDate'].split('-')])
        deep_duration = datetime.timedelta(seconds=d['deepSleepSeconds'])
        light_duration = datetime.timedelta(seconds=d['lightSleepSeconds'])
        total_duration = datetime.timedelta(seconds=d['sleepTimeSeconds'])
        awake_duration = datetime.timedelta(seconds=d['awakeSleepSeconds'])
        night = Night(bed_time, wake_time, wakeup_date, deep_duration, light_duration, total_duration, awake_duration)
        nights.append(night)
    return nights


def send_to_google(start_date, end_date):
    data = download_to_json(start_date, end_date)
    rows = []
    for n in converter(data):
        rows.append(
            [
                str(n.wake_date),
                str(n.bed_time),
                str(n.wake_time),
                str(n.deep_duration),
                str(n.light_duration),
                str(n.awake_duration),
                str(n.total_duration)
            ])
    print(rows)
    add_rows_to_sleep_tab(rows)


start_date = '2019-02-07'
end_date = '2019-03-01'
send_to_google(start_date, end_date)
