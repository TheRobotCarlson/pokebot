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


chrome_options = webdriver.ChromeOptions()
prefs = {"profile.default_content_setting_values.notifications": 2}
chrome_options.add_experimental_option("prefs", prefs)
chrome_options.add_extension('./Adblock-Plus_v1.13.4.crx')

capabilities = DesiredCapabilities.CHROME

capabilities['loggingPrefs'] = {'browser': 'ALL'}

driver = webdriver.Chrome(desired_capabilities=capabilities, chrome_options=chrome_options)

home_website = 'http://play.pokemonshowdown.com/'

driver.get(home_website)

sleep(1)
driver.find_element_by_name("search").click()

sleep(3)

elem = driver.find_element_by_name("username")
elem.send_keys("therobotcarlson2")
elem.send_keys(Keys.RETURN)

sleep(3)

driver.find_element_by_name("search").click()

# print console log messages
for entry in driver.get_log('browser'):
    if entry['source'] == 'console-api':
        print(entry['message'])

print("---------------------------------new data -------------------")

sleep(10)
url_parts = urllib.parse.urlparse(driver.current_url)
path_parts = url_parts[2].rpartition('/')
url_end = '{}'.format(path_parts[2])

print(driver.current_url)
print(url_end)

# url_end = driver.current_url.rsplit('/', 1)[-1]

while True:
    if random.choice([0, 1, 2, 3]) == 0:
        if len(driver.find_elements_by_name("chooseSwitch")) > 0:
            random.choice(driver.find_elements_by_name("chooseSwitch")).click()
    else:
        if len(driver.find_elements_by_name("chooseMove")) > 0:
            random.choice(driver.find_elements_by_name("chooseMove")).click()

    read_console(driver.get_log('browser'))

    sleep(5)
