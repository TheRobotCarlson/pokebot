from selenium import webdriver
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from selenium.webdriver.common.keys import Keys
from selenium.webdriver import ChromeOptions
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import ElementNotVisibleException

from time import sleep
import urllib.parse
import random

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

    for entry in driver.get_log('browser'):
        if entry['source'] == 'console-api':
            item = entry['message'][entry['message'].index("\"") + 1: -1]
            loc = item.find(url_end)

            # try:
            #     if len(driver.find_elements_by_name("chooseMove")) > 0:
            #         random.choice(driver.find_elements_by_name("chooseMove")).click()
            #         print("here2")
            #         continue
            # except ElementNotVisibleException:
            #     if len(driver.find_elements_by_name("chooseSwitch")) > 0:
            #         random.choice(driver.find_elements_by_name("chooseSwitch")).click()
            #         continue

            if loc != -1:
                temp_str = item[loc + len(url_end):]
                find_request = "request"
                loc = temp_str.find(find_request)

                if loc != -1:
                    print(temp_str[loc + len(find_request) + 1:])
                    continue

                find_request = "choice"
                loc = temp_str.find(find_request)

                if loc != -1:
                    print(temp_str[loc + len(find_request) + 1:])
                    continue

                find_request = "inactive"
                loc = temp_str.find(find_request)

                if loc != -1:
                    print(temp_str[loc + len(find_request) + 1:])
                    continue

                find_request = "choose"
                loc = temp_str.find(find_request)

                if loc != -1:
                    print(temp_str[loc + len(find_request) + 1:])
                    continue

                print(temp_str)
            else:
                print(item)
    sleep(10)
