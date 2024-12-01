from selenium import webdriver
from anticaptchaofficial.recaptchav2proxyless import *
import time

# Initialize the Anti-Captcha service
solver = RecaptchaV2Proxyless()
solver.set_verbose(1)
solver.set_key("xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx")  # Replace with your API key

# Start the Selenium WebDrive

# Wait for the reCAPTCHA to appear
time.sleep(5)  # Adjust timing as needed

# Get the site key from the reCAPTCHA element
site_key = driver.find_element_by_xpath("//div[@class='g-recaptcha']").get_attribute("data-sitekey")

# Send the site key to Anti-Captcha and get the solution
solver.set_website_url(driver.current_url)
solver.set_website_key(site_key)
captcha_id = solver.create_task()
solver.join_task(captcha_id)

if solver.is_solved():
    token = solver.get_solution_response()
    print("Captcha solved, token:", token)

    # Enter the token into the reCAPTCHA response field
    driver.execute_script("document.getElementById('g-recaptcha-response').innerHTML = arguments[0];", token)
    driver.execute_script("document.getElementById('g-recaptcha-response').dispatchEvent(new Event('change'));")

    # Submit the form (adjust the selector as needed)
    driver.find_element_by_xpath("//form").submit()
else:
    print("Failed to solve captcha.")

# Close the driver
driver.quit()
