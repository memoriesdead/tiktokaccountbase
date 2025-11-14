# -*- coding: utf-8 -*-
# TikTok Account Creator - Playwright CDP Version
# Connects to YOUR Chrome browser via Chrome DevTools Protocol
# Works with Chrome 136+ (2025)

import sys
import io
import os
import time
import pandas as pd
import csv
import re
import random

# Fix Windows console encoding
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')

from playwright.sync_api import sync_playwright, TimeoutError as PlaywrightTimeout

# ==================== CONFIGURATION ====================
MAX_BATCH_SIZE = 50
EMAIL_FETCH_DELAY = 5
ACCOUNT_DELAY = 3
# =======================================================

# Import email fetcher
EMAIL_AUTO_FETCH = False
get_verification_code = None

try:
    sys.path.insert(0, '..')
    from core.email_fetcher_selenium import get_verification_code_selenium
    get_verification_code = lambda email, password, max_wait: get_verification_code_selenium(email, password, max_wait, headless=True)
    EMAIL_AUTO_FETCH = True
    EMAIL_FETCH_METHOD = "Selenium (browser)"
except ImportError:
    try:
        from email_fetcher_selenium import get_verification_code_selenium
        get_verification_code = lambda email, password, max_wait: get_verification_code_selenium(email, password, max_wait, headless=True)
        EMAIL_AUTO_FETCH = True
        EMAIL_FETCH_METHOD = "Selenium (browser)"
    except ImportError:
        EMAIL_AUTO_FETCH = False
        EMAIL_FETCH_METHOD = "None"
        print("WARNING: Email auto-fetch not available")

def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')

def load_accounts():
    try:
        accounts_path = 'accounts.xlsx' if os.path.exists('accounts.xlsx') else '../accounts.xlsx'
        df = pd.read_excel(accounts_path)
        accounts = []
        for _, row in df.iterrows():
            accounts.append({
                'firstName': row['First Name'],
                'lastName': row['Last Name'],
                'email': row['email'],
                'password': row['password']
            })
        return accounts
    except FileNotFoundError:
        print("Error: accounts.xlsx file not found!")
        sys.exit(1)
    except Exception as e:
        print(f"Error reading Excel file: {str(e)}")
        sys.exit(1)

def get_processed_emails():
    if os.path.exists('processed_accounts.txt'):
        with open('processed_accounts.txt', 'r') as f:
            return set(line.strip() for line in f)
    return set()

def mark_email_processed(email):
    with open('processed_accounts.txt', 'a') as f:
        f.write(email + '\n')

def save_to_csv(account, success=True, notes=""):
    csv_file = 'created_accounts.csv'
    file_exists = os.path.exists(csv_file)

    with open(csv_file, 'a', newline='', encoding='utf-8') as f:
        writer = csv.writer(f)
        if not file_exists:
            writer.writerow(['First Name', 'Last Name', 'Email', 'Password', 'Status', 'Notes', 'Timestamp'])
        writer.writerow([
            account['firstName'],
            account['lastName'],
            account['email'],
            account['password'],
            'Success' if success else 'Failed',
            notes,
            time.strftime('%Y-%m-%d %H:%M:%S')
        ])

def human_type(element, text):
    """Type text character-by-character with human-like delays"""
    for char in str(text):
        element.type(char)
        time.sleep(random.uniform(0.1, 0.4))

