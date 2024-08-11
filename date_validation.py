import re
from datetime import datetime


class DateValidation:
    """
        This class contains methods to handle all the necessary date validations required for the epost downloader.
        ---------------------------------------------------------------------
        Attributes:
            :param beginning_date: The beginning date of the download range.
            :param ending_date: The ending date of the download range.
        ---------------------------------------------------------------------
        Methods:
            method check_date_format: To check the date format.
            method compare_date: To compare the beginning and ending dates.
            method test_before_2022: To check if the date is before 2022.
        ---------------------------------------------------------------------
        Note: The test_before_2022 method is only for testing purposes and should be REMOVED before compiling the application.
        ---------------------------------------------------------------------
    """

    def __init__(self, beginning_date, ending_date):
        """
            The constructor for the DateValidation class.
            ---------------------------------------------------------------------
            Parameters:
                :param beginning_date: The beginning date of the download range.
                :param ending_date: The ending date of the download range.
            ---------------------------------------------------------------------
        """
        self.beginning_date = beginning_date
        self.ending_date = ending_date

    def check_date_format(self):
        """
            This method is used to check the date format.
            ---------------------------------------------------------------------
            Purpose: To ensure date attributes self.beginning_date and self.ending_date are in the correct format.
            ---------------------------------------------------------------------
            Returns:
                :return: True if the BOTH date attributes are in the correct format, otherwise return an error message.
        """
        pattern = re.compile(r"^\d{2}/\d{2}/\d{4}$")
        if not pattern.match(self.beginning_date) or not pattern.match(self.ending_date):
            return False
        return True

    def compare_date(self):
        """
            This method is used to compare the beginning and ending dates
            ---------------------------------------------------------------------
            Purpose: To ensure that the beginning date is not later than the ending date.
            ---------------------------------------------------------------------
            Returns:
                :return: "success" if the beginning date is not later than the ending date, otherwise return an error message.
        """
        beginning_date = datetime.strptime(self.beginning_date, "%m/%d/%Y")
        ending_date = datetime.strptime(self.ending_date, "%m/%d/%Y")

        if beginning_date > ending_date:
            return False
        return True

    def test_before_2022(self):
        """
            Note: This method is only for testing purposes and should be REMOVED before compling the application.
            ---------------------------------------------------------------------
            This is a test method to check if the date is before 2022.
            ---------------------------------------------------------------------
            Purpose: To prevent accidentally downloading messages before 2022.
            ---------------------------------------------------------------------
            Returns:
                :return: "success" if the dates are before 2022, otherwise an error message.
        """

        beginning_date = datetime.strptime(self.beginning_date, "%m/%d/%Y")
        ending_date = datetime.strptime(self.ending_date, "%m/%d/%Y")

        if beginning_date.year > 2022:
            return False
        elif ending_date.year > 2022:
            return False

        return True

    def is_future_date(self):
        """
        Check if either the beginning_date or ending_date is in the future compared to the current date.

        :return: True if either beginning_date or ending_date is in the future, otherwise False.
        """
        current_date = datetime.strptime(datetime.now().strftime("%m/%d/%Y"), "%m/%d/%Y")
        beginning_date = datetime.strptime(self.beginning_date, "%m/%d/%Y")
        ending_date = datetime.strptime(self.ending_date, "%m/%d/%Y")

        if beginning_date > current_date or ending_date > current_date:
            return True
        return False
