from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
import time 
driver=webdriver.Chrome()
driver.get("https://www.instagram.com/accounts/login/?hl=en")
driver.implicitly_wait(5)
username=driver.find_element(By.NAME,'username')
username.send_keys("noonehereexist007")
time.sleep(10)
password=driver.find_element(By.NAME,'password')
password.send_keys("maisum06.me")
time.sleep(10)
submit=driver.find_element(By.XPATH, "//button[@type='submit']")
submit.click()
time.sleep(10)
driver.quit()