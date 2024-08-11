import selenium.webdriver as webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support.expected_conditions import presence_of_element_located
import base64
import time


class BrowserAutomation:

    def __init__(self, show_browser=False):
        self.options = webdriver.ChromeOptions()
        self.options.add_argument('--start-maximized')
        self.options.add_argument('--kiosk-printing')
        self.options.add_argument("--log-level=3")

        self.options.add_experimental_option("prefs", {"plugins.always_open_pdf_externally": True})

        if not show_browser:
            self.options.add_argument("--headless")

        self.driver = webdriver.Chrome(service=ChromeService(executable_path="chromedriver.exe"), options=self.options)

    def open_url(self, url):
        self.driver.get(url)

    def open_url_in_tab(self, url):
        self.driver.switch_to.new_window("tab")
        self.driver.get(url)

    def close_browser(self):
        self.driver.quit()

    def print_pdf(self, destination_path: str):
        pdf_data = self.driver.execute_cdp_cmd("Page.printToPDF", {
            "recentDestinations": [{
                "id": "Save as PDF",
                "origin": "local",
                "account": "",
            }],
            "selectedDestinationId": "Save as PDF",
            "version": 2
        })
        with open(destination_path, 'wb') as file:
            file.write(base64.b64decode(pdf_data['data']))
        time.sleep(1)

    def set_download_path(self, path: str):
        """

        :param path:
        """
        self.driver.execute_cdp_cmd("Page.setDownloadBehavior", {
            "behavior": "allow",
            "downloadPath": path,
        })

    def find_element_by_xpath(self, selector: str, timeout=10):
        """

        :param selector:
        :param timeout:
        :return:
        """
        element = WebDriverWait(self.driver, timeout).until(
            presence_of_element_located((By.XPATH, selector))
        )
        return element

    def find_element_by_tag(self, selector: str, timeout=10):
        """

        :param selector:
        :param timeout:
        :return:
        """
        element = WebDriverWait(self.driver, timeout).until(
            presence_of_element_located((By.TAG_NAME, selector))
        )
        return element

    def find_element_by_id(self, selector: str, timeout=10):
        """

        :param selector:
        :param timeout:
        :return:
        """
        element = WebDriverWait(self.driver, timeout).until(
            presence_of_element_located((By.ID, selector))
        )
        return element

    def find_element_by_class(self, selector: str, timeout=10):
        """

        :param selector:
        :param timeout:
        :return:
        """
        element = WebDriverWait(self.driver, timeout).until(
            presence_of_element_located((By.CLASS_NAME, selector))
        )
        return element
