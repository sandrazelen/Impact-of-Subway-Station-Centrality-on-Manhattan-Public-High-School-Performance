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
import pandas as pd

url = "https://tools.nycenet.edu/dashboard/"
# not gonna change this for time's sake but possibly could make it faster to start from a url that's in borough view 
driver = webdriver.Chrome()
driver.get(url)

dictionary = {}
try:
  search_input = driver.find_element(By.XPATH, "//input[@placeholder='Type here to search for a school']")

  search_input.click()
  time.sleep(5)
  results_list = WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.ID, 'autocomplete-results')))

  items = results_list.find_elements(By.CLASS_NAME, 'autocomplete-result')
  hschools = []
  for item in items:
    if '[HS]' in item.text:
      hschools.append(item)
  
  df = pd.DataFrame(columns=['School Name', 'Collaborative Teachers', 'Effective School Leadership', 'Rigorous Instruction', 'Supportive Environment', 'Strong Family-Community Ties', 'Trust', 'Student Achievement'])

  for hs in hschools:
    name = hs.text
    hs.click()
    chart = WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.CLASS_NAME, "mod-db-framework-barh")))

    keys = ['School Name', 'Collaborative Teachers', 'Effective School Leadership', 'Rigorous Instruction', 'Supportive Environment', 'Strong Family-Community Ties', 'Trust', 'Student Achievement']
    values = [None] * 8
    values[0] = name
    svg = chart.find_element(By.CLASS_NAME, 'chart')

    scores = svg.find_elements(By.CLASS_NAME, "bar-value")
    time.sleep(2)

    n = 1
    for score in scores:
      values[n] = score.text
      n += 1
    
    dictionary = dict(zip(keys, values))
    # print(str(dictionary))
    df = df.append(dictionary, ignore_index=True) # outdated and will soon not work and need to be replaced w pd.concat(), also not worth changing rn though 
    df = df.reset_index(drop=True)
    search_input.click()

except Exception as e:
  print(f"Failed: {e}")

file_path = r"C:\Users\carol\OneDrive\Desktop\metrics.csv"
#print(df)
df.to_csv(file_path, index=False)

driver.quit()

print("Success!")
exit(0)
