# ###########################
# ATTENTION! Zoho Mail has a limit for sent emails on free accounts. It blocks after around 50 emails.
# ###########################
# Install chromium and ChromeDriver (both have to be the same version)
# https://googlechromelabs.github.io/chrome-for-testing/
# move chrome-driver to /local/bin/chrome-driver
# for snap installed chromium give permissions: 
# sudo snap connect chromium:home
# sudo snap connect chromium:network
# sudo snap connect chromium:mount-observe
#
# pip install selenium
# 
# ###########################
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import random

email = 'your_email@example.com'
password = 'your_password'
mailing_list = ['mail1@example.com', 'mail2@example.com']

subject = 'Subject'
body = 'Body'

options = webdriver.ChromeOptions()
options.binary_location = "/snap/bin/chromium"
options.add_argument('--disable-dev-shm-usage')
options.add_argument('--no-sandbox')
options.add_argument('--remote-debugging-port=9222')
# Uncomment to run headlessly
# options.add_argument('--headless')

service = Service('/usr/local/bin/chromedriver')
driver = webdriver.Chrome(service=service, options=options)

try:
    wait = WebDriverWait(driver, 20)
    
    driver.get("https://accounts.zoho.eu/signin")
    
    wait.until(EC.presence_of_element_located((By.ID, "login_id")))
    time.sleep(3)
    driver.find_element(By.ID, "login_id").send_keys(email, Keys.RETURN)
    time.sleep(1)
    wait.until(EC.presence_of_element_located((By.ID, "password"))).send_keys(password, Keys.RETURN)
    
    wait.until(EC.url_contains("home"))
    
    for recipient in mailing_list:
        driver.get("https://mail.zoho.eu/zm/#compose")
        
        wait.until(EC.presence_of_element_located((By.XPATH, '//input[@aria-label="To Recipients"]'))).send_keys(recipient)
        
        wait.until(EC.presence_of_element_located((By.XPATH, '//input[@placeholder="Subject"]'))).click()
        wait.until(EC.presence_of_element_located((By.XPATH, '//input[@placeholder="Subject"]'))).send_keys(subject)
        
        iframe = wait.until(EC.presence_of_element_located((By.CLASS_NAME, 'ze_area')))
        driver.switch_to.frame(iframe)
        
        wait.until(EC.presence_of_element_located((By.XPATH, '//body'))).send_keys(body)
        driver.switch_to.default_content()
        
        wait.until(EC.element_to_be_clickable((By.XPATH, '//button[@data-tooltip="Send"]'))).click()
        
        wait.until(EC.url_contains("#mail"))
        print(f"Email sent to {recipient}.")
        time.sleep(2 * random.randint(1, 5))  # Add a delay to avoid triggering spam filters

finally:
    driver.quit()
