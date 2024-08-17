from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
import time

# Setup Driver
options = webdriver.ChromeOptions()
# options.add_argument('--headless')
options.add_argument("--no-sandbox");
options.add_argument("--disable-dev-shm-usage"); 
options.add_argument('--remote-debugging-pipe')
options.add_experimental_option('excludeSwitches', ['enable-logging'])

# CHeckout  how to add the user to the chrome test
# options.add_argument(r'--user-data-dir=C:\Users\Wallik\AppData\Local\Google\Chrome\User Data');
# options.add_argument("--profile-directory=Default")
options.add_argument("--disable-extensions")

# options.add_argument("--disable-gpu");
# https://github.com/SeleniumHQ/selenium/issues/12841

driver = webdriver.Chrome(options=options)

# Get URL
driver.get("https://www.selenium.dev/selenium/web/web-form.html")
title = driver.title
print(f"{title = }")
driver.implicitly_wait(500)
# time.sleep(10000)

wait = WebDriverWait(driver, timeout=2)
wait.until(lambda d : revealed.is_displayed())

text_box = driver.find_element(by=By.NAME, value="my-text")
print(f"{text_box = }")

submit_button = driver.find_element(by=By.CSS_SELECTOR, value="button")


text_box.send_keys("Selenium")
submit_button.click()

message = driver.find_element(by=By.ID, value="message")
text = message.text
print(f"{text = }")

driver.quit()