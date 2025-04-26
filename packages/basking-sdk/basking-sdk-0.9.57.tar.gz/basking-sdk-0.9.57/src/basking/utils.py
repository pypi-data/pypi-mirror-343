import logging
from typing import Union
from datetime import datetime, date, time
from functools import wraps, partial

from dateutil.tz import gettz, tzutc


class DateError(TypeError):
    """Only date objects are supported"""


class Utils:
    def __init__(self, basking_obj):
        self.basking = basking_obj
        self.log = logging.getLogger(self.__class__.__name__)
        basking_log_level = logging.getLogger(self.basking.__class__.__name__).level
        self.log.setLevel(basking_log_level)

    @staticmethod
    def filter_active_locations(locations: list) -> list[dict]:
        return [location for location in locations if (location['hasMeraki'] and location['isActive']) or location['organizationId']]

    def convert_timestamp_to_building_timezone(self, building_id: str, conversion_input: Union[datetime,date]) -> datetime:
        """
        :param conversion_input: the date to convert
        :param building_id: the building to get the timezone from
        :return: UTC representation of the timestamp in the building's timezone. TZ unaware
        """
        building_tz = gettz(self.basking.location.get_building(building_id=building_id)['data']['getBuilding']['timeZone'])
        if not building_tz:
            raise ValueError(f"Invalid timezone for building ID {building_id}")

        if isinstance(conversion_input, datetime):
            if conversion_input.tzinfo is not None:
                raise ValueError("datetime input must be timezone-naive")

            conv_datetime_utc = conversion_input.replace(tzinfo=building_tz).astimezone(tzutc())

        elif isinstance(conversion_input, date):
            conv_datetime_utc = datetime.combine(conversion_input, time()).replace(tzinfo=building_tz).astimezone(tzutc())
        else:
            raise TypeError("input_date must be a datetime or date object")

        return conv_datetime_utc.replace(tzinfo=None)

    @staticmethod
    def datetime_to_date(dt: datetime) -> date:
        return date.fromisoformat(dt.strftime('%Y-%m-%d'))


def deprecated(func=None, *, message=None):
    func = func or partial(deprecated, message=message)
    message = message or f"{func.__name__} is deprecated"

    @wraps(func)
    def do(*args, **kwargs):
        print(f'*****     DEPRECATION WARNING ({func.func.__name__}): {message}     *****')
        return func(*args, **kwargs)

    return do
