import os
import time
import sys

from selenium import webdriver
import selenium.webdriver.chrome.service as service

#####################################################################
# Settings

seconds_to_pause = 1  # seconds


class AmazonBrowser(object):

    _Singleton = None

    @staticmethod
    def Singleton():
        if AmazonBrowser._Singleton is None:
            AmazonBrowser._Singleton = AmazonBrowser()
        return AmazonBrowser._Singleton

    def __init__(self):
        # Find the AMAZON_USER and AMAZON_PASSWORD through environment variable
        if 'AMAZON_USER' not in os.environ:
            print("AMAZON_USER must be defined in environment")
            sys.exit(1)
        if 'AMAZON_PASSWORD' not in os.environ:
            print("AMAZON_PASSWORD must be defined in environment")
            sys.exit(1)
        self.AMAZON_USER = os.environ['AMAZON_USER']
        self.AMAZON_PASSWORD = os.environ['AMAZON_PASSWORD']

        self.service = service.Service('chromedriver')
        self.browser = None
        self.is_started = False
        self.is_logged_in = False

    def start(self):

        if self.is_started is False:
            self.service.start()

            capabilities = {
                'chrome.binary':
                '/Applications/Google Chrome.app/Contents/MacOS/Google Chrome'
            }
            self.browser = (
                webdriver.Remote(self.service.service_url, capabilities))
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
        # Connect to Amazon and login

        br = self.browser
        self.get(
            'https://www.amazon.com/ap/signin?_encoding=UTF8&ignoreAuthState=1&openid.assoc_handle=usflex&openid.claimed_id=http%3A%2F%2Fspecs.openid.net%2Fauth%2F2.0%2Fidentifier_select&openid.identity=http%3A%2F%2Fspecs.openid.net%2Fauth%2F2.0%2Fidentifier_select&openid.mode=checkid_setup&openid.ns=http%3A%2F%2Fspecs.openid.net%2Fauth%2F2.0&openid.ns.pape=http%3A%2F%2Fspecs.openid.net%2Fextensions%2Fpape%2F1.0&openid.pape.max_auth_age=0&openid.return_to=https%3A%2F%2Fwww.amazon.com%2F%3Fref_%3Dnav_ya_signin&switch_account='
        )

        user = br.find_element_by_id("ap_email")
        user.send_keys(self.AMAZON_USER)

        pass_ = br.find_element_by_name("password")
        pass_.send_keys(self.AMAZON_PASSWORD)

        submit = br.find_element_by_id("signInSubmit")
        submit.click()  # This blocks until page loads but AJAX may continue
        time.sleep(5)  # Wait additional time for the research page to load
        self.is_logged_in = True
        return

    def video_clear_history(self):
        br = self.browser

        br.get(
            'https://www.amazon.com/gp/yourstore/iyr/ref=pd_ys_iyr_edit_watched?ie=UTF8&collection=watched'
        )

        while (True):
            link = br.find_element_by_link_text(
                "Remove this from watched videos")
            if link is not None:
                link.click()
                time.sleep(seconds_to_pause)
            else:
                break

    def get(self, url):
        self.browser.get(url)
        time.sleep(seconds_to_pause)
        return self.browser

    def page_source(self):
        return self.browser.page_source

    def stop(self):
        self.service.stop()
