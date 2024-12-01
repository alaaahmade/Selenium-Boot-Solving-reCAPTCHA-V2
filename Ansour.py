from selenium import webdriver
from anticaptchaofficial.recaptchav2proxyless import *
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
import requests
import random
import string
import phonenumbers
from phonenumbers import geocoder
import time


def get_country_from_phone_number(phone_number):
    try:
        # Parse the phone number
        parsed_number = phonenumbers.parse('+' + phone_number, None)
        
        # Get the country name
        country = geocoder.description_for_number(parsed_number, "en")
        
        # Extract the country prefix and local number
        country_prefix = str(parsed_number.country_code)
        local_number = phone_number[len(country_prefix):]  # Remove the prefix from the full number
        
        # Return the formatted result as a dictionary
        result = {
            "number": local_number,
            "prefix": country_prefix,
            "country": country
        }
        
        return result
    except phonenumbers.NumberParseException:
        return {
            "number": None,
            "prefix": None,
            "country": "Invalid phone number"
        }

# Test the function with an example

# Function to generate random names, emails, and passwords
def generate_random_string(length, chars=string.ascii_lowercase):
    return ''.join(random.choice(chars) for _ in range(length))


def main(number):
    driver_path = '/home/alaa/Downloads/chromedriver/chromedriver'
    driver_service = Service(driver_path)
    driver = webdriver.Chrome(service=driver_service)
    driver.maximize_window()

    # Open the registration page
    driver.get("https://mangoworldcar.com/ar/sign-up")

    # Fill in the registration form
    try:
        # Accept terms
        print('checkBox')
        # checkBox = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.ID, 'terms-all')))
        # checkBox.click()
        
        # Click "Next" button after accepting terms
        # print('checkBox')

        # next_button = WebDriverWait(driver, 10).until(
        #     EC.element_to_be_clickable((By.XPATH, "//button[@type='button' and text()='التالي']"))
        # )
        # next_button.click()

        # Fill in username
        print('name_input')

        name_input = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.NAME, 'userName')))
        name_input.send_keys(generate_random_string(5))
        
        # Fill in email
        print('email_input')

        email_input = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.NAME, 'email')))
        email_input.send_keys(generate_random_string(8, string.ascii_letters) + "@gmail.com")
        
        # Fill in password and confirm password
        print('password_input')

        password = generate_random_string(9)
        password_input = driver.find_element(By.NAME, 'insertUserPW')
        print('confirm_password_input')

        confirm_password_input = driver.find_element(By.NAME, 'compare_UserPW')
        password_input.send_keys(password)
        confirm_password_input.send_keys(password)

        # Select country and enter phone number
        print('country_button')

        country_button = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.ID, 'country-code')))
        country_button.click()
        country_input = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.XPATH, "//input[@placeholder='الرجاء اختيار البلد']"))
        )
        coun = get_country_from_phone_number(number)
        print(coun)
        country_input.send_keys(coun['country'])  # Adjust as necessary

        time.sleep(5)
        if coun['country'] == 'Sudan':
            country_input.send_keys(Keys.ARROW_DOWN)
        
        country_input.send_keys(Keys.RETURN)
        print('phone_input')

        phone_input = driver.find_element(By.NAME, "tel")
        phone_input.send_keys(coun['number'])

        # Accept additional terms
        print('term_1')

        term_1 = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.XPATH, '/html/body/div[1]/form/div/div[2]/div[3]/p[1]'))
        )
        term_1.click()
        print('term_2')

        term_2 = driver.find_element(By.XPATH, '/html/body/div[1]/form/div/div[2]/div[3]/p[2]')
        term_2.click()

        # Solve CAPTCHA using 2Captcha API
        api_key = '0c0d9bfd5d0ed2f8dbf125219ca92b4a'
        iframe = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.XPATH, "//iframe[contains(@src, 'https://www.google.com/recaptcha/api2/anchor')]"))
        )
        src_url = iframe.get_attribute("src")
        site_key = src_url.split("k=")[1].split("&")[0]
        
        # Request CAPTCHA solution
        response = requests.post(
            'http://2captcha.com/in.php',
            data={
                'key': api_key,
                'method': 'userrecaptcha',
                'googlekey': site_key,
                'pageurl': driver.current_url,
                'json': 1
            }
        )
        request_id = response.json().get('request')

        # Poll for CAPTCHA solution
        solution = None
        while solution is None:
            time.sleep(3)
            print('waiting for solution ...')
            result = requests.get(
                'http://2captcha.com/res.php',
                params={'key': api_key, 'action': 'get', 'id': request_id, 'json': 1}
            )
            result_json = result.json()
            print(solution)
            if result_json.get('status') == 1:
                solution = result_json.get('request')

        # Inject CAPTCHA solution into the page
        driver.execute_script(
            "document.getElementById('g-recaptcha-response').style.display = 'block';"
            f"document.getElementById('g-recaptcha-response').value = '{solution}';"
        )
        
        # Click "Next" to complete registration
        verify_button = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, '/html/body/div[1]/form/div/div[3]/button[2]'))
        )
        verify_button.click()

        print("Registration complete.")

    except Exception as e:
        print(f"An error occurred: {e}")

    finally:
        time.sleep(8)
        # input("Press Enter to close the browser...")
        driver.quit()


def git_all_countries(file_path):
    with open(file_path, 'r') as file:
        numbers = file.readlines()
        for number in numbers:
            number = number.strip()
            if number.strip():  
                try:
                    main(number.strip())
                except requests.RequestException as e:
                    print(f"{number} is refused by website: {e}")


git_all_countries('numbers.txt')