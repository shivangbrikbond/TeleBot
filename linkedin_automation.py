from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
import time
import os

def setup_driver():
    chrome_options = Options()
    chrome_options.add_argument("--start-maximized")
    chrome_options.add_experimental_option("detach", True)
    chrome_options.add_argument("--disable-infobars")
    chrome_options.add_argument("--disable-extensions")
    return webdriver.Chrome(options=chrome_options)

def add_cookies(driver, cookies):
    driver.get("https://www.linkedin.com")
    for cookie in cookies:
        driver.add_cookie(cookie)
    driver.get("https://www.linkedin.com/jobs/")
    WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CLASS_NAME, "jobs-search-box__text-input")))

def search_jobs(driver, search_keyword):
    keyword_search = driver.find_element(By.CLASS_NAME, "jobs-search-box__text-input")
    keyword_search.click()
    keyword_search.send_keys(search_keyword, Keys.ENTER)
    WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CLASS_NAME, 'search-reusables__filter-binary-toggle')))
    
    easy_apply_filter = driver.find_element(By.CLASS_NAME, 'search-reusables__filter-binary-toggle')
    easy_apply_filter.click()

def get_job_urls(driver):
    WebDriverWait(driver, 10).until(EC.presence_of_all_elements_located((By.CLASS_NAME, "jobs-search-results__list-item")))
    job_elements = driver.find_elements(By.CLASS_NAME, "jobs-search-results__list-item")
    current_job_url = driver.current_url
    current_job_id_value = current_job_url.split("currentJobId=")[1].split("&")[0]
    
    job_applications_url = []
    for job_element in job_elements:
        job_id = job_element.get_attribute("data-occludable-job-id")
        changed_url = current_job_url.replace(f"currentJobId={current_job_id_value}", f"currentJobId={job_id}")
        job_applications_url.append(changed_url)
    
    return job_applications_url

def handle_application(driver, resume_path):
    try:
        # Logic to handle text fields
        # e.g., finding inputs, entering data
        ...

        # Handle file upload for resume
        try:
            # Explicit wait for the file input to appear
            input_element = WebDriverWait(driver, 15).until(
                EC.presence_of_element_located((By.XPATH, "//input[@type='file']"))
            )
            input_element.send_keys(resume_path)  # Path to the resume
            print(f"Successfully uploaded resume from {resume_path}")

            # Additional logic for clicking buttons, submitting, etc.
            ...
        except TimeoutException:
            print("File input element not found within the time limit")

    except Exception as e:
        print(f"An error occurred while handling the application: {str(e)}")

def apply_to_jobs(driver, job_urls, resume_path):
    applied_jobs = []
    for job_url in job_urls:
        driver.get(job_url)
        try:
            easy_apply_button = driver.find_element(By.CLASS_NAME, 'jobs-apply-button--top-card')
            easy_apply_button.click()
            handle_application(driver, resume_path)
            applied_jobs.append(job_url)
            print(f"Applied to job: {job_url}")
            time.sleep(2)

        except Exception as e:
            print(f"Failed to apply to job {job_url}: {e}")

    return applied_jobs

def run_linkedin_automation(cookies, search_keyword, resume_path):
    driver = setup_driver()
    try:
        add_cookies(driver, cookies)
        search_jobs(driver, search_keyword)
        job_urls = get_job_urls(driver)
        applied_jobs = apply_to_jobs(driver, job_urls, resume_path)
        return f"Applied to {len(applied_jobs)} jobs on LinkedIn."
    except Exception as e:
        print(f"An error occurred: {e}")
    finally:
        driver.quit()