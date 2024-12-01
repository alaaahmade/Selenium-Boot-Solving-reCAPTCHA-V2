from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
from twocaptcha import TwoCaptcha
import random
import string
import time
import phonenumbers
from phonenumbers import geocoder

# API Key for TwoCaptcha
API_KEY = 'YOUR_2CAPTCHA_API_KEY'
solver = TwoCaptcha(API_KEY)

# Chrome WebDriver Service
driver_service = Service('/home/alaa/Downloads/chromedriver/chromedriver')
driver = webdriver.Chrome(service=driver_service)

# Open the registration page
driver.maximize_window()
driver.get("https://mangoworldcar.com/ar/sign-up")

def generate_random_string(length=5, chars=string.ascii_lowercase):
    return ''.join(random.choice(chars) for _ in range(length))

def generate_random_email():
    return generate_random_string(8, string.ascii_letters) + "@gmail.com"

def remove_first_three_digits(number):
    return str(number)[2:]

def get_country_from_phone_number(phone_number):
    try:
        parsed_number = phonenumbers.parse('+' + phone_number, None)
        return geocoder.description_for_number(parsed_number, "en")
    except phonenumbers.NumberParseException:
        return "Invalid phone number"

def fill_form():
    # Accept terms and navigate to form
    try:
        check_box = WebDriverWait(driver, 5).until(
            EC.element_to_be_clickable((By.ID, 'terms-all'))
        )
        check_box.click()
        next_button = WebDriverWait(driver, 2).until(
            EC.element_to_be_clickable((By.XPATH, "//button[@type='button' and text()='التالي']"))
        )
        next_button.click()
    except Exception as e:
        print("Error clicking terms or next button:", e)

    # Fill user details
    try:
        WebDriverWait(driver, 2).until(
            EC.presence_of_element_located((By.NAME, 'userName'))
        ).send_keys(generate_random_string())

        email_input = WebDriverWait(driver, 2).until(
            EC.presence_of_element_located((By.NAME, 'email'))
        )
        email_input.send_keys(generate_random_email())

        password = generate_random_string(9)
        WebDriverWait(driver, 2).until(
            EC.presence_of_element_located((By.NAME, 'insertUserPW'))
        ).send_keys(password)

        WebDriverWait(driver, 2).until(
            EC.presence_of_element_located((By.NAME, 'compare_UserPW'))
        ).send_keys(password)
    except Exception as e:
        print("Error filling user details:", e)

    # Select phone country and number
    try:
        country_code_button = WebDriverWait(driver, 2).until(
            EC.element_to_be_clickable((By.ID, 'country-code'))
        )
        country_code_button.click()
        number = '3197010526434'
        country_name = get_country_from_phone_number(number)
        country_input = WebDriverWait(driver, 2).until(
            EC.presence_of_element_located((By.XPATH, "//input[@placeholder='الرجاء اختيار البلد']"))
        )
        country_input.send_keys(country_name)
        country_input.send_keys(Keys.RETURN)

        phone_input = WebDriverWait(driver, 2).until(
            EC.presence_of_element_located((By.NAME, "tel"))
        )
        phone_input.send_keys(remove_first_three_digits(number))
    except Exception as e:
        print("Error selecting country or entering phone:", e)

def solve_captcha():
    try:
        iframe = driver.find_element(By.XPATH, "//iframe[contains(@src, 'https://www.google.com/recaptcha/api2/anchor')]")
        site_key = iframe.get_attribute("src").split("k=")[1].split("&")[0]
        result = solver.recaptcha(sitekey=site_key, url=driver.current_url)
        captcha_solution = result['code']

        driver.execute_script("""
            document.getElementById('g-recaptcha-response').style.display = 'block';
            document.getElementById('g-recaptcha-response').value = arguments[0];
        """, captcha_solution)
        print("Captcha solved.")
    except Exception as e:
        print("Error solving CAPTCHA:", e)

def submit_form():
    try:
        submit_button = WebDriverWait(driver, 2).until(
            EC.element_to_be_clickable((By.XPATH, '/html/body/div[1]/form/div/div[3]/button[2]'))
        )
        submit_button.click()
        print("Form submitted.")
    except Exception as e:
        print("Error submitting form:", e)

try:
    fill_form()
    solve_captcha()
    submit_form()
except Exception as e:
    print(f"An error occurred: {e}")
finally:
    input("Press Enter to close the browser...")
    driver.quit()
