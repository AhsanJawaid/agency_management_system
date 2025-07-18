import undetected_chromedriver as uc
import os, time
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver import ActionChains
from app.extensions import db
from app.models.job import Jobs

def import_upwork_jobs(user_email):
    email = os.getenv('UPWORK_USERNAME')
    password = os.getenv('UPWORK_PASSWORD')
    keywords = ["django", "vue.js", "firebase", "flask", "rest api", "socket.io"]

    try:
        options = uc.ChromeOptions()
        options.add_argument("--start-maximized")
        options.add_argument("--disable-blink-features=AutomationControlled")
        options.add_argument("--disable-gpu")
        options.add_argument("--no-sandbox")
        options.add_argument("--disable-dev-shm-usage")
        # options.add_argument("--headless=new")
        # options.add_argument("--window-size=1920,1080")

        driver = uc.Chrome(options=options, version_main=138, use_subprocess=False)
        wait = WebDriverWait(driver, 20)
        driver.execute_cdp_cmd("Page.addScriptToEvaluateOnNewDocument", {
            "source": "Object.defineProperty(navigator, 'webdriver', {get: () => undefined})"
        })

        driver.get("https://www.upwork.com/ab/account-security/login")
        wait.until(EC.element_to_be_clickable((By.ID, "login_username"))).send_keys(email)
        driver.find_element(By.ID, "login_password_continue").click()
        wait.until(EC.element_to_be_clickable((By.ID, "login_password"))).send_keys(password)
        driver.find_element(By.ID, "login_control_continue").click()
        time.sleep(4)
        try:
            close_btn = WebDriverWait(driver, 10).until(
                EC.element_to_be_clickable((By.CLASS_NAME, "modal-header-close-button"))
            )
            close_btn.click()
            time.sleep(1)
        except Exception:
            pass

        query = "+".join(keywords)
        query = "payment_verified=1&"+query

        try:
            fake_input = WebDriverWait(driver, 10).until(
                EC.element_to_be_clickable((By.CLASS_NAME, "air3-typeahead-input-fake"))
            )
            fake_input.click()
            time.sleep(1)

            # Now type into the real input
            real_input = WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.CLASS_NAME, "air3-input"))
            )
            real_input.send_keys(query)
            real_input.send_keys(Keys.ENTER)
        except Exception as e:
            print("Search field interaction failed:", str(e))
        

        # driver.get("https://www.upwork.com/nx/jobs/search/?q=django")
        # driver.get(f"https://www.upwork.com/nx/jobs/search/?q={query}")
        time.sleep(10)

        job_cards = driver.find_elements(By.CSS_SELECTOR, "section.up-card-section")[:10]
        imported = []

        for card in job_cards:
            try:
                title_elem = card.find_element(By.CSS_SELECTOR, "a.job-title")
                desc_elem = card.find_element(By.CSS_SELECTOR, "p[itemprop='description']")
                
                title = title_elem.text.strip()
                description = desc_elem.text.strip()
                url = title_elem.get_attribute("href")

                exists = Jobs.query.filter_by(title=title).first()
                if exists:
                    continue

                new_job = Jobs(
                    title=title,
                    description=description,
                    category='Upwork',
                    link=url
                )
                db.session.add(new_job)
                imported.append(title)
            except Exception:
                continue

        db.session.commit()
        driver.quit()

        return {"status": "success", "count": len(imported), "jobs": imported}
    except Exception as e:
        return {"status": "error", "message": str(e)}