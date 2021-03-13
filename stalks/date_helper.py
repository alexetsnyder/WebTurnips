import datetime


class WeekDay:
    MONDAY = 0
    TUESDAY = 1
    WEDNESDAY = 2
    THURSDAY = 3
    FRIDAY = 4
    SATURDAY = 5
    SUNDAY = 6


SUNDAY_FIRST_LOOK_UP_TABLE = [x + 1 for x in range(WeekDay.SUNDAY)] + [0]


def sunday_first(week_day):
    return SUNDAY_FIRST_LOOK_UP_TABLE[week_day]


def week_day_delta(current_week_day, wanted_week_day):
    return sunday_first(wanted_week_day) - sunday_first(current_week_day)


class DateHelper:
    def __init__(self, date_str, date_format):
        self.date_format = date_format
        self.date = datetime.datetime.strptime(date_str, self.date_format)

    def __str__(self):
        return self.date.strftime(self.date_format)

    def get_sunday(date):
        return date + datetime.timedelta(days=week_day_delta(date.weekday(), WeekDay.SUNDAY))

    def get_saturday(date):
        return date + datetime.timedelta(days=week_day_delta(date.weekday(), WeekDay.SATURDAY))

    def sunday(self):
        return DateHelper.get_sunday(self.date)

    def saturday(self):
        return DateHelper.get_saturday(self.date)
