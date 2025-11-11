# Selenium-based Email Fetcher
# Uses Chrome browser to access webmail (bypasses firewall blocking Python requests)

from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
import re
import time

class SeleniumEmailFetcher:
    def __init__(self, webmail_url="https://170.9.13.229/mail"):
        self.webmail_url = webmail_url
        self.driver = None

    def init_browser(self, headless=False):
        """Initialize Chrome browser"""
        try:
            options = Options()
            options.add_argument('--ignore-certificate-errors')
            options.add_argument('--ignore-ssl-errors')
            options.add_argument('--disable-blink-features=AutomationControlled')

            if headless:
                options.add_argument('--headless')

            service = Service(ChromeDriverManager().install())
            self.driver = webdriver.Chrome(service=service, options=options)
            return True
        except Exception as e:
            print(f"   [ERROR] Failed to init browser: {e}")
            return False

    def login(self, email, password):
        """Login to webmail via browser"""
        try:
            print(f"   Opening webmail: {self.webmail_url}")
            self.driver.get(self.webmail_url)
            time.sleep(3)

            # Find and fill login form
            print(f"   Logging in as {email}...")

            # Find email field
            email_field = WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located((By.NAME, "_user"))
            )
            email_field.clear()
            email_field.send_keys(email)

            # Find password field
            password_field = self.driver.find_element(By.NAME, "_pass")
            password_field.clear()
            password_field.send_keys(password)

            # Find and click login button
            login_button = self.driver.find_element(By.CSS_SELECTOR, "button[type='submit'], input[type='submit']")
            login_button.click()

            time.sleep(3)

            # Check if login successful (should see inbox or mail interface)
            if "mail" in self.driver.current_url.lower() or "inbox" in self.driver.page_source.lower():
                print("   [OK] Logged in successfully!")
                return True
            else:
                print("   [ERROR] Login failed - not redirected to inbox")
                return False

        except Exception as e:
            print(f"   [ERROR] Login error: {e}")
            return False

    def fetch_verification_code(self, max_attempts=18, wait_seconds=5):
        """Fetch TikTok verification code from inbox"""
        try:
            for attempt in range(max_attempts):
                try:
                    # Get inbox content
                    page_source = self.driver.page_source.lower()

                    # Check if there's a TikTok email
                    if 'tiktok' in page_source:
                        print(f"   [DEBUG] Found 'tiktok' in page!")

                        # Try to find clickable email rows
                        # Roundcube typically uses class="message" or similar for email rows
                        email_rows = self.driver.find_elements(By.CSS_SELECTOR, "tr.message, tr[id^='rcmrow'], .messagelist tr, tbody tr")

                        print(f"   [DEBUG] Found {len(email_rows)} email rows")

                        # Check each row for TikTok
                        for row in email_rows[-5:]:  # Check last 5 emails
                            row_text = row.text.lower()

                            if 'tiktok' in row_text or 'verification' in row_text:
                                print(f"   [DEBUG] Found TikTok email row, clicking...")

                                # Click to open the email
                                try:
                                    row.click()
                                except:
                                    # Try clicking a link inside
                                    try:
                                        link = row.find_element(By.TAG_NAME, "a")
                                        link.click()
                                    except:
                                        pass

                                time.sleep(2)

                                # Get the email content
                                email_content = self.driver.page_source

                                # Look for 6-digit code
                                code_match = re.search(r'\b(\d{6})\b', email_content)

                                if code_match:
                                    code = code_match.group(1)
                                    print(f"   [SUCCESS] Found code: {code}")
                                    return code
                                else:
                                    print(f"   [DEBUG] Email opened but no 6-digit code found")

                        # Try refreshing inbox
                        print(f"   [DEBUG] Refreshing inbox...")
                        self.driver.refresh()
                        time.sleep(2)

                    else:
                        print(f"   Waiting for email... (attempt {attempt + 1}/{max_attempts})")

                except Exception as e:
                    print(f"   [DEBUG] Error checking emails: {e}")

                # Wait before next attempt
                if attempt < max_attempts - 1:
                    time.sleep(wait_seconds)

            print(f"   [FAILED] No verification code found after {max_attempts} attempts")
            return None

        except Exception as e:
            print(f"   [ERROR] Error fetching code: {e}")
            return None

    def close(self):
        """Close browser"""
        try:
            if self.driver:
                self.driver.quit()
        except:
            pass


def get_verification_code_selenium(email, password, max_wait=90, headless=False):
    """
    Get verification code using Selenium (browser automation)
    This bypasses firewall issues by using the browser

    Args:
        email: Email address
        password: Email password
        max_wait: Max seconds to wait
        headless: Run browser in background (True) or visible (False)

    Returns:
        6-digit code or None
    """
    print(f"\n[EMAIL FETCHER] Using Selenium browser method for: {email}")

    fetcher = SeleniumEmailFetcher()

    if not fetcher.init_browser(headless=headless):
        return None

    if not fetcher.login(email, password):
        fetcher.close()
        return None

    max_attempts = max_wait // 5
    code = fetcher.fetch_verification_code(max_attempts=max_attempts, wait_seconds=5)

    fetcher.close()

    return code


# Test
if __name__ == "__main__":
    print("Testing Selenium Email Fetcher...")
    print("="*60)

    test_email = "eveline.ross@pumplabsweb3.com"
    test_password = "Welcome2025!"

    # Run in visible mode for testing
    code = get_verification_code_selenium(test_email, test_password, max_wait=30, headless=False)

    if code:
        print(f"\n[SUCCESS] Code: {code}")
    else:
        print("\n[FAILED] No code found")
