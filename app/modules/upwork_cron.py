import undetected_chromedriver as uc
import os

from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains


email = os.environ.get('UPWORK_USERNAME', None)
password = os.environ.get('UPWORK_PASSWORD', None) 
secret = os.environ.get('UPWORK_SECRET', None) 

try:
    options = uc.ChromeOptions()
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-blink-features=AutomationControlled")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("--disable-gpu")
    options.add_argument("--start-maximized")

    driver = uc.Chrome(options=options, version_main=138)

    driver.get("https://www.upwork.com/ab/account-security/login")

    # xpath = "//use[@href='/next_/icon.svg?v=1fd2d54#close']"
    # element = EC.visibility_of_element_located(By.XPATH, xpath)
    # element.click()
    # element.send_keys("my username")

    # Wait for email field and fill
    WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.ID, "login_username"))
    ).send_keys(email)

    # Click "Continue" button
    driver.find_element(By.ID, "login_password_continue").click()

    # Wait for password field and fill
    WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.ID, "login_password"))
    ).send_keys(password)

    # Submit login
    driver.find_element(By.ID, "login_control_continue").click()

    # Check for successful login (adjust selector as needed)
    time.sleep(5)
    if "feed" in driver.current_url:
        driver.quit()
        print( jsonify({"status": "success", "message": "Logged in successfully!"}) )
    else:
        driver.quit()
        print( jsonify({"status": "error", "message": "Login failed. Check credentials or CAPTCHA."}) )

except Exception as e:
    print( jsonify({"status": "error", "message": str(e)}) )