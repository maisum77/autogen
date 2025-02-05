from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
import time
import os

def login_to_instagram(username, password):
    """
    Automates Instagram login process using Selenium WebDriver.
    
    Args:
        username (str): Instagram username
        password (str): Instagram password
    
    Returns:
        webdriver: Logged in browser session if successful
        None: If login fails
    """
    try:
        # Initialize the Chrome WebDriver
        driver = webdriver.Chrome()
        driver.maximize_window()
        
        # Navigate to Instagram login page
        driver.get('https://www.instagram.com/accounts/login/')
        
        # Wait for the page to load and cookie dialog to appear (if any)
        time.sleep(3)
        
        # Find and input username
        username_field = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.NAME, "username"))
        )
        username_field.send_keys(username)
        
        # Find and input password
        password_field = driver.find_element(By.NAME, "password")
        password_field.send_keys(password)
        
        # Click login button
        login_button = driver.find_element(By.XPATH, "//button[@type='submit']")
        login_button.click()
        
        # Wait for login to complete (checking for home feed)
        WebDriverWait(driver, 15).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, "svg[aria-label='Home']"))
        )
        
        print("Successfully logged in to Instagram!")
        return driver
        
    except TimeoutException:
        print("Error: Page elements took too long to load")
        if 'driver' in locals(): driver.quit()
        return None
        
    except NoSuchElementException:
        print("Error: Could not find expected page elements")
        if 'driver' in locals(): driver.quit()
        return None
        
    except Exception as e:
        print(f"An unexpected error occurred: {str(e)}")
        if 'driver' in locals(): driver.quit()
        return None

def upload_post(driver, image_path, caption):
    """
    Uploads an image to Instagram with a caption.
    
    Args:
        driver: Selenium WebDriver instance
        image_path (str): Full path to the image file
        caption (str): Caption for the post
    
    Returns:
        bool: True if successful, False otherwise
    """
    try:
        # Verify file exists
        if not os.path.exists(image_path):
            print(f"Error: File not found at {image_path}")
            return False

        # Click the "New Post" button (try multiple possible selectors)
        try:
            new_post_button = WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, "[aria-label='New post']"))
            )
        except:
            new_post_button = WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.XPATH, "//div[@role='menuitem']/*[name()='svg'][@aria-label='New post']"))
            )
        new_post_button.click()
        time.sleep(2)

        # Find and interact with file input
        file_input = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, "input[type='file']"))
        )
        file_input.send_keys(image_path)
        time.sleep(3)  # Wait for upload

        # Handle the crop/aspect ratio screen
        try:
            # Try to find and click the expand/crop button if it exists
            expand_crop_button = WebDriverWait(driver, 5).until(
                EC.presence_of_element_located((By.XPATH, "//button[contains(@aria-label, 'Select crop')]"))
            )
            expand_crop_button.click()
            time.sleep(1)
            
            # Select original aspect ratio
            original_ratio_button = WebDriverWait(driver, 5).until(
                EC.presence_of_element_located((By.XPATH, "//button[contains(@aria-label, 'Original')]"))
            )
            original_ratio_button.click()
            time.sleep(1)
        except:
            print("No crop adjustment needed or elements not found, continuing...")

        # Click Next for crop screen
        next_buttons = WebDriverWait(driver, 10).until(
            EC.presence_of_all_elements_located((By.XPATH, "//div[@role='button'][text()='Next']"))
        )
        next_buttons[0].click()
        time.sleep(2)

        # Click Next for filter screen
        try:
            filter_next = WebDriverWait(driver, 10).until(
                EC.element_to_be_clickable((By.XPATH, "//div[@role='button'][text()='Next']"))
            )
            filter_next.click()
            time.sleep(2)
        except:
            # If the filter screen is skipped, try alternate next button
            try:
                filter_next = WebDriverWait(driver, 10).until(
                    EC.element_to_be_clickable((By.XPATH, "//button[text()='Next']"))
                )
                filter_next.click()
                time.sleep(2)
            except:
                print("Could not find filter next button, attempting to continue...")

        # Add caption
        caption_input = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, "textarea[aria-label='Write a caption...']"))
        )
        caption_input.send_keys(caption)
        time.sleep(2)

        # Click Share
        share_buttons = WebDriverWait(driver, 10).until(
            EC.presence_of_all_elements_located((By.XPATH, "//div[@role='button'][text()='Share']"))
        )
        share_buttons[0].click()

        # Wait for post to be published
        time.sleep(10)
        print("Post uploaded successfully!")
        return True

    except Exception as e:
        print(f"Error uploading post: {str(e)}")
        return False

if __name__ == "__main__":
    # Replace with your Instagram credentials
    USERNAME = "noonehereexist007"
    PASSWORD = "maisum06.me"
    
    # Replace with your image path and caption
    IMAGE_PATH = r"C:\Users\only-\Downloads\iage to upload\DT39-F.jpg"  # Use raw string (r) to handle Windows paths
    CAPTION = "My awesome post! 📸✨ #instagram #selenium"
    
    # Login to Instagram
    browser = login_to_instagram(USERNAME, PASSWORD)
    
    if browser:
        # Upload the post
        success = upload_post(browser, IMAGE_PATH, CAPTION)
        
        # Wait a bit before closing
        time.sleep(5)
        browser.quit()