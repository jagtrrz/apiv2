"""
Headers mixin
"""

import re
from datetime import datetime, tzinfo, timedelta
from django.utils import timezone

def get_utc():
    date = timezone.now()
    return date.tzinfo

UTC = get_utc()

class DatetimeMixin():
    """Headers mixin"""
    def datetime_now(*args, **kwargs):
        return timezone.now()


    def datetime_to_iso(self, date=datetime.utcnow()) -> str:
        return re.sub(
            r'\+00:00$', 'Z',
            date.replace(tzinfo=UTC).isoformat()
        )

    def datetime_to_ical(self, date=datetime.utcnow()) -> str:
        return '{:4d}{:02d}{:02d}T{:02d}{:02d}{:02d}Z'.format(
            date.year, date.month, date.day, date.hour, date.minute,
            date.second)

    def assertDatetime(self, date):
        if not isinstance(date, str):
            self.assertTrue(isinstance(date, datetime))
            return True

        try:
            string = re.sub(r'Z$', '', date)
            datetime.fromisoformat(string)
            self.assertTrue(True)
            return True
        except Exception:
            self.assertTrue(False)

    # def iso_to_datetime(self, string):
    #     string = re.sub(r'Z$', '', string)
    #     date = datetime.fromisoformat(string)
    #     date = date.astimezone(tz=UTC)

    #     return date
