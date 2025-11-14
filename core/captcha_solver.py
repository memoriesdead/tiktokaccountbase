# CAPTCHA Solver using CapMonster Cloud API
# Supports reCAPTCHA v2, v3, hCaptcha, FunCaptcha and more
# ONLY calls the API when a CAPTCHA is actually detected!

from capmonster_python import RecaptchaV2Task, RecaptchaV3Task, HCaptchaTask, FunCaptchaTask
import time
import os

class CaptchaSolver:
    """
    Handles automatic CAPTCHA solving using CapMonster Cloud API

    ⚡ COST-EFFICIENT: Only charges when captcha is actually triggered!
    ⚡ No pre-emptive calls - detects captcha first, then solves

    Get your API key from: https://capmonster.cloud/
    Dashboard: https://dash.capmonster.cloud/

    Pricing (as of 2025):
    - FunCaptcha (TikTok uses this): $0.60/1000 solves
    - reCAPTCHA v2: $1.00/1000 solves
    - hCaptcha: $1.00/1000 solves
    - reCAPTCHA v3: $1.00/1000 solves

    Only charged when CAPTCHA is successfully solved!
    """

    def __init__(self, api_key=None):
        """
        Initialize the CAPTCHA solver

        Args:
            api_key: Your CapMonster Cloud API key. If None, reads from environment variable CAPTCHA_API_KEY
        """
        self.api_key = api_key or os.getenv('CAPTCHA_API_KEY')

        if not self.api_key:
            raise ValueError("CapMonster API key not provided. Set CAPTCHA_API_KEY environment variable or pass api_key parameter.")

        print(f"✓ CapMonster Cloud initialized (API key: {self.api_key[:8]}...)")

        # CapMonster uses task-based API - instantiate tasks
        self.recaptcha_v2 = RecaptchaV2Task(self.api_key)
        self.recaptcha_v3 = RecaptchaV3Task(self.api_key)
        self.hcaptcha = HCaptchaTask(self.api_key)
        self.funcaptcha = FunCaptchaTask(self.api_key)

    def solve_recaptcha_v2(self, site_key, url):
        """
        Solve reCAPTCHA v2

        Args:
            site_key: The site key from the page (found in data-sitekey attribute)
            url: The URL of the page with CAPTCHA

        Returns:
            str: The CAPTCHA solution token
        """
        print(f"🔄 Solving reCAPTCHA v2 (CapMonster Cloud)...")

        try:
            task_id = self.recaptcha_v2.create_task(
                website_url=url,
                website_key=site_key
            )

            result = self.recaptcha_v2.join_task_result(task_id)
            token = result.get("gRecaptchaResponse")

            print(f"✓ CAPTCHA solved! Token: {token[:50]}...")
            return token

        except Exception as e:
            print(f"✗ CAPTCHA solving failed: {e}")
            return None

    def solve_recaptcha_v3(self, site_key, url, action='verify', min_score=0.3):
        """
        Solve reCAPTCHA v3

        Args:
            site_key: The site key from the page
            url: The URL of the page with CAPTCHA
            action: The action name (default: 'verify')
            min_score: Minimum score required (0.1 to 0.9)

        Returns:
            str: The CAPTCHA solution token
        """
        print(f"🔄 Solving reCAPTCHA v3 (CapMonster Cloud)...")

        try:
            task_id = self.recaptcha_v3.create_task(
                website_url=url,
                website_key=site_key,
                page_action=action,
                min_score=min_score
            )

            result = self.recaptcha_v3.join_task_result(task_id)
            token = result.get("gRecaptchaResponse")

            print(f"✓ CAPTCHA solved! Token: {token[:50]}...")
            return token

        except Exception as e:
            print(f"✗ CAPTCHA solving failed: {e}")
            return None

    def solve_hcaptcha(self, site_key, url):
        """
        Solve hCaptcha

        Args:
            site_key: The site key from the page
            url: The URL of the page with CAPTCHA

        Returns:
            str: The CAPTCHA solution token
        """
        print(f"🔄 Solving hCaptcha (CapMonster Cloud)...")

        try:
            task_id = self.hcaptcha.create_task(
                website_url=url,
                website_key=site_key
            )

            result = self.hcaptcha.join_task_result(task_id)
            token = result.get("gRecaptchaResponse")

            print(f"✓ CAPTCHA solved! Token: {token[:50]}...")
            return token

        except Exception as e:
            print(f"✗ CAPTCHA solving failed: {e}")
            return None

    def solve_funcaptcha(self, public_key, url, surl=None):
        """
        Solve FunCaptcha (Arkose Labs) - TikTok uses this!

        Args:
            public_key: The public key from the page
            url: The URL of the page with CAPTCHA
            surl: Service URL (optional)

        Returns:
            str: The CAPTCHA solution token
        """
        print(f"🔄 Solving FunCaptcha/Arkose Labs (CapMonster Cloud - $0.60/1k)...")

        try:
            task_params = {
                "website_url": url,
                "website_public_key": public_key
            }

            if surl:
                task_params["funcaptcha_api_js_subdomain"] = surl

            task_id = self.funcaptcha.create_task(**task_params)
            result = self.funcaptcha.join_task_result(task_id)
            token = result.get("token")

            print(f"✓ FunCaptcha solved! Token: {token[:50]}...")
            return token

        except Exception as e:
            print(f"✗ CAPTCHA solving failed: {e}")
            return None

    def get_balance(self):
        """
        Check your CapMonster Cloud account balance

        Returns:
            float: Account balance in USD
        """
        try:
            # CapMonster Cloud doesn't have a direct balance check in the Python library
            # You can check your balance at: https://dash.capmonster.cloud/
            print(f"💰 Check your balance at: https://dash.capmonster.cloud/")
            print(f"   (CapMonster Python library doesn't support balance checks)")
            return None
        except Exception as e:
            print(f"✗ Failed to get balance: {e}")
            return None