def logout_tiktok(page):
    """Log out from TikTok account"""
    try:
        print("  → Looking for profile/settings menu...")

        # Method 1: Click on profile icon in top right
        try:
            # Look for the hamburger menu (three dots) in top right
            menu_button = page.locator("div[data-e2e='user-avatar'], button[aria-label*='Profile' i], span[data-e2e='top-right-avatar']").first
            menu_button.click(timeout=5000)
            print("  → Clicked profile menu")
            time.sleep(2)
        except:
            pass

        # Method 2: Try clicking "More" in sidebar (three dots icon)
        try:
            more_button = page.locator("div[data-e2e='more-menu'], button:has-text('More')").first
            more_button.click(timeout=5000)
            print("  → Clicked 'More' menu")
            time.sleep(2)
        except:
            pass

        # Method 3: JavaScript click on settings/menu button
        try:
            page.evaluate("""() => {
                // Find any button/div that looks like a menu
                const buttons = document.querySelectorAll('[data-e2e*="menu"], [aria-label*="Settings"], [aria-label*="Menu"], button');
                for (let btn of buttons) {
                    const text = btn.textContent || btn.getAttribute('aria-label') || '';
                    if (text.includes('Settings') || text.includes('Menu') || text.includes('More')) {
                        btn.click();
                        return true;
                    }
                }
            }""")
            time.sleep(2)
        except:
            pass

        # Now look for "Log out" button in the menu
        print("  → Looking for 'Log out' option...")

        # Try multiple logout button selectors
        logout_selectors = [
            "div[role='menuitem']:has-text('Log out')",
            "button:has-text('Log out')",
            "a:has-text('Log out')",
            "[data-e2e='logout-button']",
            "div:has-text('Log out')"
        ]

        logout_clicked = False
        for selector in logout_selectors:
            try:
                logout_button = page.locator(selector).first
                logout_button.click(timeout=3000)
                print("  ✓ Clicked 'Log out'")
                logout_clicked = True
                break
            except:
                continue

        # JavaScript fallback for logout
        if not logout_clicked:
            try:
                result = page.evaluate("""() => {
                    const elements = document.querySelectorAll('div, button, a, span');
                    for (let elem of elements) {
                        const text = (elem.textContent || elem.innerText || '').trim();
                        if (text === 'Log out' || text === 'Logout' || text === 'Sign out') {
                            elem.click();
                            return 'CLICKED: ' + text;
                        }
                    }
                    return 'NOT_FOUND';
                }""")

                if 'CLICKED' in result:
                    print(f"  ✓ {result}")
                    logout_clicked = True
            except:
                pass

        if logout_clicked:
            time.sleep(3)

            # Verify we're logged out (check if we're on login/signup page or home)
            current_url = page.url
            if 'login' in current_url.lower() or page.url == 'https://www.tiktok.com/':
                print("  ✓ Confirmed logged out")
                return True
            else:
                print(f"  ⚠ Still at: {current_url}")
                return True  # Consider it success anyway
        else:
            print("  ⚠ Could not find logout button")

            # Alternative: Navigate directly to logout URL
            try:
                print("  → Trying direct logout URL...")
                page.goto("https://www.tiktok.com/logout", timeout=10000)
                time.sleep(3)
                print("  ✓ Navigated to logout URL")
                return True
            except:
                pass

            # Alternative 2: Clear cookies by navigating to homepage
            try:
                print("  → Navigating to homepage...")
                page.goto("https://www.tiktok.com/", timeout=10000)
                time.sleep(2)
                return True
            except:
                pass

            return False

    except Exception as e:
        print(f"  ⚠ Logout error: {e}")
        return False

