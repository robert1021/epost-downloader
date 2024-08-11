import datetime
from dateutil import parser
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver import ActionChains
from selenium.webdriver.support.ui import Select
from selenium.common.exceptions import NoSuchElementException
import time
import random
from browser_automation import BrowserAutomation
from utilities import update_user_chrome_preferences
from constants import EPOST_CONNECT_LOGIN_URL, EPOST_CONNECT_LOGOUT_URL
from enums import EpostConnectApplicationScrapeHeaders
from xlsx_builder import XlsxBuilder
from styling import Styling
from utilities import get_timestamp


class WebScrapeMessages:
    """ WebScrapeMessages

        This class is used to navigate the ePost Connect inbox using selenium for web automation.
        The scrapeDateRange() and scrapeNew() methods of this class is what should be used to get message data from the ePost Connect website.


    """

    def __init__(self, username: str, password: str):
        """
        Constructs an object that is used to automate and scrape message data from the ePost Connect website.

        :param username: The username for logging into the ePost Connect website.
        :param password: The password for logging into the ePost Connect website.
        """
        self.username = username
        self.password = password
        self.report_name = "epost_new_messages"
        self.sheet_name = "New Messages"

        # Close chromeBrowser before starting driver
        # close_chrome_browser()
        # Turn off restore session pop-up
        update_user_chrome_preferences()
        # Set up Chrome driver (starts Chrome browser as well)
        # Chrome driver will be downloaded automatically
        self.driver = BrowserAutomation(show_browser=True).driver
        # Time to search for element
        self.driver.implicitly_wait(45)

    @staticmethod
    def __check_icon(text: str) -> str:
        """
        Checks the provided text to determine if it is a new message or conversation.

        :param text: The string of html element you would like to determine if new message or conversation
        :return: 'New message' or 'Conversation'
        """
        new_message = 'background: url("/EDMS/connect/images/icon_new.png") left center no-repeat scroll transparent;'
        if new_message.lower() in text.lower():
            return 'New message'
        else:
            return 'Conversation'

    @staticmethod
    def __is_checkbox(element: WebElement) -> bool:
        """
        Checks if a message has a checkbox.

        :param element: The html element to check if it has a checkbox.
        """
        try:
            element.find_element(By.CLASS_NAME, 'js-select-conversation')
            return True

        except:
            return False

    @staticmethod
    def __get_message_status(element: WebElement) -> bool:
        """
        Checks if a message is open or closed.

        :param element: The html element to check if open or closed message.
        :return: True for a closed message. False for an open message.
        """
        try:
            element.find_element(By.CLASS_NAME, 'closed')
            image = element.find_element(By.TAG_NAME, 'img')
            img_src = image.get_attribute('src')
            if '/EDMS/connect/images/message-envelope-en.png' in img_src:
                return True
            else:
                return False

        except:
            return False

    @staticmethod
    def __get_company_code_convo_subject(subject: str) -> str:
        """
        Gets the company code from the message subject.

        :param subject: The message subject that you want to extract the company code from.
        :return: The company code as a string.
        """
        return subject[:5]

    @staticmethod
    def __get_message_date_modified(element: WebElement) -> str:
        """
        Gets the date modified of a message.

        :param element: The html element to get the date from.
        :return: Date modified in the format "Dec 14, 2022"
        """
        return element.find_element(By.CLASS_NAME, 'modified').text

    @staticmethod
    def __compare_dates(message_date: datetime.datetime, start_date: datetime.datetime, end_date) -> bool:
        """
        Compares message date to start and end date.

        :param message_date: Date the message was sent.
        :param start_date: The start date.
        :param end_date: The end date.
        :return: True if messageDate is within the date range, False otherwise.
        """
        # Check times
        if end_date is not None:
            if start_date <= message_date <= end_date:
                return True

        else:
            if message_date >= start_date:
                return True

        return False

    def __set_amount_messages_displayed(self):
        """
        Sets the amount of messages displayed on main page.

        """
        display = self.driver.find_element(By.XPATH, '//*[@id="connect"]/footer/div/div[1]/select')
        select = Select(display)
        # Set to max
        select.select_by_index(5)

    def __get_messages(self) -> list[WebElement]:
        """
        Gets a list of all messages as elements.

        :return allMessages: List of elements.
        """
        files_container = self.driver.find_element(By.ID, 'files')
        all_messages = files_container.find_elements(By.TAG_NAME, 'li')

        return all_messages

    def __click(self, element_to_click: WebElement):
        """
        Moves to and clicks on specified element.

        :param element_to_click: The html element you would like apply actions to.
        """
        act_chains = ActionChains(self.driver)
        act_chains.pause(random.uniform(0.5, 1))
        act_chains.move_to_element(element_to_click)
        act_chains.pause(random.uniform(0.5, 1))
        act_chains.click(element_to_click)
        act_chains.perform()
        act_chains.reset_actions()

    def __create_report(self, rows: list[list]):
        """
        Create an Excel report with the provided rows.

        :param rows: A list of lists representing the rows of data to be included in the report.
                     Each inner list represents a row, with its elements being the column values.
        """
        rows.insert(0, EpostConnectApplicationScrapeHeaders.get_values())
        # Create excel report
        wb = XlsxBuilder()
        wb.add_sheet(self.sheet_name, rows)
        timestamp = get_timestamp()
        wb.save(f"{self.report_name}_{timestamp}.xlsx")
        # Add Styling
        Styling(f"{self.report_name}_{timestamp}.xlsx").apply_basic_styling(self.sheet_name)

    def login_epost(self):
        """
        Logs into ePost Connect account.

        """
        self.driver.get(EPOST_CONNECT_LOGIN_URL)
        time.sleep(random.uniform(1, 2))

        # check if remember username selected
        checkbox = self.driver.find_element(By.CLASS_NAME, 'cpc-checkbox__box')
        is_checked = checkbox.get_attribute('aria-checked')

        # Username
        if is_checked == 'false':
            username_box = self.driver.find_element(By.XPATH, '//*[@id="f-username"]')
            username_box.send_keys(self.username)

        time.sleep(random.uniform(1, 2))
        # Password
        password_box = self.driver.find_element(By.XPATH, '//*[@id="f-password"]')
        password_box.send_keys(self.password)

        time.sleep(3)
        # Press enter to log in
        password_box.send_keys(Keys.RETURN)
        self.driver.implicitly_wait(10)
        time.sleep(3)

        try:
            error_message = self.driver.find_element(By.CLASS_NAME, "notification--error")

            if error_message is not None:
                password_box.send_keys(Keys.RETURN)

        except NoSuchElementException:
            pass

        self.driver.implicitly_wait(45)

    def sign_out_epost(self):
        """
        Signs out of ePost Connect account.

        """
        self.driver.get(EPOST_CONNECT_LOGOUT_URL)
        self.driver.quit()

    def scrape_new(self):
        """
        Navigates ePost Connect website and scrapes information on all new messages.
        """
        rows = []
        open_convo_counter = 0

        self.login_epost()
        self.__set_amount_messages_displayed()

        # Container that holds all the conversations
        conversations = self.__get_messages()

        for convo in conversations:
            # Check if conversation has checkbox. Skip the ones without it.
            self.driver.implicitly_wait(0.25)
            if self.__is_checkbox(convo):
                self.driver.implicitly_wait(45)

                # Check icon to see if it's a new message
                icon = convo.find_element(By.CLASS_NAME, 'icon')
                status = icon.get_attribute('style')
                icon_status = self.__check_icon(status)

                # Check for 25 conversations with no closed message in a row.
                if open_convo_counter == 25:
                    break

                # Only get data on new messages.
                if icon_status == 'New message':

                    open_convo_counter = 0

                    time.sleep(random.randint(3, 5))

                    convo_tile = convo.find_element(By.CLASS_NAME, 'name')
                    subject = convo_tile.text
                    company_code = self.__get_company_code_convo_subject(subject)

                    # Enter message
                    self.__click(convo_tile)

                    time.sleep(random.uniform(3, 5))

                    conversation_container = self.driver.find_element(By.ID, 'conversation')

                    # Need to sleep so html can load
                    time.sleep(random.uniform(1, 5))
                    total_convo_messages = conversation_container.find_element(By.CLASS_NAME,
                                                                               'js-message-pagination-summary')
                    total_convo_messages = int(total_convo_messages.text.split(' ')[3])  # Extract total from string

                    # display all button doesn't exist if 5 or less messages
                    if not total_convo_messages <= 5:
                        #  Click the button to display all conversation messages
                        display_all_btn = conversation_container.find_element(By.CLASS_NAME, 'js-load-all-messages')
                        self.__click(display_all_btn)

                    time.sleep(random.uniform(3, 5))

                    # Check number of loaded messages up to 25 times.
                    # Need to verify all have been loaded
                    for i in range(0, 25):
                        all_replies = conversation_container.find_elements(By.CLASS_NAME, 'message-container')
                        if len(all_replies) == total_convo_messages:
                            break

                        time.sleep(random.uniform(3, 5))

                    time.sleep(random.uniform(1, 5))

                    open_message_counter = 0

                    # All received messages
                    all_sender_messages = conversation_container.find_elements(By.CLASS_NAME, 'editorLeft')

                    # Reverse the list because newest will be last.
                    all_sender_messages.reverse()

                    self.driver.implicitly_wait(0.25)

                    for item in all_sender_messages:

                        # check for 25 messages with no closed message in a row.
                        if open_message_counter == 25:
                            break

                        date_container = item.find_element(By.CLASS_NAME, 'date')
                        split_date_info = date_container.text.split('\n')

                        sent = split_date_info[0].replace('Sent: ', '')
                        expires = split_date_info[1].replace('Expired: ', '').replace('Expires: ', '')

                        # Check if message is open or closed.
                        message_status = self.__get_message_status(item)
                        if message_status:
                            open_message_counter = 0

                            formatted_sent_time = parser.parse(sent[:-4])
                            formatted_expiry_time = parser.parse(expires[:-4])
                            # add message data to rows
                            rows.append([company_code, subject, formatted_sent_time, formatted_expiry_time])

                        else:
                            open_message_counter += 1

                    self.driver.implicitly_wait(45)

                    time.sleep(random.uniform(10, 20))
                    # close message
                    close_btn = conversation_container.find_element(By.ID, 'close')
                    self.__click(close_btn)

                else:
                    open_convo_counter += 1

        self.__create_report(rows)
        # Add sign out here
        self.sign_out_epost()

    def scrape_date_range(self, start_date: datetime.datetime, end_date: datetime.datetime = None):
        """
        Navigates ePost Connect website and scrapes information on messages in a specific range.

        :param start_date: The start date and time of the range.
        :param end_date: The end date and time of the range.
                        Can be None if you want to capture everything greater or equal to the start date.
        """
        # Need to make the time 00:00:00 to be able to compare to date modified of each conversation
        start_date_modified = start_date.replace(hour=0, minute=0, second=0, microsecond=0)

        rows = []

        self.login_epost()
        self.__set_amount_messages_displayed()

        # Container that holds all the messages
        conversations = self.__get_messages()

        # Start going through each conversation
        for convo in conversations:
            # Check if conversation has checkbox. Skip the ones without it.
            self.driver.implicitly_wait(0.25)
            if self.__is_checkbox(convo):
                self.driver.implicitly_wait(45)
                # Get conversation date modified
                date_modified = parser.parse(self.__get_message_date_modified(convo))

                # Need to click on a conversation if date modified is not less than start date
                if self.__compare_dates(date_modified, start_date=start_date_modified, end_date=None):
                    time.sleep(random.randint(3, 5))

                    convo_tile = convo.find_element(By.CLASS_NAME, 'name')
                    subject = convo_tile.text
                    company_code = self.__get_company_code_convo_subject(subject)

                    # Enter conversation
                    self.__click(convo_tile)

                    time.sleep(random.uniform(3, 5))

                    conversation_container = self.driver.find_element(By.ID, 'conversation')

                    # Need to sleep so html can load
                    time.sleep(random.uniform(1, 5))
                    total_convo_messages = conversation_container.find_element(By.CLASS_NAME,
                                                                               'js-message-pagination-summary')
                    total_convo_messages = int(total_convo_messages.text.split(' ')[3])  # Extract total from string

                    # display all button doesn't exist if 5 or less messages
                    if not total_convo_messages <= 5:
                        #  Click the button to display all conversation messages
                        display_all_btn = conversation_container.find_element(By.CLASS_NAME, 'js-load-all-messages')
                        self.__click(display_all_btn)

                    time.sleep(random.uniform(3, 5))

                    # Check number of loaded messages up to 25 times.
                    # Need to verify all have been loaded
                    for i in range(0, 25):
                        all_replies = conversation_container.find_elements(By.CLASS_NAME, 'message-container')
                        if len(all_replies) == total_convo_messages:
                            break

                        time.sleep(random.uniform(3, 5))

                    time.sleep(random.uniform(1, 5))

                    # All received messages
                    all_sender_messages = conversation_container.find_elements(By.CLASS_NAME, 'editorLeft')

                    # Reverse the list because newest will be last.
                    all_sender_messages.reverse()

                    self.driver.implicitly_wait(0.25)

                    # Start going through each sender message
                    for item in all_sender_messages:

                        date_container = item.find_element(By.CLASS_NAME, 'date')
                        split_date_info = date_container.text.split('\n')

                        # Date message sent
                        sent = split_date_info[0].replace('Sent: ', '')
                        # Date message expires
                        expires = split_date_info[1].replace('Expired: ', '').replace('Expires: ', '')

                        formatted_sent_time = parser.parse(sent[:-4])

                        # Add message data to rows list if within the range
                        if self.__compare_dates(formatted_sent_time, start_date, end_date):
                            formatted_expiry_time = parser.parse(expires[:-4])

                            rows.append([company_code, subject, formatted_sent_time, formatted_expiry_time])

                        # Stop looking for messages in date range
                        elif formatted_sent_time < start_date:
                            break

                    self.driver.implicitly_wait(45)

                    time.sleep(random.uniform(10, 20))
                    # close conversation
                    close_btn = conversation_container.find_element(By.ID, 'close')
                    self.__click(close_btn)

                # Stop looking through conversations
                else:
                    break

        self.__create_report(rows)
        # Sign out of ePost
        self.sign_out_epost()