import time
import requests
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# Your 2Captcha API key
API_KEY = 'YOUR_2CAPTCHA_API_KEY'
SITE_KEY = 'YOUR_SITE_KEY'
URL = 'YOUR_WEBSITE_URL'

# Step 1: Set up the WebDriver
driver = webdriver.Chrome()  # or webdriver.Firefox(), etc.
driver.get(URL)

# Step 2: Request 2Captcha to solve the reCAPTCHA
def get_recaptcha_solution():
    # Send a request to 2Captcha
    response = requests.post('http://2captcha.com/in.php', {
        'key': API_KEY,
        'method': 'userrecaptcha',
        'googlekey': SITE_KEY,
        'pageurl': URL,
        'json': 1
    })
    
    result = response.json()
    
    if result['status'] == 1:
        captcha_id = result['request']
        return captcha_id
    else:
        print("Error in 2Captcha request:", result)
        return None

# Step 3: Wait for the solution
def wait_for_solution(captcha_id):
    while True:
        time.sleep(5)  # Wait before checking the solution
        response = requests.get(f'http://2captcha.com/res.php?key={API_KEY}&action=get&id={captcha_id}&json=1')
        result = response.json()
        
        if result['status'] == 1:
            return result['request']
        elif result['request'] != 'CAPTCHA_NOT_READY':
            print("Error:", result)
            return None

captcha_id = get_recaptcha_solution()
if captcha_id:
    token = wait_for_solution(captcha_id)
    print("Token received:", token)
    
    # Step 4: Enter the token into the hidden textarea
    driver.execute_script("document.getElementById('g-recaptcha-response').value = arguments[0];", token)
    
    # Now you can submit your form or proceed with the next steps
    # driver.find_element(By.ID, 'your_submit_button_id').click()

driver.quit()
