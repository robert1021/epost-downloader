from enums import CalendarDayTypes
from dateutil import parser
from datetime import datetime, date, timedelta
from dates_data import federal_calendar_data


class FederalCalendar:

    def __init__(self):
        self.min_date = parser.parse('01-Jan-2010')
        self.max_date = parser.parse('31-Dec-2039')

    def validate_date(self, check_date: datetime):
        """
        Validates if the date is within the expected date range

        :param check_date: The date to validate as a datetime object
        """
        if check_date < self.min_date or check_date > self.max_date:
            raise Exception('Date is outside of expected range')

    def is_work_day(self, check_date: datetime) -> bool:
        """
        Searches a dictionary for the checkDate and verifies if it is a Workday.

        :param check_date: The date to check as a datetime object
        :return: True or False depending on if the day is a Workday
        """
        self.validate_date(check_date)

        # Convert datetime to string
        string_date = f'{check_date:%d-%b-%Y}'.upper()

        # Check if the date is a Workday
        return CalendarDayTypes[federal_calendar_data[string_date]['TYPE'].upper()] is CalendarDayTypes.WORKDAY

    def get_business_date(self, given_datetime: datetime) -> date:
        """
        Gets the business date based on the given date and time.

        :param given_datetime: The date and time to find its business date
        :return: If the given datetime is on a workday before 5pm, returns the same date.
                 If the time is after 5pm or the date is on a weekend or holiday, returns the date of the next workday.
        """
        # Is workday before 5pm
        if self.is_work_day(given_datetime) and given_datetime.hour < 17:
            return given_datetime.date()

        # Find next workday
        next_work_day = given_datetime
        while True:
            next_work_day = next_work_day + timedelta(days=1)
            if self.is_work_day(next_work_day):
                return next_work_day.date()