def create_account(page, account, account_num, total_accounts):
    email = account['email']
    password = account['password']

    print("\n" + "=" * 80)
    print(f"PROCESSING ACCOUNT {account_num}/{total_accounts}")
    print("=" * 80)
    print(f"Name: {account['firstName']} {account['lastName']}")
    print(f"Email: {email}")
    print(f"Password: {password}")
    print("=" * 80 + "\n")

    try:
        url = 'https://www.tiktok.com/signup/phone-or-email/email'
        print("Opening TikTok signup page...")
        page.goto(url, wait_until='domcontentloaded', timeout=60000)
        time.sleep(5)

        # Auto-set birthday: May 3, 2002
        print("\n[1/5] Setting birthday to May 3, 2002...")

        birthday_set = False

        # Wait for birthday dropdowns
        print("  → Waiting for birthday dropdowns to load...")
        try:
            page.wait_for_selector("div[role='combobox']", timeout=15000)
            print("  → Dropdowns detected")
            time.sleep(2)
        except PlaywrightTimeout:
            print("✗ Birthday dropdowns never appeared")
            save_to_csv(account, success=False, notes="Birthday dropdowns not found")
            return False

        # Try multiple times to set birthday
        for attempt in range(5):
            try:
                comboboxes = page.query_selector_all("div[role='combobox']")

                if len(comboboxes) >= 3:
                    print(f"  → Found {len(comboboxes)} custom dropdowns (attempt {attempt+1})")

                    month_combo = comboboxes[0]
                    day_combo = comboboxes[1]
                    year_combo = comboboxes[2]

                    # Scroll into view
                    month_combo.scroll_into_view_if_needed()
                    time.sleep(0.5)

                    # MONTH: Click and select May
                    print("  → Clicking Month dropdown...")
                    month_combo.click()
                    time.sleep(1.5)

                    month_options = page.query_selector_all("div[role='listbox'] div[role='option']")
                    if len(month_options) >= 5:
                        month_options[4].click()  # May is 5th option (index 4)
                        print("  ✓ Clicked May option")
                        time.sleep(1)

                        month_text = month_combo.inner_text().strip()
                        if month_text and month_text not in ['Month', 'Mes', '月']:
                            print(f"  ✓✓ Month confirmed: {month_text}")
                        else:
                            print(f"  ⚠ Month not confirmed")
                            continue
                    else:
                        print(f"  ⚠ Not enough month options")
                        continue

                    # DAY: Click and select 3
                    print("  → Clicking Day dropdown...")
                    day_combo.click()
                    time.sleep(1.5)

                    day_options = page.query_selector_all("div[role='listbox'] div[role='option']")
                    day_found = False
                    for opt in day_options:
                        if opt.inner_text().strip() == "3":
                            opt.click()
                            print("  ✓ Clicked Day 3 option")
                            time.sleep(1)
                            day_found = True
                            break

                    if not day_found:
                        print("  ⚠ Could not find day 3")
                        continue

                    # YEAR: Click and select 2002
                    print("  → Clicking Year dropdown...")
                    year_combo.click()
                    time.sleep(1)

                    year_options = page.query_selector_all("div[role='listbox'] div[role='option']")
                    year_found = False
                    for opt in year_options:
                        if opt.inner_text().strip() == "2002":
                            opt.click()
                            print("  ✓ Selected Year 2002")
                            year_found = True
                            break

                    if not year_found:
                        print("  ⚠ Could not find year 2002")
                        continue

                    time.sleep(0.8)
                    print("  ✓✓ Birthday set: May 3, 2002")
                    birthday_set = True
                    break

            except Exception as e:
                print(f"  ⚠ Attempt {attempt+1} failed: {e}")

            if not birthday_set and attempt < 4:
                print("  → Retrying...")
                time.sleep(1)

        if not birthday_set:
            print("\n✗ FAILED: Could not set birthday after 5 attempts")
            save_to_csv(account, success=False, notes="Failed to set birthday")
            return False

        # Wait for form to enable
        print("  → Waiting for form to enable...")
        time.sleep(3)

        # Email
        print("\n[2/5] Entering email address (human-like typing)...")
        email_selectors = [
            "input[name='email']",
            "input[type='text']",
            "input[placeholder*='email' i]"
        ]

        email_sent = False
        for selector in email_selectors:
            try:
                email_field = page.wait_for_selector(selector, timeout=5000)
                if email_field:
                    email_field.click()
                    email_field.fill('')  # Clear first
                    human_type(email_field, email)
                    email_sent = True
                    break
            except:
                continue

        if not email_sent:
            print("✗ Could not find email field")
            save_to_csv(account, success=False, notes="Could not find email field")
            return False

        time.sleep(1)

        # Password
        print("[3/5] Entering password (human-like typing)...")
        password_selectors = [
            "input[type='password']",
            "input[name='password']"
        ]

        password_sent = False
        for selector in password_selectors:
            try:
                password_field = page.wait_for_selector(selector, timeout=5000)
                if password_field:
                    password_field.click()
                    password_field.fill('')  # Clear first
                    human_type(password_field, password)
                    password_sent = True
                    break
            except:
                continue

        if not password_sent:
            print("✗ Could not find password field")
            save_to_csv(account, success=False, notes="Could not find password field")
            return False

        time.sleep(1)

        # Send code button
        print("[4/5] Clicking 'Send code' button...")

        button_clicked = False

        # Try JavaScript click first
        try:
            result = page.evaluate("""() => {
                var buttons = document.querySelectorAll('button');
                for (var i = 0; i < buttons.length; i++) {
                    var btn = buttons[i];
                    var text = btn.textContent || btn.innerText || '';
                    if (text.includes('Send code') || text.includes('Send')) {
                        btn.disabled = false;
                        btn.scrollIntoView({block: 'center'});
                        btn.click();
                        return 'CLICKED: ' + text.trim();
                    }
                }
                return 'NOT_FOUND';
            }""")

            if 'CLICKED' in result:
                print(f"  ✓✓ SUCCESS! {result}")
                button_clicked = True
                time.sleep(2)
        except Exception as e:
            print(f"  → JavaScript click failed: {e}")

        # Try Playwright selector click
        if not button_clicked:
            try:
                send_button = page.locator("button:has-text('Send code')").first
                send_button.click(timeout=5000)
                print("  ✓ Clicked Send code button")
                button_clicked = True
                time.sleep(2)
            except:
                pass

        if not button_clicked:
            print("✗ Could not find send code button")
            save_to_csv(account, success=False, notes="Could not find send code button")
            return False

        time.sleep(2)

        # Check for rate limiting
        try:
            page_text = page.locator("body").inner_text()
            if "maximum number" in page_text.lower() or "try again later" in page_text.lower():
                print("\n🚫 RATE LIMIT DETECTED!")
                print("  → TikTok says: 'Maximum number of attempts reached'")
                save_to_csv(account, success=False, notes="Rate limited - IP blocked")
                return "RATE_LIMITED"
        except:
            pass

        # Wait for verification code
        print("\n[!] VERIFICATION CODE REQUIRED")
        print("=" * 80)

        code = None

        if EMAIL_AUTO_FETCH:
            print(f"[EMAIL FETCHER] Auto-fetching code using: {EMAIL_FETCH_METHOD}")
            print(f"[EMAIL FETCHER] Email: {email}")
            print("=" * 80)

            print(f"  → Waiting {EMAIL_FETCH_DELAY} seconds for email to be sent...")
            time.sleep(EMAIL_FETCH_DELAY)

            code = get_verification_code(email, password, max_wait=90)

        if not code:
            if EMAIL_AUTO_FETCH:
                print("\n⚠ Auto-fetch failed")
                print("=" * 80)
                code = input("Enter 6-digit code (or 'skip'): ").strip()

                if code.lower() == 'skip' or not code:
                    print("Skipping account...")
                    save_to_csv(account, success=False, notes="Manual code entry skipped")
                    return False

                if not re.match(r'^\d{6}$', code):
                    print("✗ Invalid code format")
                    save_to_csv(account, success=False, notes="Invalid code entered")
                    return False
            else:
                print("\n✗ Email auto-fetch not available")
                save_to_csv(account, success=False, notes="Email auto-fetch not available")
                return False
        else:
            print(f"\n✓ Code auto-fetched: {code}")
            human_delay = random.uniform(8, 12)
            print(f"Simulating human checking email... waiting {human_delay:.1f} seconds")
            time.sleep(human_delay)

        # Enter verification code
        print("\n[5/5] Entering verification code (character-by-character)...")
        code_selectors = [
            "input[placeholder*='digit' i]",
            "input[placeholder*='code' i]",
            "input[name='code']"
        ]

        code_sent = False
        for selector in code_selectors:
            try:
                code_field = page.wait_for_selector(selector, timeout=10000)
                if code_field:
                    code_field.click()
                    human_type(code_field, code)
                    code_sent = True
                    break
            except:
                continue

        if not code_sent:
            print("✗ Could not find code field")
            save_to_csv(account, success=False, notes="Could not find verification code field")
            return False

        # Human review delay
        review_delay = random.uniform(2, 4)
        print(f"  → Pausing {review_delay:.1f}s (simulating human reviewing code)...")
        time.sleep(review_delay)

        # Click Next button
        print("\n[6/7] Clicking 'Next' button...")

        next_clicked = False
        try:
            result = page.evaluate("""() => {
                var buttons = document.querySelectorAll('button');
                for (var i = 0; i < buttons.length; i++) {
                    var btn = buttons[i];
                    var text = btn.textContent || btn.innerText || '';
                    if (text.trim() === 'Next' || text.includes('Next')) {
                        btn.scrollIntoView({block: 'center'});
                        btn.click();
                        return 'CLICKED: ' + text.trim();
                    }
                }
                return 'NOT_FOUND';
            }""")

            if 'CLICKED' in result:
                print(f"  ✓ {result}")
                next_clicked = True
                time.sleep(3)
        except:
            pass

        if not next_clicked:
            try:
                next_button = page.locator("button:has-text('Next')").first
                next_button.click(timeout=5000)
                print("  ✓ Clicked Next button")
                time.sleep(3)
            except:
                print("  ⚠ Could not find Next button - may auto-submit")
                time.sleep(5)

        # Check for success
        print("\n[7/7] Checking if account was created...")
        time.sleep(5)

        current_url = page.url
        print(f"  → Current URL: {current_url}")

        # Check if redirected to username creation page
        if 'create-username' in current_url.lower():
            print("  ✓ Redirected to username creation page!")
            print("\n[8/9] Creating username...")

            # Generate username from email (first part before @)
            username_base = account['email'].split('@')[0]
            # Add random numbers to make it unique
            username = f"{username_base}{random.randint(100, 999)}"
            print(f"  → Generated username: {username}")

            # Enter username
            try:
                username_field = page.wait_for_selector("input[placeholder*='Username' i], input[name='username']", timeout=10000)
                if username_field:
                    username_field.click()
                    username_field.fill('')
                    human_type(username_field, username)
                    print(f"  ✓ Entered username: {username}")
                    time.sleep(1)
            except Exception as e:
                print(f"  ⚠ Could not enter username: {e}")

            # Click "Sign up" button or "Skip"
            print("\n[9/9] Clicking 'Sign up' or 'Skip' button...")

            # Try to click "Skip" button first (easier, no username validation)
            skip_clicked = False
            try:
                skip_button = page.locator("button:has-text('Skip'), a:has-text('Skip')").first
                skip_button.click(timeout=5000)
                print("  ✓ Clicked 'Skip' button")
                skip_clicked = True
                time.sleep(3)
            except:
                pass

            # If skip didn't work, try "Sign up" button
            if not skip_clicked:
                try:
                    signup_button = page.locator("button:has-text('Sign up')").first
                    signup_button.click(timeout=5000)
                    print("  ✓ Clicked 'Sign up' button")
                    time.sleep(3)
                except Exception as e:
                    print(f"  ⚠ Could not click button: {e}")

            # Wait a moment for redirect
            time.sleep(5)
            final_url = page.url
            print(f"  → Final URL: {final_url}")

            # Check if we're now on the main TikTok page
            if 'signup' not in final_url.lower() and 'create-username' not in final_url.lower():
                print(f"✓✓ SUCCESS! Account fully created and logged in!")
                print(f"  → Redirected to: {final_url}")

                # LOG OUT before finishing
                print("\n[10/10] Logging out for next account...")
                logout_success = logout_tiktok(page)

                if logout_success:
                    print("  ✓ Logged out successfully")
                    save_to_csv(account, success=True, notes=f"Completed - Username: {username if not skip_clicked else 'skipped'} - Logged out")
                else:
                    print("  ⚠ Logout may have failed, but account created")
                    save_to_csv(account, success=True, notes=f"Completed - Username: {username if not skip_clicked else 'skipped'} - Check logout")

                mark_email_processed(email)
                return True
            else:
                print(f"  ⚠ Still on signup flow at: {final_url}")
                save_to_csv(account, success=True, notes="Partial success - verify manually")
                mark_email_processed(email)
                return True

        elif 'signup' not in current_url.lower():
            print(f"  ✓ URL changed - no longer on signup page")

            if 'tiktok.com' in current_url.lower():
                print(f"✓✓ SUCCESS! Account created and logged in!")
                print(f"  → Redirected to: {current_url}")

                # LOG OUT before finishing
                print("\n[8/8] Logging out for next account...")
                logout_success = logout_tiktok(page)

                if logout_success:
                    print("  ✓ Logged out successfully")
                    save_to_csv(account, success=True, notes="Completed automatically - Logged out")
                else:
                    print("  ⚠ Logout may have failed, but account created")
                    save_to_csv(account, success=True, notes="Completed automatically - Check logout")

                mark_email_processed(email)
                return True

        # Check for errors
        try:
            page_text = page.locator("body").inner_text().lower()
            error_phrases = ['invalid code', 'incorrect code', 'wrong code', 'expired']

            for error in error_phrases:
                if error in page_text:
                    print(f"✗ FAILED: Detected error: '{error}'")
                    save_to_csv(account, success=False, notes=f"Error: {error}")
                    return False
        except:
            pass

        # Final check
        time.sleep(10)
        final_url = page.url

        if 'signup' not in final_url.lower() and 'tiktok.com' in final_url.lower():
            print(f"✓✓ SUCCESS! Account created!")
            save_to_csv(account, success=True, notes="Completed - Playwright CDP")
            mark_email_processed(email)
            return True
        else:
            print(f"✗ UNCERTAIN: Marking as success (verify manually)")
            save_to_csv(account, success=True, notes="Uncertain - verify manually")
            mark_email_processed(email)
            return True

    except Exception as e:
        print(f"\n✗ Error: {str(e)}")
        save_to_csv(account, success=False, notes=f"Error: {str(e)}")
        return False

