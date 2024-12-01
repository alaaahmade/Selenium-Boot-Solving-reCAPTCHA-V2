from selenium import webdriver
from anticaptchaofficial.recaptchav2proxyless import *
import requests
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.action_chains import ActionChains

import time
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys

import random
import string
import phonenumbers
from phonenumbers import geocoder

def remove_first_three_digits(number):
    return str(number)[2:]

def get_country_from_phone_number(phone_number):
    try:
        # Parse the phone number
        parsed_number = phonenumbers.parse('+' + phone_number, None)
        country = geocoder.description_for_number(parsed_number, "en")
        return country
    except phonenumbers.NumberParseException:
        return "Invalid phone number"

def generate_random_name(length=5):
    letters = string.ascii_lowercase  # Use lowercase letters
    random_name = ''.join(random.choice(letters) for _ in range(length))
    return random_name

def generate_random_email(length=8):
    letters = string.ascii_letters  # Use lowercase letters
    random_name = ''.join(random.choice(letters) for _ in range(length))
    random_domain = "@gmail.com"
    return random_name + random_domain

driverService = Service('/home/alaa/Downloads/chromedriver/chromedriver')

driver = webdriver.Chrome(service=driverService)  #"]
# driver = webdriver.Chrome(ChromeDriverManager().install())

driver.maximize_window()
driver.get("https://mangoworldcar.com/ar/sign-up")    

