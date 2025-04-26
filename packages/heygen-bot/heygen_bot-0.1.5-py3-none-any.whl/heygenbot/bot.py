from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
import time


class HeygenBot:
    """
    A bot to automate video creation tasks on Heygen using Selenium.

    Features:
    - Logs in using a session cookie
    - Navigates to the video creation interface
    - Automates script input, avatar selection, title setting, and video submission

    Usage:
    bot = HeygenBot(chromedriver_path, session_cookie_value)
    bot.login()
    bot.verify_login()
    bot.create_video(script_text, avatar_name="Karma", video_title="Demo")
    bot.close()
    """

    def __init__(self, chromedriver_path, session_cookie_value):
        self.options = Options()
        self.options.add_argument("--no-sandbox")
        self.options.add_argument("--disable-dev-shm-usage")
        self.options.add_argument("--headless=new")  # 'new' for Chrome 109+
        self.options.add_argument("--disable-gpu")
        self.options.add_argument("--window-size=1920,1080")
        self.options.add_argument("--start-maximized")
        self.driver = webdriver.Chrome(service=Service(chromedriver_path), options=self.options)
        self.cookie = {
            "name": "heygen_session",
            "value": session_cookie_value,
            "domain": ".heygen.com",
            "path": "/",
            "httpOnly": True,
            "secure": True
        }

    def login(self):
        self.driver.get("https://www.heygen.com")
        time.sleep(2)
        self.driver.add_cookie(self.cookie)
        self.driver.get("https://app.heygen.com/home")
        print("✅ Logged in using heygen-session cookie.")

    def verify_login(self):
        try:
            verify_btn = WebDriverWait(self.driver, 10).until(
                EC.element_to_be_clickable((By.XPATH, "//button[contains(text(), 'Verify')]"))
            )
            verify_btn.click()
            print("✅ Clicked verify button")
        except:
            print("❌ No verify button found or already passed")

    def create_video(self, script_text, avatar_name="Karma", video_title="Task 12"):
        self.driver.get("https://app.heygen.com/create-v3/")
        print("✅ Opened Create Video page")
        time.sleep(2)

        try:
            WebDriverWait(self.driver, 10).until(
                EC.element_to_be_clickable((By.XPATH, "//*[contains(text(), 'Script')]"))
            ).click()
            print("✅ Clicked on 'Scripts'")
        except Exception as e:
            print(f"❌ Failed to click on 'Scripts': {e}")

        try:
            WebDriverWait(self.driver, 10).until(
                EC.element_to_be_clickable((By.XPATH, "//*[contains(text(), 'Add Script')]"))
            ).click()
            print("✅ Clicked on 'Add Script'")
        except Exception as e:
            print(f"❌ Failed to click on 'Add Script': {e}")

        try:
            editable_box = WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, "div[contenteditable='true']"))
            )
            editable_box.click()
            editable_box.send_keys(Keys.CONTROL + "a")
            editable_box.send_keys(Keys.BACKSPACE)
            editable_box.send_keys(script_text)
            print("✅ Script added")
        except Exception as e:
            print(f"❌ Script input failed: {e}")

        time.sleep(10)  # Wait for the script to be processed

        for name in ["Avatar", avatar_name]:
            try:
                WebDriverWait(self.driver, 15).until(
                    EC.element_to_be_clickable((By.XPATH, f"//*[contains(text(), '{name}')]"))
                ).click()
                print(f"✅ Clicked on item containing '{name}'")
            except Exception as e:
                print(f"❌ Failed to click on '{name}': {e}")
        
        try:
            # Wait until an element containing 'Karma' is clickable
            karma_element = WebDriverWait(self.driver, 15).until(
                EC.element_to_be_clickable((By.XPATH, "//*[contains(text(), 'Hyper-Realistic')]"))
            )
            karma_element.click()
            print("✅ Clicked on item containing 'Video added'")
        except Exception as e:
            print(f"❌ Failed to click on 'Karma': {e}")  
        time.sleep(2)

        try:
            label_element = WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located((By.XPATH, "//*[contains(text(), 'Untitled Video')]"))
            )
            parent = label_element.find_element(By.XPATH, "..")
            try:
                input_box = parent.find_element(By.TAG_NAME, "input")
            except:
                input_box = parent.find_element(By.CSS_SELECTOR, "div[contenteditable='true']")
            input_box.click()
            input_box.send_keys(Keys.CONTROL + "a")
            input_box.send_keys(Keys.BACKSPACE)
            input_box.send_keys(video_title)
            print(f"✅ Video renamed to '{video_title}'")
        except Exception as e:
            print(f"❌ Failed to rename video: {e}")

        try:
            WebDriverWait(self.driver, 10).until(
                EC.element_to_be_clickable((By.XPATH, "//button[contains(., 'Submit')]"))
            ).click()
            print("✅ Clicked 'Submit'")
        except Exception as e:
            print(f"❌ Submit failed: {e}")

        try:
            popup = WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located((By.XPATH, "//*[contains(text(), 'Submit Video')]"))
            )
            modal = popup.find_element(By.XPATH, "./ancestor::div[contains(@class, 'Dialog') or contains(@class, 'modal') or @role='dialog']")
            
            submit_button = modal.find_element(By.XPATH, ".//button[contains(., 'Submit')]")
            self.driver.execute_script("arguments[0].click();", submit_button)
            print("✅ Confirmed 'Submit' in popup")
        except Exception as e:
            print(f"❌ Final submission failed: {e}")


    def save_video(self):
       
        self.driver.get("https://app.heygen.com/projects")
        print("✅ Opened Create Video page")

        time.sleep(5)
        # Try printing out thumbnails
        # Step 2: Wait for hover-visible menu to appear
        # Step 2: Wait for the hover-visible container to show up
        wait = WebDriverWait(self.driver, 15)
        from selenium.webdriver.common.action_chains import ActionChains
        try:
            # STEP 1: Find all video cards
            video_cards = self.driver.find_elements(By.CLASS_NAME, "video-card")
            if not video_cards:
                raise Exception("❌ No video cards found")

            # STEP 2: Get the first video card
            first_video_card = video_cards[0]

            # STEP 3: Find <img> inside that card and extract src
            img_tag = first_video_card.find_element(By.TAG_NAME, "img")
            img_src = img_tag.get_attribute("src")

            if not img_src:
                raise Exception("❌ No <img src> found inside video card")

            # STEP 4: Extract file name from image URL
            file_name_with_ext = img_src.split("/")[-1]
            file_name = ".".join(file_name_with_ext.split(".")[:-1])
            print("📁 File Name:", file_name)

            # STEP 5: Build video URL and navigate
            video_url = f"https://app.heygen.com/videos/{file_name}"
            print("🔗 Navigating to:", video_url)
            self.driver.get(video_url)

        except Exception as e:
            print("❌ Error:", e)
            
        time.sleep(2)

        try:
                # Find first download icon (top right or wherever)
                download_icons = wait.until(EC.presence_of_all_elements_located(
                    (By.XPATH, "//iconpark-icon[@name='download']")
                ))

                if len(download_icons) < 1:
                    raise Exception("❌ No first download icon found.")

                first_icon_parent = download_icons[0].find_element(By.XPATH, "./ancestor::button | ./..")
                first_icon_parent.click()
                print("✅ Clicked first Download icon (opened dropdown)")

                time.sleep(1)  # short wait for dropdown menu

                # Find second download icon inside the dropdown
                download_icons_after_dropdown = self.driver.find_elements(By.XPATH, "//iconpark-icon[@name='download']")
                if len(download_icons_after_dropdown) < 2:
                    raise Exception("❌ No second download icon found inside dropdown.")

                second_icon_parent = download_icons_after_dropdown[1].find_element(By.XPATH, "./ancestor::button | ./..")
                second_icon_parent.click()
                print("✅ Clicked second Download icon (download started!)")

                time.sleep(10)  # wait for download to start

        except Exception as e:
            print("❌ Download step failed:", e)
     


    def close(self, delay=60):
        """
        Close the browser window after a specified delay.

        Parameters:
        delay (int or float): Number of seconds to wait before quitting the browser.
                             Set to 0 for immediate shutdown.
        """
        if delay > 0:
            time.sleep(delay)
        self.driver.quit()
