# https://github.com/2captcha/2captcha-python

import sys
import os
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

sys.path.append(os.path.dirname(os.path.dirname(os.path.realpath(__file__))))

from twocaptcha import TwoCaptcha

api_key = os.getenv('APIKEY_2CAPTCHA', 'xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx')

solver = TwoCaptcha(api_key)
def solveC():
  try:
    result = solver.recaptcha(
        sitekey='6LfD3PIbAAAAAJs_eEHvoOl75_83eXSqpPSRFJ_u',
        url='https://2captcha.com/demo/recaptcha-v2')

  except Exception as e:
      sys.exit(e)

  else:
      # sys.exit('solved: ' + str(result))
      return result

def main():

  try: 
    driverService = Service('/home/alaa/Downloads/chromedriver/chromedriver')

    driver = webdriver.Chrome(service=driverService)  #"]
    driver.get('https://2captcha.com/demo/recaptcha-v2')
    res = solveC()
    print(res)
    time.sleep(5)
    inp = driver.find_element(By.ID, 'g-recaptcha-response')
    print(0000)

    inp.send_keys(res)
    print(11111)
    check = driver.find_element(By.XPATH, '/html/body/div[1]/div[2]/main/div/div/div[2]/section/div/form/div[2]/button[1]')
    print(222222)
    check.click()
    input('enter')
  except Exception as e:
    sys.exit(e)

main()