try:
    try:
        checkBox = WebDriverWait(driver, 2).until(
            EC.element_to_be_clickable((By.ID, 'terms-all'))
        )
        if checkBox :
            checkBox.click()
            button = WebDriverWait(driver, 2).until(
                EC.element_to_be_clickable((By.XPATH, "//button[@type='button' and text()='التالي']"))
            )
            button.click()
    except:
        print('gooo')

    nInput = WebDriverWait(driver, 2).until(
        EC.presence_of_element_located((By.NAME, 'userName'))
    )
    nInput.clear()
    nInput.send_keys(generate_random_name()) 

    eInput = WebDriverWait(driver, 1).until(
        EC.presence_of_element_located((By.NAME, 'email'))
    )

    eInput.clear()
    emaile = generate_random_email()
    print(emaile)
    eInput.send_keys(emaile)  

    PInput = WebDriverWait(driver, 1).until(
        EC.presence_of_element_located((By.NAME, 'insertUserPW'))
    )
    password = generate_random_name(9)
    PInput.clear()
    print('password:', password)
    PInput.send_keys(password)

    CpInput = WebDriverWait(driver, 1).until(
        EC.presence_of_element_located((By.NAME, 'compare_UserPW'))
    )
    CpInput.clear()
    CpInput.send_keys(password)

    time.sleep(2)

    try:
        Button = WebDriverWait(driver, 1).until(
        EC.presence_of_element_located((By.ID, 'country-code'))
        )
        Button.click()
        number = '3197010526434'
        country_input = WebDriverWait(driver, 2).until(
            EC.presence_of_element_located((By.XPATH, "//input[@placeholder='الرجاء اختيار البلد']"))
        )
        if country_input:
            country_input.click()
            country = get_country_from_phone_number(number)
            print(country)
            CPUinput = WebDriverWait(driver, 2).until(
            EC.presence_of_element_located((By.XPATH, '//*[@id="country-code"]'))
            )
            country_input.send_keys(country)
            time.sleep(4)
            country_input.send_keys(Keys.RETURN)
            PoneInput = WebDriverWait(driver, 0 ).until(
            EC.presence_of_element_located((By.NAME, "tel"))
            )
            PoneInput.clear()
            PoneInput.send_keys(remove_first_three_digits(number))
            time.sleep(0.2)
    except Exception as e:
        print('select country::', e)

    try:
        accept_term_1 = WebDriverWait(driver, 2).until(
            EC.presence_of_element_located((By.XPATH, '/html/body/div[1]/form/div/div[2]/div[3]/p[1]'))
        )
        if accept_term_1 :
            accept_term_1.click()

        accept_term_2 = WebDriverWait(driver, 2).until(
            EC.presence_of_element_located((By.XPATH, '/html/body/div[1]/form/div/div[2]/div[3]/p[2]'))
        )
        if accept_term_2 :
            accept_term_2.click()

    except:
        print('accepted terms')
    time.sleep(2)

    try: 
        #/html/body/div[5]/div[3]/button
        close_button = WebDriverWait(driver, 2 ).until(
        EC.presence_of_element_located((By.XPATH, "/html/body/div[5]/div[3]/button"))
    )
        if close_button:
            close_button.click()
            time.sleep(1)
    except:
        print('close terms')


    time.sleep(2)
    api_key = 'xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx'
    url = 'https://mangoworldcar.com/ar/sign-up'  

    # Add delay to ensure the page loads completely
    time.sleep(5)

    # Find and extract the site_key from the iframe
    iframe = driver.find_element(By.XPATH, "//iframe[contains(@src, 'https://www.google.com/recaptcha/api2/anchor')]")
    src_url = iframe.get_attribute("src")
    site_key = src_url.split("k=")[1].split("&")[0]
    print("Site Key found in iframe:", site_key) 
    driver.switch_to.default_content()

    # Send the initial request to 2Captcha
    response = requests.post(
        'http://2captcha.com/in.php',
        data={
            'key': api_key,
            'method': 'userrecaptcha',
            'googlekey': site_key,
            'pageurl': url,
            'json': 1
        }
    )

    # Parse the initial response and check for errors
    response_json = response.json()
    print("2Captcha Initial Response:", response_json)  # Print response for debugging

    if response_json.get('status') == 1:
        request_id = response_json.get('request')
        print("Request ID:", request_id)  # Confirm we received the request ID
    else:
        print("Error in 2Captcha request:", response_json)  # Print error details
        # driver.quit()
        exit()

    # # Poll for the solution
    solution = None
    while solution is None:
        time.sleep(10)  # Add a delay between requests to avoid frequent polling
        result = requests.get(
            'http://2captcha.com/res.php',
            params={'key': api_key, 'action': 'get', 'id': request_id, 'json': 1}
        )
        result_json = result.json()
        print("Captcha Polling Response: true")  # Print each polling response

        if result_json.get('status') == 1:
            solution = result_json.get('request')
        elif result_json.get('status') == 0:
            print("Solution not ready yet. Retrying...")
        else:
            print("Error with 2Captcha response:", result_json)
            break  # Exit loop if there's an error

    if solution:
        print(f"Captcha solution: {'solution'}")
        time.sleep(5)
        wait = WebDriverWait(driver, 10)
        form = driver.find_element(By.XPATH, '/html/body/div[1]/form')

        recaptcha_textarea = wait.until(EC.presence_of_element_located((By.XPATH, "/html/body/div[1]/form/div/div[2]/div[2]/div[1]/div[2]/div[4]/div/div/div/textarea")))
        print(1111, recaptcha_textarea.tag_name)
        ActionChains(driver).move_to_element(recaptcha_textarea).perform()
        print(218)
        # Now interact with the textarea
        driver.execute_script("""
            var element = document.querySelector("textarea#g-recaptcha-response");
            element.style.display = 'block';  // Ensure it's displayed if hidden
            element.value = arguments[0];  // Set the value of the textarea
        """, solution)
        print(225)




        # Submit the form using JavaScript to bypass interactability issues
        form_element = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.XPATH, "/html/body/div[1]/form"))
        )
        print(234)

        print("Submitting the form...")
        next = WebDriverWait(driver, 1).until(
        EC.presence_of_element_located((By.XPATH, '/html/body/div[1]/form/div/div[3]/button[2]'))
    )
        print(240)
        
        next.click()

        try: 
        #/html/body/div[5]/div[3]/button
            close_button = WebDriverWait(driver, 2 ).until(
            EC.presence_of_element_located((By.XPATH, "/html/body/div[5]/div[3]/button"))
        )
            if close_button:
                close_button.click()
                time.sleep(1)
        except:
            print('close terms')

    else:
        print("Failed to get CAPTCHA solution.")

    # Clean up
    driver.delete_all_cookies()

except Exception as e:
    print(f"An error occurred: {e}")

input("Press Enter to close the browser...")
driver.quit()
