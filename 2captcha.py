from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
from twocaptcha import TwoCaptcha
import requests
import time
import random
import string
import phonenumbers
from phonenumbers import geocoder

def remove_first_three_digits(number):
    return str(number)[2:]

def get_country_from_phone_number(phone_number):
    try:
        parsed_number = phonenumbers.parse('+' + phone_number, None)
        country = geocoder.description_for_number(parsed_number, "en")
        return country
    except phonenumbers.NumberParseException:
        return "Invalid phone number"

def generate_random_name(length=5):
    letters = string.ascii_lowercase
    return ''.join(random.choice(letters) for _ in range(length))

def generate_random_email(length=8):
    letters = string.ascii_letters
    random_name = ''.join(random.choice(letters) for _ in range(length))
    return random_name + "@gmail.com"

# TwoCaptcha setup
api_key = 'YOUR_2CAPTCHA_API_KEY'
solver = TwoCaptcha(api_key)

driverService = Service('/home/alaa/Downloads/chromedriver/chromedriver')
driver = webdriver.Chrome(service=driverService)

driver.maximize_window()
driver.get("https://mangoworldcar.com/ar/sign-up")

try:
    # Accept terms and fill in form
    checkBox = WebDriverWait(driver, 2).until(EC.element_to_be_clickable((By.ID, 'terms-all')))
    if checkBox:
        checkBox.click()
        button = WebDriverWait(driver, 2).until(
            EC.element_to_be_clickable((By.XPATH, "//button[@type='button' and text()='التالي']"))
        )
        button.click()

    # Fill user details
    WebDriverWait(driver, 2).until(EC.presence_of_element_located((By.NAME, 'userName'))).send_keys(generate_random_name())
    email_input = WebDriverWait(driver, 1).until(EC.presence_of_element_located((By.NAME, 'email')))
    email = generate_random_email()
    email_input.send_keys(email)

    password = generate_random_name(9)
    WebDriverWait(driver, 1).until(EC.presence_of_element_located((By.NAME, 'insertUserPW'))).send_keys(password)
    WebDriverWait(driver, 1).until(EC.presence_of_element_located((By.NAME, 'compare_UserPW'))).send_keys(password)

    # Handle phone input and country selection
    number = '3197010526434'
    country_input = WebDriverWait(driver, 2).until(EC.presence_of_element_located((By.XPATH, "//input[@placeholder='الرجاء اختيار البلد']")))
    country_input.send_keys(get_country_from_phone_number(number))
    country_input.send_keys(Keys.RETURN)
    WebDriverWait(driver, 1).until(EC.presence_of_element_located((By.NAME, "tel"))).send_keys(remove_first_three_digits(number))

    # Retrieve CAPTCHA site key
    iframe = driver.find_element(By.XPATH, "//iframe[contains(@src, 'https://www.google.com/recaptcha/api2/anchor')]")
    site_key = iframe.get_attribute("src").split("k=")[1].split("&")[0]
    
    # Solve CAPTCHA with TwoCaptcha
    print("Solving CAPTCHA...")
    result = solver.recaptcha(sitekey=site_key, url="https://mangoworldcar.com/ar/sign-up")
    captcha_solution = result['code']
    print("Captcha solution obtained:", captcha_solution)
    
    # Inject CAPTCHA solution into the page
    driver.execute_script("""
        document.getElementById('g-recaptcha-response').style.display = 'block';
        document.getElementById('g-recaptcha-response').value = arguments[0];
    """, captcha_solution)

    # Submit the form
    submit_button = WebDriverWait(driver, 2).until(EC.element_to_be_clickable((By.XPATH, '/html/body/div[1]/form/div/div[3]/button[2]')))
    submit_button.click()

    print("Form submitted.")

except Exception as e:
    print(f"An error occurred: {e}")

finally:
    input("Press Enter to close the browser...")
    driver.quit()
