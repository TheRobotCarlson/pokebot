from selenium import webdriver
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from selenium.webdriver.common.keys import Keys
from selenium.webdriver import ChromeOptions
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import ElementNotVisibleException

from time import sleep
import urllib.parse
import random
from parse_input import read_console
from TAMER_Input import TAMERInput
import queue

class showdown:
    def __init__(self, username):
        self.in_q = queue.Queue()
        self.out_q = queue.Queue()
        self.tamer = TAMERInput(self.in_q, self.out_q)

        self.tamer.start()
        self.username = username

        self.init_selenium()
        self.tamer.run()

    def init_selenium(self):
        chrome_options = webdriver.ChromeOptions()
        prefs = {"profile.default_content_setting_values.notifications": 2}
        chrome_options.add_experimental_option("prefs", prefs)
        chrome_options.add_extension('./Adblock-Plus_v1.13.4.crx')

        capabilities = DesiredCapabilities.CHROME

        capabilities['loggingPrefs'] = {'browser': 'ALL'}

        self.driver = webdriver.Chrome(desired_capabilities=capabilities, chrome_options=chrome_options)

        home_website = 'http://play.pokemonshowdown.com/'

        self.driver.get(home_website)

        sleep(1)
        self.driver.find_element_by_name("search").click()

        sleep(3)

        elem = self.driver.find_element_by_name("username")
        elem.send_keys(self.username)
        elem.send_keys(Keys.RETURN)

        sleep(3)

        self.driver.find_element_by_name("search").click()
        self.state = []

    def get_actions(self):
        return list(self.driver.find_elements_by_name("chooseMove")) + list(self.driver.find_elements_by_name("chooseSwitch"))

    # action
    def step(self, action):

        while not self.in_q.empty():
            self.in_q.get()

        if action > 3:
            switch_elements = self.driver.find_elements_by_name("chooseSwitch")
            if 0 < action - 4 < len(switch_elements):
                self.driver.find_elements_by_name("chooseSwitch")[action - 4].click()
        else:
            move_elements = self.driver.find_elements_by_name("chooseMove")
            if 0 < action < len(move_elements):
                self.driver.find_elements_by_name("chooseMove")[action].click()

        self.in_q.put((self.state, action))

        sleep(5)

        self.state = read_console(self.driver.get_log('browser'))

        if self.state == -1:
            return [], 0, True
        else:
            if self.out_q.empty():
                reward = 0
            else:
                reward = self.out_q.get()
                print(reward)
            return self.state, reward, False

    def reset(self):
        self.driver.close()
        self.driver.quit()

        self.init_selenium()
