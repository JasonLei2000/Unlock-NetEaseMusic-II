# coding: utf-8

import os
import time
import logging
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
from retrying import retry

# Configure logging
logging.basicConfig(level=logging.INFO, format='[%(levelname)s] %(asctime)s %(message)s')

@retry(wait_random_min=5000, wait_random_max=10000, stop_max_attempt_number=3)
def enter_iframe(browser):
    logging.info("Enter login iframe")
    time.sleep(5)  # 给 iframe 额外时间加载
    try:
        iframe = WebDriverWait(browser, 10).until(
            EC.presence_of_element_located((By.XPATH, "//*[starts-with(@id,'x-URS-iframe')]")
        ))
        browser.switch_to.frame(iframe)
        logging.info("Switched to login iframe")
    except Exception as e:
        logging.error(f"Failed to enter iframe: {e}")
        browser.save_screenshot("debug_iframe.png")  # 记录截图
        raise
    return browser

@retry(wait_random_min=1000, wait_random_max=3000, stop_max_attempt_number=5)
def extension_login():
    chrome_options = webdriver.ChromeOptions()

    logging.info("Load Chrome extension NetEaseMusicWorldPlus")
    chrome_options.add_extension('NetEaseMusicWorldPlus.crx')

    logging.info("Initializing Chrome WebDriver")
    try:
        service = Service(ChromeDriverManager().install())  # Auto-download correct chromedriver
        browser = webdriver.Chrome(service=service, options=chrome_options)
    except Exception as e:
        logging.error(f"Failed to initialize ChromeDriver: {e}")
        return

    # Set global implicit wait
    browser.implicitly_wait(20)

    browser.get('https://music.163.com')

    # Inject Cookie to skip login
    logging.info("Injecting Cookie to skip login")
    browser.add_cookie({"name": "MUSIC_U", "value": "00963CCDD5ECA1ACA890A8D4E0B4F02BEEBBC4D3F2670763C15677AFB2C36C2ECD26D5525646917924E2B607561F7C464DFFEDB271A804A2F546EC8A0F190917288CB2B8AABE867B4DAC4EDDCA249314C38154CBCA8125A64A01E75AFB69E949E53DE38C9DB917B068DD65308C276ED52F6CB252987966AFFC1FAA8CF4E92946DCD56E5625A10BD3E01DA0CF442C077D00F86B9430DCDFC58959E254FBA7904C75011C923AA66FB3C016D193ED529B9F9E86F0560AC98B6F6BA9FA412A53AD32D6718CEA1F70D9024F7BB52DCE07339EDCAF2F619607831B974CE506485F30E3F7212829343A4C90F8548B10A000A5A5DAD2A4E2690937BACC47DB40865C073E612FA7C7C851C77E39EDDBECD6B937243ACDC948C3F967717157EC323CB1B70EDCBA64A0096E92D9EBAB3895CA14DE7A7872669B4E74BBF5C60E9FB5D50B75E565632D417C7BAFA86897255E7243D26402727D000D2BBF5A3421481774E2F2E7CE"})
    browser.refresh()
    time.sleep(5)  # Wait for the page to refresh
    logging.info("Cookie login successful")

    # Confirm login is successful
    logging.info("Unlock finished")

    time.sleep(10)
    browser.quit()


if __name__ == '__main__':
    try:
        extension_login()
    except Exception as e:
        logging.error(f"Failed to execute login script: {e}")
