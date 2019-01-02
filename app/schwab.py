import os
import os.path
import time
import datetime
import sys

from selenium import webdriver
import selenium.webdriver.chrome.service as service
from selenium.webdriver.common.action_chains import ActionChains

#####################################################################
# Settings


def move_latest_downloaded_file(newname, folder_of_download, folder_to_save_to):

    filename = None
    for i in range(0, 120):
        # Find the newest file created
        filename = max([f for f in os.listdir(folder_of_download)],
                       key=lambda xa: os.path.getctime(os.path.join(folder_of_download, xa)))

        if not filename.endswith('.part'):
            break
        else:
            print("Waiting for file to complete download, because *.part file exists: %s" % filename)
            time.sleep(1)

    if filename is None:
        print("Failed to find downloaded file")
        sys.exit(1)
    else:
        os.rename(os.path.join(folder_of_download, filename), os.path.join(folder_to_save_to, newname))
    return


class Schwab(object):

    _Singleton = None

    @staticmethod
    def Singleton():
        if Schwab._Singleton is None:
            Schwab._Singleton = Schwab()
        return Schwab._Singleton

    def __init__(self, download_dir, save_dir):
        self.service = service.Service('chromedriver')
        self.browser = None
        self.is_started = False
        self.is_logged_in = False

        self.download_dir = download_dir
        self.save_dir = save_dir

    def start(self):

        if self.is_started is False:
            self.service.start()

            capabilities = {'chrome.binary': '/Applications/Google Chrome.app/Contents/MacOS/Google Chrome'}

            self.browser = (webdriver.Remote(self.service.service_url, capabilities))
            self.browser.implicitly_wait(10)  # seconds

            self.is_started = True

        return

    def login(self):

        self.start()
        assert (self.is_started is True)
        assert (self.browser is not None)

        # Don't login twice
        if self.is_logged_in is True:
            return True

        #######################################
        # Connect to to the service provider and promt the user to login

        self.get('https://www.schwab.com')
        time.sleep(5)

        input("Please find the newly opened browser window\n" + "  and authenticate.  Once you have successfully\n" +
              "  authenticated, please return to this window and\n" + "Press Enter to continue...")
        self.is_logged_in = True
        return

    def show_and_click(self, element, **kwargs):

        sleep_after_show = kwargs.get('sleep_after_show', 0)
        sleep_after_click = kwargs.get('sleep_after_click', 0)

        ActionChains(self.browser).move_to_element(element).perform()
        time.sleep(0.25)
        time.sleep(sleep_after_show)

        try:
            element.click()
        except Exception as e:
            print(str(e))
            # Then try one more time by scrolling the element into view using a different mechanism
            self.browser.execute_script("arguments[0].scrollIntoView();", element)
            time.sleep(0.25)
            element.click()
            time.sleep(sleep_after_show)

        time.sleep(sleep_after_click)
        return

    def download_all(self):
        for i in ['Bank', 'Brokerage']:
            self.download_statements_helper(i)
        return

    def download_statements_helper(self, type):
        # type can be 'Bank' or 'Brokerage'

        br = self.browser

        # Browse to the statements page
        br.get('https://client.schwab.com/Apps/accounts/statements')
        time.sleep(5)

        # Select the Date range to be 10 years
        self.show_and_click(
            br.find_element_by_xpath("//select[@id='statements-daterange1']/option[text()='Last 10 Years']"),
            sleep_after_click=1)

        # Select all bank accounts
        self.show_and_click(br.find_element_by_xpath("//button[@id='sch-account-selector-btn']"), sleep_after_click=1)
        self.show_and_click(
            br.find_element_by_xpath("//div/a[text()='Show All %s Accounts']" % type), sleep_after_click=1)

        # Select all document types
        self.show_and_click(br.find_element_by_xpath("//a[text()='Select All']"), sleep_after_click=1)

        # Click the search button
        self.show_and_click(br.find_element_by_xpath("//button[@id='btnSearch']"), sleep_after_click=5)

        # Download each statement
        for row in br.find_elements_by_xpath("//tr[@scope='row']"):
            spans = row.find_elements_by_xpath(".//span")
            dt = datetime.datetime.strptime(spans[0].text, '%m/%d/%Y')
            doctype = spans[1].text
            account = spans[2].text
            docname = spans[4].text
            savebtn = spans[6]

            datestr = "%d%d%d" % (dt.year, dt.month, dt.day)
            filename = str.join(" ", [datestr, doctype, account, docname]).replace(" ", "-").lower() + ".pdf"

            if os.path.isfile(os.path.join(self.save_dir, filename)):
                print("Skipping download of existing file %s" % (filename))
            else:
                print("Downloading file %s" % (filename))
                self.show_and_click(savebtn, sleep_after_click=5)
                move_latest_downloaded_file(filename, self.download_dir, self.save_dir)

        return

    def get(self, url):
        self.browser.get(url)
        return self.browser

    def page_source(self):
        return self.browser.page_source

    def stop(self):
        self.service.stop()
