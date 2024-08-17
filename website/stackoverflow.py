# Learn How to locate the element where text is  (For example : Play Online)
# Normally you can
# 'driver.find_element(By.XPATH,"//*[text()='Play online']")'
# But this takes too long time, since it have to scrape all elements and check for the given text
# If the website is running for the long time, and print() does not show anything
# This means the driver is not quit, we have to make sure the previous session's driver is quit


import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# Make sure to install chromedriver.exe first
driver_path = r'C:\Program Files (x86)\chromedriver-win64\chromedriver.exe'

# Setup Driver
options = webdriver.ChromeOptions()
options.add_experimental_option('excludeSwitches', ['enable-logging'])
options.add_argument(r'--user-data-dir=C:\Users\Wallik\AppData\Local\Google\Chrome\User Data');
options.add_argument("--profile-directory=Default")
# options.add_argument('-headless')
options.add_argument("--disable-extensions")

driver = webdriver.Chrome(executable_path=driver_path,options=options)

# Get HTML Content of URL
driver.get("https://stackoverflow.com/")

# Maximum tolerance for waiting the element is 3 sec
driver.implicitly_wait(3)

print(0)
discover_button = driver.find_element(By.XPATH,"//*[text()='Discover Teams']")
buttonWrapper
href = (discover_button.get_attribute("href"))
print(f"{href = }")
discover_button.click()
print(1)
driver.quit()
