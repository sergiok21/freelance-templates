from datetime import datetime, timezone
from zoneinfo import ZoneInfo

import pytz
from dateutil.relativedelta import relativedelta
from dateutil.tz import tzlocal


class Transformer:
    @staticmethod
    def transform_to_standard_date(date: datetime) -> str:
        return date.strftime('%d.%m.%Y %H:%M')

    @staticmethod
    def transform_to_datetime(date: str) -> datetime:
        date_format = "%d.%m.%Y %H:%M"
        return datetime.strptime(date, date_format)


class Date(Transformer):
    _default_timezone = '...'

    @staticmethod
    def create_date(
            seconds: int = 0,
            minutes: int = 0,
            hours: int = 0,
            days: int = 0,
            months: int = 0,
            transform: bool = False,
            timezone_: str = None
    ) -> datetime | str:
        now = datetime.now(pytz.timezone(timezone_) if timezone_ else pytz.timezone(Date._default_timezone))

        delta_args = {'seconds': seconds, 'minutes': minutes, 'hours': hours, 'days': days, 'months': months}
        time_later = now + relativedelta(**{k: v for k, v in delta_args.items() if v})

        if transform:
            return Date.transform_to_standard_date(time_later)
        return time_later

    @staticmethod
    def get_current_date(transform: bool = False) -> datetime | str:
        if transform:
            return datetime.now().strftime('%d.%m.%Y %H:%M')
        return datetime.now()

    @staticmethod
    def update_date(
            date: str,
            seconds: int = 0,
            minutes: int = 0,
            hours: int = 0,
            days: int = 0,
            months: int = 0,
            transform: bool = False
    ) -> datetime | str:
        delta_args = {'seconds': seconds, 'minutes': minutes, 'hours': hours, 'days': days, 'months': months}
        new_date = Date.transform_to_datetime(date) + relativedelta(**{k: v for k, v in delta_args.items() if v})
        if transform:
            return Date.transform_to_standard_date(new_date)
        return new_date

    @staticmethod
    def compare_dates(current_date: str, user_date: str) -> bool:
        current_date, user_date = \
            Date.transform_to_datetime(current_date), Date.transform_to_datetime(user_date)
        if current_date > user_date:
            return True
        elif current_date < user_date:
            return False
        else:
            return True

    @staticmethod
    def sort_date(users: list, to_datetime: bool = False) -> list:
        if to_datetime:
            sorted_users = sorted(users, key=lambda x: Date.transform_to_datetime(x[1]))
            return [
                [user[0], Date.transform_to_standard_date(Date.transform_to_datetime(user[1]))]
                for user in sorted_users
            ]
        return sorted(users, key=lambda x: Date.transform_to_datetime(x[1]))

    @staticmethod
    def define_date_type(date: datetime | int | str) -> datetime:
        if isinstance(date, int):
            return Date.create_date(months=date)
        elif isinstance(date, str):
            return Date.transform_to_datetime(date=date)
        return date
