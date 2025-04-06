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
    browser.add_cookie({"name": "MUSIC_U", "value": "00665AAE7F529F2E2B8FD66ECF3F867C25ABB2760D86EC684324E94599E9A42822FEA72D2DD1C0C64E9E9FC2B71D686BA81C1D745177F25F445366EB7AF569D6C3644F63CF27F923D3D8A69AD10A48F10E9FFA956CEB7BFFD416D8BF92ED04AFB673E6FD0A1354D0D42B38EE3714C15F0269464A609549B26630C76040D60CAB06BB2048E792492F55B5B9886E37F7DD2F37A9A06FB7784124D89FF63B940ADC1F7A7F29028D9B2EE5A47889D78047DBE53380A64618BE15E7D47FF4A595D3BD22FAB34470F54235B8ACFB19EAE06C6571F99E103BE39F254843D181645C72E22223EFFA2418C2778CB6D5FFEDD427B8474517CACAAFFD5B717362E16E68F81F058713AC317A741D1415E59D0F1CAE0161BE5AAD53ED4DC2435A07F16CA4B3B569F8B7CD8F6D0D7221749E2B56C9254DE60A9FC824FEFE8522BBBF2C1C963C54BCF933A57B72B5AF15E9455F2103BD0E00455552F1A7BC6867685D92413D57DA8C"})
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
