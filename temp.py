from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.action_chains import ActionChains
from selenium.common.exceptions import TimeoutException, NoSuchElementException
import pyperclip
import time
import logging

# Set up logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

class TwitterAutomation:
    def __init__(self, username, password):
        self.username = username
        self.password = password
        self.setup_driver()

    def setup_driver(self):
        """Initialize the Chrome driver with appropriate options"""
        chrome_options = webdriver.ChromeOptions()
        chrome_options.add_argument("--start-maximized")
        chrome_options.add_argument("--disable-notifications")
        
        try:
            self.driver = webdriver.Chrome(
                service=Service(ChromeDriverManager().install()),
                options=chrome_options
            )
            self.wait = WebDriverWait(self.driver, 20)
        except Exception as e:
            logging.error(f"Failed to initialize driver: {e}")
            raise

    def get_motivational_quote(self):
        """Fetch a motivational quote from the generator website"""
        try:
            self.driver.get("https://randomwordgenerator.com/motivational-quote.php")
            quote_element = self.wait.until(
                EC.presence_of_element_located((By.CSS_SELECTOR, ".support-sentence"))
            )
            quote_text = quote_element.text
            pyperclip.copy(quote_text)
            logging.info("Quote copied to clipboard")
            return quote_text
        except Exception as e:
            logging.error(f"Failed to get motivational quote: {e}")
            return None

    def login_to_twitter(self):
        """Handle Twitter login process"""
        try:
            self.driver.get("https://x.com/i/flow/login")
            
            # Enter username
            username_field = self.wait.until(
                EC.presence_of_element_located((By.NAME, "text"))
            )
            username_field.send_keys(self.username)
            username_field.send_keys(Keys.ENTER)
            
            # Enter password
            password_field = self.wait.until(
                EC.presence_of_element_located((By.NAME, "password"))
            )
            password_field.send_keys(self.password)
            password_field.send_keys(Keys.ENTER)
            
            # Wait for login confirmation
            self.wait.until(
                EC.presence_of_element_located((By.CSS_SELECTOR, "a[aria-label='Profile']"))
            )
            logging.info("Successfully logged in to Twitter")
            return True
        except TimeoutException:
            logging.error("Login timed out - check credentials or network connection")
            return False
        except Exception as e:
            logging.error(f"Login failed: {e}")
            return False

    def post_tweet(self, retries=3):
        """Post the tweet with retry mechanism"""
        for attempt in range(retries):
            try:
                # Navigate to tweet composer
                self.driver.get("https://twitter.com/compose/tweet")
                
                # Wait for and locate tweet box
                tweet_box = self.wait.until(
                    EC.presence_of_element_located((By.CSS_SELECTOR, "div[aria-label='Tweet text']"))
                )
                tweet_box.click()
                
                # Paste the copied text
                action = ActionChains(self.driver)
                action.key_down(Keys.CONTROL).send_keys('v').key_up(Keys.CONTROL).perform()
                
                # Click tweet button
                tweet_button = self.wait.until(
                    EC.element_to_be_clickable((By.CSS_SELECTOR, "div[data-testid='tweetButtonInline']"))
                )
                tweet_button.click()
                
                # Wait for tweet confirmation
                time.sleep(3)  # Brief wait to ensure tweet is posted
                logging.info("Tweet posted successfully")
                return True
            except Exception as e:
                logging.warning(f"Attempt {attempt + 1} failed: {e}")
                if attempt == retries - 1:
                    logging.error("All posting attempts failed")
                    return False
                time.sleep(2)  # Wait before retrying

    def cleanup(self):
        """Clean up resources"""
        try:
            self.driver.quit()
            logging.info("Browser closed successfully")
        except Exception as e:
            logging.error(f"Error during cleanup: {e}")

def main():
    # Replace with your credentials
    TWITTER_USERNAME = "flowframe07@gmail.com"
    TWITTER_PASSWORD = "Maisum06.me"
    
    bot = TwitterAutomation(TWITTER_USERNAME, TWITTER_PASSWORD)
    
    try:
        quote = bot.get_motivational_quote()
        if quote and bot.login_to_twitter():
            if bot.post_tweet():
                logging.info("Process completed successfully")
            else:
                logging.error("Failed to post tweet")
        else:
            logging.error("Failed to get quote or login")
    except Exception as e:
        logging.error(f"An unexpected error occurred: {e}")
    finally:
        bot.cleanup()

if __name__ == "__main__":
    main()