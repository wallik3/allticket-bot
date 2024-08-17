# USE MULTIPLE WINDOW INSTEAD OF MULTIPLE BROWSER (BUT NEED TO HANDLE RECAPTCHA FIRST)
from selenium import webdriver
# from selenium_recaptcha_solver import RecaptchaSolver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium_recaptcha_solver import RecaptchaSolver
import time
import json
from typing import Dict, List
from utils import generate_html_from_string
from selenium.webdriver.common.action_chains import ActionChains
from selenium.common.exceptions import ElementClickInterceptedException
import logging

# 1. HOW TO RECAPTCHA
# 2. HOW TO SELECT LEVEL WHICH AVAILABLE (CHENG RECOMMEND B OVER A)
# 3. SCRAPE THE SEAT WITH THE GIVEN PREDEFINED NUMBER 
# 4. DEAL WITH MONEY
# 5. TYPES ADDED TO FUNCTION

def get_user_json()->Dict:
    file_name = "user.json"
    with open(file_name,"r") as f:
        data = json.load(f)
    return data

def get_driver(profile="anonymous"):
    # Anonymous can be Default, Profile 1
    driver_path = r'C:\Program Files (x86)\chromedriver-win64\chromedriver.exe'
    
    options = webdriver.ChromeOptions()
    options.add_experimental_option('excludeSwitches', ['enable-logging'])
    options.add_argument("--disable-extensions")
    options.add_argument('--disable-blink-features=AutomationControlled')
    options.add_argument("start-maximized")
    if profile != "anonymous":
        options.add_argument(r'--user-data-dir=C:\Users\Wallik\AppData\Local\Google\Chrome\User Data');
        options.add_argument(f"--profile-directory={profile}")
        
    driver = webdriver.Chrome(driver_path, options=options)
    return driver

def get_all_child_element(parent_element):
    return parent_element.find_elements(By.XPATH,".//*")

def make_login(driver, recaptcha_solver, data:Dict):
    """Login from the allticket.com page
    
    Problem : Recaptcha is able to detect recaptcha_solver automation 
    Add manual way to let the user solve ReCAPTCHA
    
    Keyword arguments:
    driver
    data - Dictionary contains email, password
    Return: return_description
    """
    # Get into Email/Password Login system
    
    login_button = driver.find_element(by=By.ID, value="loginBtn")
    login_button.click()
    
    # Locate the element first
    email_login_textbox = driver.find_element(by=By.ID, value="email-login")
    password_login_textbox = driver.find_element(by=By.ID, value="password-login")
    signin_button = driver.find_element(By.XPATH, "//button[contains(@class, 'signin-button')]")
    
    # Fill element with data
    email_login_textbox.send_keys(data["email"])
    password_login_textbox.send_keys(data["password"])
    
    # Solve ReCAPTCHA
    recaptcha_iframe = WebDriverWait(driver, 5).until(EC.presence_of_element_located((By.XPATH, "//iframe[@title='reCAPTCHA']")))
    # WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, "//span[@id='recaptcha-anchor']"))).click()
    time.sleep(5)
    recaptcha_solver.click_recaptcha_v2(iframe=recaptcha_iframe)
    # Now do Selenium
    driver.switch_to.default_content()
    signin_button.click()


def reserve_seat_from_layout(app_seat_layout_element, 
                             limited_seat_num:int = 4, 
                             strategy="simple"):
    
    # Wait until seat layout appeared (For sit strategy)
    table_layout_element = app_seat_layout_element.find_element(By.TAG_NAME, "table")
    reserved_count = 0

    # Get all clickable seat element (Always have text inside svg)
    all_seat_xpath = "//tbody/tr/td/div"
    available_seat_xpath = all_seat_xpath+"/*[local-name() = 'svg']/*[local-name() = 'text']"
    available_seat_elements = table_layout_element.find_elements(By.XPATH, available_seat_xpath)
    # Loop though 
    for available_seat_element in available_seat_elements:
        # If no popup was found, then continue clicking
        try:
            available_seat_element.click()
            reserved_count += 1
            if reserved_count == limited_seat_num:
                break
        # If it reachs the limit
        except ElementClickInterceptedException as e:
            pass
        
