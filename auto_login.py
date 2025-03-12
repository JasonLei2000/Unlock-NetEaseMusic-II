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
    browser.add_cookie({"name": "MUSIC_U", "value": "003487BB961220EFDD4584E6AE7C31A48C0B86DF684AD8733BE4A9E7C7293BF6ECCD6EB762F51BEE0044D01DD28076D55FD1AA17122FC15F33CD74C3CA8A2F98CC0868D5145E784D7A0D1A251E2E3B74B45103ED61A7CDA0A267487E4AFBDF271758F123509C5EABE1F36DC39242001D5E389BC67E989A965EB6481C0123DECB20D856FE306C8055CD145D56B6640966613A399F164107BC418F76D1EB9BBB1E14C5D45CD8883F9081F2AE4EE38D549E3027F45417008CE911380EBC0F68D5C9C50F577CC193C90CF4A4E15CFD99695C2052AFF97EA9DCB65828915F97188FE5A34004D411028E6B8C36C8A0CE18E065791D4C2F74298341EA10FFB4074BE6B6ED76AB2C1FC993E44135EE0D9F76B20A1110E4DB82CF7DAC0B8DC1B4AF328C306B06832015A17757DD7FADCC743876D963C3BD9F25A2F219715162D70668DE12ADF2A8386F1E0AEBE321FF6B291B3B527A09AC74B944B625824F2E933CCDFD435A"})
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
