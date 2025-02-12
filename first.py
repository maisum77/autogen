import os
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
import time 
driver=webdriver.Chrome()
driver.get("https://jqueryui.com/resources/demos/progressbar/download.html")
driver.implicitly_wait(30)
my_element=driver.find_element(By.ID,'downloadButton')
my_element.click()
progress_element= driver.find_element(By.CLASS_NAME,'progress-label')
time.sleep(10)
driver.quit()