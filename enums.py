from enum import Enum


class VTPReceiveLogFields(Enum):
    MESSAGE_ID = "Message ID"
    SENT_TIMESTAMP = "Sent Timestamp"
    RECEIVED_TIMESTAMP = "Received Timestamp"
    SUBJECT = "Subject"
    OWNER = "Owner"
    ATTACHMENT = "Attachment"
    STATUS = "Status"

    @classmethod
    def get_values(cls):
        return [member.value for member in cls]


class VTPTrackLogFields(Enum):
    MESSAGE_ID = "Message ID"
    SENT_TIMESTAMP = "Sent Timestamp"
    SUBJECT = "Subject"
    OWNER = "Owner"
    PARTICIPANT = "Participant"
    STATUS = "Status"
    STATUS_TIMESTAMP = "Status Timestamp"

    @classmethod
    def get_values(cls):
        return [member.value for member in cls]


class EpostConnectApplicationScrapeHeaders(Enum):
    COMPANY_CODE = "Company Code"
    CONVERSATION_TITLE = "Conversation Title"
    SENT_DATETIME = "Sent Datetime"
    EXPIRY_DATETIME = "Expiry Datetime"

    @classmethod
    def get_values(cls):
        return [member.value for member in cls]


class CalendarDayTypes(Enum):
    HOLIDAY = "Holiday"
    WORKDAY = "Workday"
    WEEKEND = "Weekend"


class Holidays(Enum):
    NEW_YEARS_DAY = "New Years Day"
    GOOD_FRIDAY = "Good Friday"
    EASTER_MONDAY = "Easter Monday"
    VICTORIA_DAY = "Victoria Day"
    CANADA_DAY = "Canada Day"
    CIVIC_HOLIDAY = "Civic Holiday"
    LABOUR_DAY = "Labour Day"
    NATIONAL_DAY_FOR_TRUTH_AND_RECONCILIATION = "Truth & Reconciliation Day"
    THANKSGIVING = "Thanksgiving Day"
    REMEMBRANCE_DAY = "Remembrance Day"
    CHRISTMAS_DAY = "Christmas Day"
    BOXING_DAY = "Boxing Day"