# Setup logging to allow us to spot the bug
def main():
    logger = logging.getLogger(__name__)
    logging.basicConfig(filename=f'log/recent.log', encoding='utf-8', level=logging.DEBUG)

    data = get_user_json()
    
    # Avoid RECAPTCHA By logging in Google Profile
    chrome_profile = data["chrome_profile"]
    event_name = data['event_name']
    prior_seat_types = data.get("prior_seat_types",[])
    payment_method = data.get("payment_method","cash")
    driver = get_driver(profile=chrome_profile)
    
    # Setup the common wait
    wait = WebDriverWait(driver, 10)
    driver.implicitly_wait(3)

    # Now
    event_url = f"https://www.allticket.com/event/{event_name}"
    driver.get(event_url)

    # Start
    buy_button = driver.find_element(By.XPATH,"/html/body/app-root/app-event-info/div/div[2]/div[2]/div/div[5]/div/button")
    buy_button.click()

    # Read and Agree the condition
    generate_html_from_string(driver.page_source)

    accept_consent_checkbox = driver.find_element(By.CSS_SELECTOR, "label[for='acceptConsent']")
    accept_consent_checkbox.click()

    confirm_button = driver.find_element(By.XPATH, "//span[text()=' Confirm ']/parent::*")
    confirm_button.click()

    # Land to reserve page as Some concerts have more than 1 time, they will ask before to check seat available
    # TODO : If the confirmed button is still not done, then, it is possible that the popup window will be shown, Click yes to wait for a few minute

    time_index = data.get("time_index")
    if time_index:
        # Assume that there is time_index if it was provided
        select_time_container_xpath = "/html/body/app-root/app-booking/div[3]/div[1]"
        select_time_container = wait.until(EC.presence_of_element_located((By.XPATH, select_time_container_xpath)))
        select_time_button_xpath = f"{select_time_container_xpath}/div[{time_index+1}]/div/label"
        select_time_button_xpath = wait.until(EC.presence_of_element_located((By.XPATH, select_time_container_xpath)))
        select_time_button_xpath.click()

    # Performing Check Seat Available being shown
    check_seat_available_button_xpath = "//button[contains(text(),'CHECK SEAT AVAILABLE')]"
    check_seat_available_button = wait.until(EC.presence_of_element_located((By.XPATH, check_seat_available_button_xpath)))
    check_seat_available_button.click()

    # Now, all seats from each zone is being shown

    # Get Seat Available Container which containing 2 column : SEAT TYPE and Number of Available 
    seat_ava_container_xpath = '/html/body/app-root/app-booking/div[3]/div[2]/app-get-seat-available'
    seat_ava_container_element = wait.until(EC.presence_of_element_located((By.XPATH, seat_ava_container_xpath)))

    # Iterating all seats type via map image
    seat_ava_map_element = wait.until(EC.presence_of_element_located((By.ID, "zone")))
    seat_ava_map_element = seat_ava_map_element.find_element(By.XPATH,".//div/p/map")


    """
    seat_ava_map_element : 
        <area class="p_A1" coords="102,130,47,173,47,200,178,199,178,130" data-zone="A1" shape="poly">
        <area class="p_A2" coords="102,130,47,173,47,200,178,199,178,130" data-zone="A1" shape="poly">
    """

    # prior_seat_types = ["A1"]

    # Start by iterating in these seat type
    for prior_seat_type in prior_seat_types:
        seat_ava_prior_map_element = seat_ava_map_element.find_element(By.XPATH, f'.//*[@class="p_{prior_seat_type}"]')
        seat_ava_prior_map_element.click()


    # Wait until seat layout appeared (For sit strategy)

    # Click all
    app_seat_layout_element = wait.until(EC.presence_of_element_located((By.TAG_NAME, "app-seat-layout")))
    # Start reserving ticket from app seat layout element of that seat type 
    reserve_seat_from_layout(app_seat_layout_element)

    booking_button = driver.find_element(By.XPATH,"//span[contains(text(), 'Booking')]/parent::button")
    booking_button.click()

    # Now, looking for App summary
    wait = WebDriverWait(driver, 30)
    app_reserve_summary_element = wait.until(EC.presence_of_element_located((By.XPATH, "/html/body/app-root/app-reserve-summary"))) 

    # Select Payment method
    payment_method_index = {"cash" : 1, "promptpay" : 4}
    payment_method_xpath= f"//div[1]/div[2]/div[1]/div/div/div[2]/div[2]/div[{payment_method_index[payment_method]}]/label"
    payment_method_element = app_reserve_summary_element.find_element(By.XPATH,payment_method_xpath)
    payment_method_element.click()

    # Select Payment method
    payment_agree_button = driver.find_element(By.CSS_SELECTOR,"label[for='checkAgree']")
    payment_agree_button.click()

    booking_button = app_reserve_summary_element.find_element(By.XPATH,"//span[contains(text(), 'Payment')]/parent::button")
    booking_button.click()

    confirm_button = wait.until(EC.presence_of_element_located((By.XPATH, "//button[@class='swal2-confirm swal2-styled']"))) 
    confirm_button.click()

    # Not quit until.
    time.sleep(1000000)
    
    # driver.quit()

main()