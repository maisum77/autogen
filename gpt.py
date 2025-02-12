from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.action_chains import ActionChains
import pyperclip
import time

# Set up Chrome options (optional)
chrome_options = webdriver.ChromeOptions()
chrome_options.add_argument("--start-maximized")

# Initialize the Chrome driver using webdriver_manager for ease
driver = webdriver.Chrome(
    service=Service(ChromeDriverManager().install()),
    options=chrome_options
)

# Open ChatGPT website
driver.get("https://randomwordgenerator.com/motivational-quote.php")
time.sleep(10)
try:
    element = driver.find_element(By.TAG_NAME, "span")
    extracted_text = element.text
    print("Extracted text:", extracted_text)
    pyperclip.copy(extracted_text)
    print("Text copied to clipboard!")
except Exception as e:
    print(f"An error occurred: {e}")

# Navigate to Twitter's login page
driver.get("https://x.com/i/flow/login")
time.sleep(3)  # Allow time for the login page to load

# Replace these with your actual Twitter credentials
twitter_username = "flowframe07@gmail.com"  # e.g., your email or Twitter handle
twitter_password = "Maisum06.me"

# Twitter’s login is a multi-step process.
# Step 2a: Enter the username.
username_field = WebDriverWait(driver, 20).until(
    EC.presence_of_element_located((By.NAME, "text"))
)
username_field.send_keys(twitter_username)
username_field.send_keys(Keys.ENTER)

# Step 2b: Wait for the password field and enter the password.
password_field = WebDriverWait(driver, 20).until(
    EC.presence_of_element_located((By.NAME, "password"))
)
# A short pause may help if the transition is not instantaneous.
time.sleep(2)
password_field.send_keys(twitter_password)
password_field.send_keys(Keys.ENTER)

# Optionally, wait until login is confirmed by checking for an element on the homepage.
# For example, waiting for the profile link to appear.
WebDriverWait(driver, 30).until(
    EC.presence_of_element_located((By.CSS_SELECTOR, "a[aria-label='Profile']"))
)
print("Logged in to Twitter.")

driver.get("https://twitter.com/compose/tweet")
time.sleep(3)  # Wait for the tweet composer to load

# Locate the tweet text area.
# Twitter’s tweet box typically uses a div with aria-label "Tweet text".
tweet_box = WebDriverWait(driver, 20).until(
    EC.presence_of_element_located((By.CSS_SELECTOR, "div[aria-label='Tweet text']"))
)

tweet_box.click()  # Focus the tweet box
action = ActionChains(driver)
action.key_down(Keys.CONTROL).send_keys('v').key_up(Keys.CONTROL).perform()


# Locate and click the Tweet button.
# The tweet button often has a data-testid attribute "tweetButtonInline".
tweet_button = WebDriverWait(driver, 20).until(
    EC.element_to_be_clickable((By.CSS_SELECTOR, "div[data-testid='tweetButtonInline']"))
)
tweet_button.click()
print("Tweet submitted.")



# Wait some time to view the results before closing the browser (adjust as needed)
time.sleep(15)
driver.quit()
