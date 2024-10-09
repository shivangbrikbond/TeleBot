from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import time

def setup_driver():
    chrome_options = Options()
    chrome_options.add_argument("--start-maximized")
    return webdriver.Chrome(options=chrome_options)

def add_cookies(driver, cookies):
    driver.get("https://internshala.com/")
    for cookie in cookies:
        driver.add_cookie(cookie)
    time.sleep(5)

def search_internships(driver, search_keyword):
    driver.get("https://internshala.com/internships/")
    search_box = driver.find_element(By.ID, "keywords")
    search_box.send_keys(search_keyword)
    search_box.send_keys(Keys.ENTER)
    time.sleep(5)

def apply_to_internships(driver):
    internships = driver.find_elements(By.CLASS_NAME, "internship_list_container")
    for internship in internships:
        apply_button = internship.find_element(By.CLASS_NAME, "apply_button")
        apply_button.click()
        time.sleep(2)
        print(f"Applied to internship: {internship.text}")

def run_internshala_automation(cookies, search_keyword):
    driver = setup_driver()
    add_cookies(driver, cookies)
    search_internships(driver, search_keyword)
    apply_to_internships(driver)
    driver.quit()