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
# options.add_argument('-headless')
options.add_argument("--disable-extensions")

driver = webdriver.Chrome(executable_path=driver_path,options=options)

# Get HTML Content of URL
driver.get("https://pokemonshowdown.com")
# driver.implicitly_wait(3)

# Alternative 1 (More complex)
# parent_element = driver.find_element(By.XPATH,"//section[@class='section']")
# parent_element = parent_element.find_element(By.XPATH,"//div[@class='right']")
# play_online_button = parent_element.find_element(By.XPATH,"//*[text()='Play online']")

# Alternative 2 (More Simple)
print(0)
play_online_button = driver.find_element(By.ID,"play-online")
print(1)
# play_online_button = WebDriverWait(driver, 1).until(EC.presence_of_element_located((By.ID,"play-online")))
print(2)
play_online_button = play_online_button.find_element(By.XPATH,"//*[text()='Play online']")
# play_online_button = play_online_button.find_element(By.XPATH,"//a")

href = (play_online_button.get_attribute("href"))
print(f"{href = }")
play_online_button.click()
print(5)
driver.quit()