# Helper function for easy integration
def solve_tiktok_captcha(driver, api_key=None):
    """
    Automatically detect and solve CAPTCHA on TikTok signup page

    ⚡ COST-EFFICIENT: Only called when captcha is detected!
    ⚡ No pre-emptive API calls - only charges when solving

    Args:
        driver: Selenium WebDriver instance
        api_key: CapMonster Cloud API key (optional if set in environment variable CAPTCHA_API_KEY)

    Returns:
        bool: True if CAPTCHA was solved, False otherwise
    """
    try:
        solver = CaptchaSolver(api_key)
        current_url = driver.current_url

        # Check for reCAPTCHA v2
        try:
            recaptcha_frame = driver.find_elements("css selector", "iframe[src*='recaptcha']")
            if recaptcha_frame:
                print("🤖 Detected reCAPTCHA v2")

                # Find site key
                site_key = driver.execute_script("""
                    var elements = document.querySelectorAll('[data-sitekey]');
                    return elements.length > 0 ? elements[0].getAttribute('data-sitekey') : null;
                """)

                if site_key:
                    token = solver.solve_recaptcha_v2(site_key, current_url)

                    if token:
                        # Inject token into page
                        driver.execute_script(f"""
                            document.getElementById('g-recaptcha-response').innerHTML = '{token}';
                            if (typeof ___grecaptcha_cfg !== 'undefined') {{
                                ___grecaptcha_cfg.clients[0].callback('{token}');
                            }}
                        """)

                        print("✓ reCAPTCHA token injected!")
                        time.sleep(2)
                        return True
        except Exception as e:
            print(f"No reCAPTCHA v2 found: {e}")

        # Check for hCaptcha
        try:
            hcaptcha_frame = driver.find_elements("css selector", "iframe[src*='hcaptcha']")
            if hcaptcha_frame:
                print("🤖 Detected hCaptcha")

                # Find site key
                site_key = driver.execute_script("""
                    var elements = document.querySelectorAll('[data-sitekey]');
                    return elements.length > 0 ? elements[0].getAttribute('data-sitekey') : null;
                """)

                if site_key:
                    token = solver.solve_hcaptcha(site_key, current_url)

                    if token:
                        # Inject token into page
                        driver.execute_script(f"""
                            document.querySelector('[name="h-captcha-response"]').innerHTML = '{token}';
                            if (typeof hcaptcha !== 'undefined') {{
                                hcaptcha.submit();
                            }}
                        """)

                        print("✓ hCaptcha token injected!")
                        time.sleep(2)
                        return True
        except Exception as e:
            print(f"No hCaptcha found: {e}")

        # Check for FunCaptcha (TikTok often uses this)
        try:
            funcaptcha = driver.find_elements("css selector", "iframe[src*='arkose'], iframe[src*='funcaptcha']")
            if funcaptcha:
                print("🤖 Detected FunCaptcha (Arkose Labs)")

                # Find public key
                public_key = driver.execute_script("""
                    var elements = document.querySelectorAll('[data-public-key]');
                    return elements.length > 0 ? elements[0].getAttribute('data-public-key') : null;
                """)

                if public_key:
                    token = solver.solve_funcaptcha(public_key, current_url)

                    if token:
                        print("✓ FunCaptcha token obtained!")
                        # FunCaptcha tokens are usually submitted automatically
                        time.sleep(2)
                        return True
        except Exception as e:
            print(f"No FunCaptcha found: {e}")

        print("ℹ No CAPTCHA detected on current page")
        return False

    except Exception as e:
        print(f"✗ CAPTCHA solving error: {e}")
        return False


if __name__ == "__main__":
    print("=" * 60)
    print("CapMonster Cloud API Tester")
    print("=" * 60)
    print()

    # Test if API key is configured
    api_key = os.getenv('CAPTCHA_API_KEY')

    if not api_key:
        print("⚠ CAPTCHA_API_KEY not set in environment variables")
        print()
        print("To set it up:")
        print("1. Get API key from: https://capmonster.cloud/")
        print("2. View your key at: https://dash.capmonster.cloud/")
        print("3. Set environment variable:")
        print("   Windows CMD: set CAPTCHA_API_KEY=your_api_key_here")
        print("   Windows PowerShell: $env:CAPTCHA_API_KEY='your_api_key_here'")
        print("   Linux/Mac: export CAPTCHA_API_KEY=your_api_key_here")
        print()
        print("Or create a .env file with:")
        print("CAPTCHA_API_KEY=your_api_key_here")
        print()
        print("💰 Pricing:")
        print("   - FunCaptcha (TikTok): $0.60/1000 solves")
        print("   - reCAPTCHA v2: $1.00/1000 solves")
        print("   - hCaptcha: $1.00/1000 solves")
    else:
        try:
            solver = CaptchaSolver(api_key)
            print(f"✓ API key loaded: {api_key[:8]}...")
            print(f"✓ CapMonster Cloud initialized successfully!")
            print()
            print(f"💰 Check your balance at: https://dash.capmonster.cloud/")
            print(f"📊 View stats and usage: https://dash.capmonster.cloud/statistics")
            print()
            print("⚡ COST SAVINGS:")
            print("   - Only charged when CAPTCHA is successfully solved")
            print("   - No charge if captcha detection fails")
            print("   - No charge if solving fails")
            print()
            print("✓ Ready to solve captchas!")
        except Exception as e:
            print(f"✗ Error initializing CapMonster: {e}")
            print()
            print("Possible issues:")
            print("- Invalid API key")
            print("- capmonster-python not installed (pip install capmonster-python)")
            print("- Network connectivity issue")
