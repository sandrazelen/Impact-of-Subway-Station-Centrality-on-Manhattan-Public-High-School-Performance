from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import Select
import time

url = "https://tools.nycenet.edu/snapshot/2023/01M015/EMS/"
DRIVER_PATH = "C:/Users/carol/Downloads/chromedriver-win64.zip/chromedriver-win64/chromedriver.exe"

options = Options()

driver = webdriver.Chrome()

driver.get(url)
#time.sleep(5)

try:
  # dropdown = driver.find_element(By.ID, 'select-school')
  #select = Select(dropdown)
  search_input = driver.find_element(By.XPATH, "//input[@placeholder='Type here to search for a school']")
  #search_input.send_keys("[HS]")
  #search_input.send_keys(Keys.RETURN)
  search_input.click()
  # firebug/equiv for Chrome
  # capture what's being sent back 
  # may need the mouse event onclick 
  results_list = WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.ID, 'autocomplete-results')))

  items = results_list.find_elements(By.CLASS_NAME, 'autocomplete-result')
  # html = driver.page_source

  # soup = BeautifulSoup(html, 'html.parser')

  for item in items:
    if '[HS]' in item.text:
      print(item.text)
      item.click()
      ratings = driver.find_elements(By.CLASS_NAME, 'v-middle content')
      for rating in ratings:
        print(rating.text)
      continue

    else:
      continue
    
except Exception as e:
  print(f"Failed: {e}")

driver.quit()