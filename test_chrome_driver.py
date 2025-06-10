from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.common.exceptions import WebDriverException
import time
import sys

def test_chrome_driver():
    try:
        # Print Python and Selenium versions
        print(f"Python version: {sys.version}")
        print(f"Selenium version: {webdriver.__version__}")
        
        # Configure Chrome options
        options = Options()
        options.add_argument("--headless")  # Remove this line to see the browser
        options.add_argument("--no-sandbox")
        options.add_argument("--disable-dev-shm-usage")
        
        # Initialize the Chrome WebDriver
        driver = webdriver.Chrome(options=options)
        
        # Test basic functionality
        print("\nTesting WebDriver functionality:")
        driver.get("https://www.realestate.com.au")
        print(f"Title: {driver.title}")
        print(f"Current URL: {driver.current_url}")
        
        # Test JavaScript execution
        print("\nTesting JavaScript execution:")
        js_result = driver.execute_script("return navigator.userAgent")
        print(f"User Agent: {js_result}")
        
        # Test page source
        print("\nTesting page source:")
        print(f"Page source length: {len(driver.page_source)} characters")
        
        time.sleep(2)
        driver.quit()
        print("\nTest completed successfully!")
        
    except WebDriverException as e:
        print(f"\nError: WebDriver failed to initialize: {str(e)}")
        sys.exit(1)
    except Exception as e:
        print(f"\nUnexpected error: {str(e)}")
        sys.exit(1)

if __name__ == "__main__":
    test_chrome_driver()