def main():
    clear_screen()

    fetch_status = f"✓ AUTO-FETCHES codes ({EMAIL_FETCH_METHOD})" if EMAIL_AUTO_FETCH else "⚠ Manual code entry"

    print(f"""
================================================================
     TikTok Account Creator v7.0 - PLAYWRIGHT CDP
        ✓ Connects to YOUR Chrome browser
        ✓ Uses YOUR ProtonVPN connection
        ✓ Human-like character typing (100-400ms delays)
        {fetch_status}
        ✓ No bot detection - uses real browser fingerprint
================================================================
""")

    # Load accounts
    print("Loading accounts from accounts.xlsx...")
    accounts = load_accounts()
    processed_emails = get_processed_emails()
    available_accounts = [acc for acc in accounts if acc['email'] not in processed_emails]

    print(f"✓ Loaded {len(accounts)} accounts")
    print(f"Already processed: {len(processed_emails)}")
    print(f"Remaining: {len(available_accounts)}")

    if not available_accounts:
        print("\n✓ All accounts processed!")
        return

    # Ask batch size
    max_allowed = min(len(available_accounts), MAX_BATCH_SIZE)

    if len(sys.argv) > 1:
        try:
            batch_size = int(sys.argv[1])
            batch_size = min(batch_size, max_allowed)
            print(f"\nBatch size from command line: {batch_size}")
        except:
            batch_size = 1
            print(f"\nInvalid argument, using default: {batch_size}")
    else:
        # Default to 1 if no argument provided
        batch_size = 1
        print(f"\nNo batch size specified, using default: {batch_size}")
        print(f"(To specify batch size, run: python core/run_playwright_chrome.py <number>)")

    accounts_to_process = available_accounts[:batch_size]

    print(f"\n→ Processing {batch_size} account(s)...")
    print("\n" + "=" * 80)
    print("CONNECTING TO YOUR CHROME BROWSER")
    print("=" * 80)
    print("Checking if Chrome is running on port 9222...")
    print("=" * 80)

    successful = 0
    failed = 0

    try:
        with sync_playwright() as playwright:
            print("\nConnecting to Chrome via CDP on port 9222...")

            try:
                browser = playwright.chromium.connect_over_cdp("http://localhost:9222")
                print("✓ Connected to your Chrome browser!")

                # Get default context and page
                if len(browser.contexts) > 0:
                    context = browser.contexts[0]

                    # Create new page or use existing
                    if len(context.pages) > 0:
                        page = context.pages[0]
                    else:
                        page = context.new_page()

                    print("✓ Using your browser with ProtonVPN active!")
                    print("=" * 80 + "\n")

                    # Process accounts
                    for idx, account in enumerate(accounts_to_process, 1):
                        result = create_account(page, account, idx, batch_size)

                        if result == "RATE_LIMITED":
                            print("\n⚠ Rate limited - switch VPN location and restart")
                            failed += 1
                        elif result:
                            successful += 1
                        else:
                            failed += 1

                        # Progress update
                        remaining = batch_size - idx
                        progress_pct = (idx / batch_size) * 100
                        print(f"\n📊 Progress: {idx}/{batch_size} ({progress_pct:.1f}%) | ✓ {successful} | ✗ {failed}")

                        if idx < batch_size:
                            print(f"⏳ Waiting {ACCOUNT_DELAY}s before next account...")
                            time.sleep(ACCOUNT_DELAY)
                else:
                    print("❌ No browser contexts found!")
                    print("   Make sure Chrome is running on port 9222")
                    sys.exit(1)

            except Exception as e:
                print(f"\n❌ Could not connect to Chrome on port 9222!")
                print(f"   Error: {str(e)}")
                print("\n" + "=" * 80)
                print("TROUBLESHOOTING:")
                print("=" * 80)
                print("1. Run START_CHROME_DEBUG.bat first")
                print("2. Keep that Chrome window open")
                print("3. Verify Chrome opened (check taskbar)")
                print("4. Check http://localhost:9222/json in another browser")
                print("5. Run this script again")
                print("=" * 80)
                sys.exit(1)

    except KeyboardInterrupt:
        print("\n\n⚠ Interrupted by user")

    finally:
        print("\n" + "=" * 80)
        print("BATCH COMPLETE")
        print("=" * 80)
        print(f"Successful: {successful}")
        print(f"Failed: {failed}")
        print(f"Remaining: {len(available_accounts) - batch_size}")
        print("=" * 80)
        print("\nKeep Chrome window open for next batch!")

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\nScript interrupted")
        sys.exit(0)
    except Exception as e:
        print(f"\n\nUnexpected error: {e}")
        sys.exit(1)
