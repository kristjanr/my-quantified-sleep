import datetime

import pytz

tallinn = pytz.timezone('Europe/Tallinn')


class Night:
    def __init__(self,
                 bed_time: datetime.datetime,
                 wake_time: datetime.datetime,
                 wake_date: datetime.date,
                 deep_duration: datetime.timedelta,
                 light_duration: datetime.timedelta,
                 total_duration: datetime.timedelta,
                 awake_duration: datetime.timedelta,
                 ):
        self.bed_time = bed_time.astimezone(tallinn)
        self.wake_time = wake_time.astimezone(tallinn)
        self.wake_date = wake_date
        self.deep_duration = deep_duration
        self.light_duration = light_duration
        self.total_duration = total_duration
        self.awake_duration = awake_duration

    def __str__(self):
        return self.bed_time.strftime('%H:%M %a, %d-%b-%Y') \
               + ' - ' \
               + self.wake_time.strftime('%H:%M %a, %d-%b-%Y')

    def __repr__(self):
        return self.wake_date.isoformat()
