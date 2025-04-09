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
    browser.add_cookie({"name": "MUSIC_U", "value": "00A96C2509C59AD7C523A15B909F79B4FB50200FA2DE14116777B2152D00C67359A546F1E45B6273F8AED5AFF7E0E890034BAD9028AE02ED959BB46FF92D10D17AD8D18E75C018728E3CB6970E1371B39CB165B700E691FB14B531116E0D12CB4D71B73D200248013B8625670EE366C380B7A7FEEC14CDDC3F8FC582803DAEC6997689EDC0CF34B67DED1E6A808E299E509460874119EB0677FA3E822B8E358DB6FE19553C92CC72D33F7092192BD49837FD9F270C83CDA801353B0C92D12C65FE9B0C5015BFF0223416FB11F777DB5A65A7962A366AD5533AB2FEB3019E349B2F22366D88B334CD0F7E049A733269FCE0F7260FD11FEFC90EC5421742904AFB2DA2815DBB89CDBE2154971215D72401B6F1F936E9F3996D998CBABC1CB34A958484CA100CC886F812DB484960B4FD02893693E69AF54DD8EE9BB0103F2171726DDAF9A17E608B82B490ECC97F8E0677AF899634F9724768A3FB4CDEBFFE0643DD"})
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
