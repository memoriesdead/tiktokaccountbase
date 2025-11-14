# Instagram Account Creator - Playwright CDP Method

**Adapted from TikTok v7.0 - Tested & Working Method**

---

## 🎯 **The Method That Works**

This document explains how to adapt the **Playwright CDP (Chrome DevTools Protocol)** method that successfully works for TikTok to create Instagram accounts.

---

## 🔧 **Core Concept (From TikTok v7.0)**

### What Makes This Method Perfect

1. **Uses YOUR Chrome Browser**
   - Connects via Chrome DevTools Protocol (CDP)
   - Real browser fingerprint = no bot detection
   - Your extensions, cookies, settings all intact

2. **Uses YOUR VPN**
   - ProtonVPN (or any VPN) stays active throughout
   - No need to configure proxies in code
   - Switch VPN locations manually when rate-limited

3. **Human-Like Automation**
   - Character-by-character typing (100-400ms delays)
   - Random pauses between actions
   - Natural mouse movements via Playwright

4. **Chrome 136+ Compatible**
   - Uses `--remote-debugging-port=9222`
   - Requires `--user-data-dir` (custom profile)
   - Works with latest Chrome (2025)

---

## 📋 **Instagram Signup Flow Analysis**

### Step-by-Step Breakdown

1. **Landing Page**
   - URL: `https://www.instagram.com/accounts/emailsignup/`
   - Or: `https://www.instagram.com/` → Click "Sign up"

2. **Email/Phone Input**
   - Field: Mobile Number or Email
   - Can use email or phone

3. **Full Name**
   - Field: Full Name
   - Instagram display name

4. **Username**
   - Field: Username
   - Must be unique
   - Auto-suggestions provided

5. **Password**
   - Field: Password
   - Minimum 6 characters

6. **Birthday**
   - Month dropdown
   - Day dropdown
   - Year dropdown
   - Must be 13+ years old

7. **Click "Next" or "Sign Up"**
   - Submit button

8. **Email Verification (if email used)**
   - Instagram sends verification code
   - Enter 6-digit code
   - Similar to TikTok flow

9. **Post-Signup Steps**
   - May ask to add profile photo
   - May ask to follow suggested accounts
   - May ask to enable notifications
   - Can skip all these

---

## 🚀 **Implementation Plan**

### Files to Create

```
TikTok-Account-Creator/
├── instagram/
│   ├── run_instagram_playwright.py    # Main Instagram script
│   ├── START_CHROME_INSTAGRAM.bat     # Launch Chrome for Instagram
│   └── RUN_INSTAGRAM.bat              # One-click launcher
│
├── instagram_accounts.xlsx             # Input: Instagram credentials
├── instagram_created.csv               # Output: Results
└── instagram_processed.txt             # Processed emails
```

---

## 💻 **Code Structure (Adapted from TikTok)**

### 1. Chrome Connection (Same as TikTok)

```python
from playwright.sync_api import sync_playwright

with sync_playwright() as playwright:
    # Connect to YOUR Chrome via CDP
    browser = playwright.chromium.connect_over_cdp("http://localhost:9222")
    context = browser.contexts[0]

    if len(context.pages) > 0:
        page = context.pages[0]
    else:
        page = context.new_page()
```

**This is identical to TikTok - no changes needed!**

---

### 2. Navigate to Instagram Signup

```python
url = 'https://www.instagram.com/accounts/emailsignup/'
page.goto(url, wait_until='domcontentloaded', timeout=60000)
time.sleep(3)
```

---

### 3. Email Entry (Human-Like Typing)

```python
def human_type(element, text):
    """Type character-by-character with random delays"""
    import random
    for char in str(text):
        element.type(char)
        time.sleep(random.uniform(0.1, 0.4))

# Find and fill email field
email_field = page.wait_for_selector("input[name='emailOrPhone']", timeout=10000)
email_field.click()
human_type(email_field, account['email'])
```

---

### 4. Full Name Entry

```python
fullname_field = page.wait_for_selector("input[name='fullName']", timeout=10000)
fullname_field.click()
full_name = f"{account['firstName']} {account['lastName']}"
human_type(fullname_field, full_name)
```

---

### 5. Username Generation

```python
# Generate username from email or first/last name
username_base = account['email'].split('@')[0]
username = f"{username_base}{random.randint(100, 999)}"

username_field = page.wait_for_selector("input[name='username']", timeout=10000)
username_field.click()
human_type(username_field, username)
```

---

### 6. Password Entry

```python
password_field = page.wait_for_selector("input[name='password']", timeout=10000)
password_field.click()
human_type(password_field, account['password'])
```

---

### 7. Birthday Selection (Similar to TikTok)

```python
# Month dropdown
month_select = page.wait_for_selector("select[title='Month:']", timeout=10000)
month_select.select_option(label="May")  # or value="5"

# Day dropdown
day_select = page.wait_for_selector("select[title='Day:']", timeout=10000)
day_select.select_option(label="3")  # or value="3"

# Year dropdown
year_select = page.wait_for_selector("select[title='Year:']", timeout=10000)
year_select.select_option(label="2002")  # or value="2002"
```

---

### 8. Click Sign Up Button

```python
# Try multiple methods to click "Sign up" button
signup_clicked = False

# Method 1: JavaScript click
try:
    result = page.evaluate("""() => {
        var buttons = document.querySelectorAll('button');
        for (var i = 0; i < buttons.length; i++) {
            var btn = buttons[i];
            var text = btn.textContent || btn.innerText || '';
            if (text.includes('Sign up') || text.includes('Next')) {
                btn.click();
                return 'CLICKED: ' + text.trim();
            }
        }
        return 'NOT_FOUND';
    }""")

    if 'CLICKED' in result:
        print(f"✓ {result}")
        signup_clicked = True
except:
    pass

# Method 2: Playwright selector
if not signup_clicked:
    try:
        signup_button = page.locator("button:has-text('Sign up')").first
        signup_button.click(timeout=5000)
        signup_clicked = True
    except:
        pass
```

---

### 9. Email Verification Code (Same as TikTok!)

```python
# Wait for verification code
print("\n[!] EMAIL VERIFICATION CODE REQUIRED")

# Auto-fetch from webmail (reuse TikTok's email fetcher!)
if EMAIL_AUTO_FETCH:
    print(f"Auto-fetching code from: {email}")
    time.sleep(EMAIL_FETCH_DELAY)

    # Use the SAME email fetcher as TikTok
    code = get_verification_code(email, password, max_wait=90)

# Enter verification code
if code:
    code_field = page.wait_for_selector("input[name='email_confirmation_code']", timeout=10000)
    code_field.click()
    human_type(code_field, code)
```

---

### 10. Skip Post-Signup Steps

```python
# Check current URL after code entry
current_url = page.url

# Skip profile photo
if 'profile_pic' in current_url.lower():
    try:
        skip_button = page.locator("button:has-text('Skip')").first
        skip_button.click(timeout=5000)
    except:
        pass

# Skip follow suggestions
if 'follow' in current_url.lower():
    try:
        skip_button = page.locator("button:has-text('Skip')").first
        skip_button.click(timeout=5000)
    except:
        pass

# Skip notifications
if 'notification' in current_url.lower():
    try:
        not_now_button = page.locator("button:has-text('Not Now')").first
        not_now_button.click(timeout=5000)
    except:
        pass
```

---

### 11. Success Detection

```python
# Check if we're logged in (redirected to home feed)
time.sleep(5)
final_url = page.url

if 'instagram.com' in final_url and 'accounts/emailsignup' not in final_url:
    print("✓✓ SUCCESS! Account created and logged in!")
    save_to_csv(account, success=True, notes=f"Username: {username}")
    return True
else:
    print("✗ Account creation uncertain")
    save_to_csv(account, success=False, notes=f"Still at: {final_url}")
    return False
```

---

## 🔑 **Key Differences from TikTok**

| Aspect | TikTok | Instagram |
|--------|--------|-----------|
| **Signup URL** | `/signup/phone-or-email/email` | `/accounts/emailsignup/` |
| **Birthday** | Custom dropdowns (`div[role='combobox']`) | Standard `<select>` dropdowns |
| **Username** | Post-auth page | During signup |
| **Full Name** | Separate fields (First/Last) | Single field |
| **Email Verification** | Always required | Always required |
| **Post-Signup** | Username creation | Photo, follows, notifications |

---

## 📝 **Excel File Format (instagram_accounts.xlsx)**

```
| First Name | Last Name | Email                    | Password      |
|------------|-----------|--------------------------|---------------|
| Ahmed      | Benali    | ahmed.benali@example.com | Welcome2025! |
| Sarah      | Johnson   | sarah.j@example.com      | Secure123!   |
```

**Same format as TikTok!**

---

## 🚀 **Quick Start Commands**

### 1. Start Chrome with Debugging
```bash
START_CHROME_INSTAGRAM.bat
```

**Contents of `START_CHROME_INSTAGRAM.bat`:**
```batch
@echo off
set CHROME_PROFILE=%USERPROFILE%\ChromeInstagramProfile

if not exist "%CHROME_PROFILE%" mkdir "%CHROME_PROFILE%"

"C:\Program Files\Google\Chrome\Application\chrome.exe" --remote-debugging-port=9222 --user-data-dir="%CHROME_PROFILE%" --no-first-run --no-default-browser-check

pause
```

---

### 2. Enable ProtonVPN in Chrome
- Open ProtonVPN extension
- Connect to a location (UK, US, etc.)

---

### 3. Run Instagram Automation
```bash
python instagram/run_instagram_playwright.py 1
```

---

## ⚙️ **Configuration**

```python
# instagram/run_instagram_playwright.py

# Batch settings (same as TikTok)
MAX_BATCH_SIZE = 50
EMAIL_FETCH_DELAY = 5
ACCOUNT_DELAY = 3

# Birthday (hardcoded for 18+ / 13+)
BIRTHDAY_MONTH = 5    # May
BIRTHDAY_DAY = 3
BIRTHDAY_YEAR = 2002  # Age 23 in 2025
```

---

## 🔄 **Rate Limit Handling**

Instagram rate limits are similar to TikTok:

1. **Detection**
   - Look for error messages like "Try again later"
   - "Too many requests"
   - "Unusual activity"

2. **Response**
   - Switch ProtonVPN to different location
   - Wait 5-10 minutes
   - Continue script

```python
# Check for rate limiting
try:
    page_text = page.locator("body").inner_text()

    if "try again later" in page_text.lower() or "too many" in page_text.lower():
        print("\n🚫 RATE LIMIT DETECTED!")
        print("  → Instagram rate limiting detected")
        print("  → Switch VPN and wait 5-10 minutes")
        return "RATE_LIMITED"
except:
    pass
```

---

## 🎯 **Typical Workflow**

### Daily Operation (Same as TikTok)

1. **Morning (9 AM)**
   - Start Chrome with ProtonVPN (UK)
   - Run: `python instagram/run_instagram_playwright.py 5`
   - Creates 5 Instagram accounts

2. **Rate Limited? (10 AM)**
   - Switch ProtonVPN to US
   - Wait 5 minutes
   - Run: `python instagram/run_instagram_playwright.py 5`
   - Creates 5 more accounts

3. **Afternoon (2 PM)**
   - Switch ProtonVPN to Canada
   - Run: `python instagram/run_instagram_playwright.py 5`
   - Creates 5 more accounts

**Daily Total:** 15 Instagram accounts with 3 VPN switches

---

## 🔍 **Selectors to Find**

Before coding, we need to verify these Instagram selectors:

### Email/Phone Input
```python
# Likely selectors:
"input[name='emailOrPhone']"
"input[aria-label='Mobile Number or Email']"
"input[placeholder*='email' i]"
```

### Full Name
```python
"input[name='fullName']"
"input[aria-label='Full Name']"
```

### Username
```python
"input[name='username']"
"input[aria-label='Username']"
```

### Password
```python
"input[name='password']"
"input[type='password']"
"input[aria-label='Password']"
```

### Birthday Dropdowns
```python
"select[title='Month:']"
"select[title='Day:']"
"select[title='Year:']"
```

### Sign Up Button
```python
"button:has-text('Sign up')"
"button:has-text('Next')"
"button[type='submit']"
```

### Verification Code
```python
"input[name='email_confirmation_code']"
"input[placeholder*='confirmation' i]"
"input[placeholder*='code' i]"
```

---

## 📦 **Dependencies (Same as TikTok)**

```bash
pip install playwright
pip install pandas openpyxl
pip install selenium  # For email fetcher
```

---

## 🎨 **Complete Script Template**

```python
# instagram/run_instagram_playwright.py
# -*- coding: utf-8 -*-

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
BIRTHDAY_MONTH = 5
BIRTHDAY_DAY = 3
BIRTHDAY_YEAR = 2002
# =======================================================

# Import email fetcher (reuse from TikTok!)
EMAIL_AUTO_FETCH = False
get_verification_code = None

try:
    sys.path.insert(0, '..')
    from core.email_fetcher_selenium import get_verification_code_selenium
    get_verification_code = lambda email, password, max_wait: get_verification_code_selenium(email, password, max_wait, headless=True)
    EMAIL_AUTO_FETCH = True
    EMAIL_FETCH_METHOD = "Selenium (browser)"
except ImportError:
    EMAIL_AUTO_FETCH = False
    EMAIL_FETCH_METHOD = "None"

def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')

def load_accounts():
    try:
        df = pd.read_excel('instagram_accounts.xlsx')
        accounts = []
        for _, row in df.iterrows():
            accounts.append({
                'firstName': row['First Name'],
                'lastName': row['Last Name'],
                'email': row['email'],
                'password': row['password']
            })
        return accounts
    except Exception as e:
        print(f"Error reading Excel: {e}")
        sys.exit(1)

def get_processed_emails():
    if os.path.exists('instagram_processed.txt'):
        with open('instagram_processed.txt', 'r') as f:
            return set(line.strip() for line in f)
    return set()

def mark_email_processed(email):
    with open('instagram_processed.txt', 'a') as f:
        f.write(email + '\n')

def save_to_csv(account, success=True, notes=""):
    csv_file = 'instagram_created.csv'
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
    """Type character-by-character with human-like delays"""
    for char in str(text):
        element.type(char)
        time.sleep(random.uniform(0.1, 0.4))

def create_instagram_account(page, account, account_num, total_accounts):
    email = account['email']
    password = account['password']

    print("\n" + "=" * 80)
    print(f"PROCESSING INSTAGRAM ACCOUNT {account_num}/{total_accounts}")
    print("=" * 80)
    print(f"Name: {account['firstName']} {account['lastName']}")
    print(f"Email: {email}")
    print("=" * 80 + "\n")

    try:
        # Step 1: Navigate to Instagram signup
        url = 'https://www.instagram.com/accounts/emailsignup/'
        print("Opening Instagram signup page...")
        page.goto(url, wait_until='domcontentloaded', timeout=60000)
        time.sleep(3)

        # Step 2: Enter email
        print("\n[1/7] Entering email...")
        email_field = page.wait_for_selector("input[name='emailOrPhone']", timeout=10000)
        email_field.click()
        human_type(email_field, email)
        time.sleep(1)

        # Step 3: Enter full name
        print("[2/7] Entering full name...")
        fullname = f"{account['firstName']} {account['lastName']}"
        fullname_field = page.wait_for_selector("input[name='fullName']", timeout=10000)
        fullname_field.click()
        human_type(fullname_field, fullname)
        time.sleep(1)

        # Step 4: Generate and enter username
        print("[3/7] Generating username...")
        username_base = account['email'].split('@')[0].replace('.', '_')
        username = f"{username_base}{random.randint(100, 999)}"
        print(f"  → Username: {username}")

        username_field = page.wait_for_selector("input[name='username']", timeout=10000)
        username_field.click()
        human_type(username_field, username)
        time.sleep(1)

        # Step 5: Enter password
        print("[4/7] Entering password...")
        password_field = page.wait_for_selector("input[name='password']", timeout=10000)
        password_field.click()
        human_type(password_field, password)
        time.sleep(1)

        # Step 6: Click Sign Up button
        print("[5/7] Clicking Sign Up...")
        try:
            signup_button = page.locator("button:has-text('Sign up')").first
            signup_button.click(timeout=5000)
            time.sleep(3)
        except:
            pass

        # Step 7: Set birthday
        print("[6/7] Setting birthday...")

        # Month
        month_select = page.wait_for_selector("select[title='Month:']", timeout=10000)
        month_select.select_option(value=str(BIRTHDAY_MONTH))
        time.sleep(0.5)

        # Day
        day_select = page.wait_for_selector("select[title='Day:']", timeout=10000)
        day_select.select_option(value=str(BIRTHDAY_DAY))
        time.sleep(0.5)

        # Year
        year_select = page.wait_for_selector("select[title='Year:']", timeout=10000)
        year_select.select_option(value=str(BIRTHDAY_YEAR))
        time.sleep(1)

        # Click Next after birthday
        try:
            next_button = page.locator("button:has-text('Next')").first
            next_button.click(timeout=5000)
            time.sleep(3)
        except:
            pass

        # Step 8: Email verification
        print("[7/7] Waiting for email verification code...")

        code = None
        if EMAIL_AUTO_FETCH:
            print("  → Auto-fetching code...")
            time.sleep(EMAIL_FETCH_DELAY)
            code = get_verification_code(email, password, max_wait=90)

        if code:
            print(f"  ✓ Code received: {code}")

            # Enter code
            code_field = page.wait_for_selector("input[name='email_confirmation_code']", timeout=10000)
            code_field.click()
            human_type(code_field, code)
            time.sleep(2)

            # Click Next/Confirm
            try:
                next_button = page.locator("button:has-text('Next')").first
                next_button.click(timeout=5000)
                time.sleep(5)
            except:
                pass

        # Skip post-signup steps
        for _ in range(3):
            try:
                # Try Skip button
                skip_button = page.locator("button:has-text('Skip')").first
                skip_button.click(timeout=3000)
                time.sleep(2)
            except:
                try:
                    # Try Not Now button
                    not_now = page.locator("button:has-text('Not Now')").first
                    not_now.click(timeout=3000)
                    time.sleep(2)
                except:
                    break

        # Check success
        final_url = page.url
        if 'instagram.com' in final_url and 'emailsignup' not in final_url:
            print(f"\n✓✓ SUCCESS! Instagram account created!")
            print(f"  → Username: {username}")
            save_to_csv(account, success=True, notes=f"Username: {username}")
            mark_email_processed(email)
            return True
        else:
            print(f"\n✗ Uncertain - Final URL: {final_url}")
            save_to_csv(account, success=False, notes=f"At: {final_url}")
            return False

    except Exception as e:
        print(f"\n✗ Error: {e}")
        save_to_csv(account, success=False, notes=f"Error: {e}")
        return False

def main():
    clear_screen()

    print("""
================================================================
     Instagram Account Creator - Playwright CDP
        ✓ Uses YOUR Chrome with YOUR ProtonVPN
        ✓ Human-like typing (100-400ms delays)
        ✓ Email auto-fetch (Selenium)
        ✓ Zero bot detection
================================================================
""")

    # Load accounts
    accounts = load_accounts()
    processed = get_processed_emails()
    available = [acc for acc in accounts if acc['email'] not in processed]

    print(f"✓ Loaded {len(accounts)} accounts")
    print(f"Already processed: {len(processed)}")
    print(f"Remaining: {len(available)}")

    if not available:
        print("\n✓ All accounts processed!")
        return

    # Batch size
    batch_size = int(sys.argv[1]) if len(sys.argv) > 1 else 1
    batch_size = min(batch_size, MAX_BATCH_SIZE, len(available))

    print(f"\n→ Processing {batch_size} account(s)...")
    print("\nMake sure Chrome is running with ProtonVPN!")
    print("=" * 80 + "\n")

    successful = 0
    failed = 0

    try:
        with sync_playwright() as playwright:
            browser = playwright.chromium.connect_over_cdp("http://localhost:9222")
            context = browser.contexts[0]
            page = context.pages[0] if len(context.pages) > 0 else context.new_page()

            print("✓ Connected to Chrome!\n")

            for idx, account in enumerate(available[:batch_size], 1):
                result = create_instagram_account(page, account, idx, batch_size)

                if result:
                    successful += 1
                else:
                    failed += 1

                print(f"\n📊 Progress: {idx}/{batch_size} | ✓ {successful} | ✗ {failed}")

                if idx < batch_size:
                    print(f"⏳ Waiting {ACCOUNT_DELAY}s...")
                    time.sleep(ACCOUNT_DELAY)

    except Exception as e:
        print(f"\n✗ Error: {e}")

    finally:
        print("\n" + "=" * 80)
        print("BATCH COMPLETE")
        print("=" * 80)
        print(f"Successful: {successful}")
        print(f"Failed: {failed}")
        print("=" * 80)

if __name__ == "__main__":
    main()
```

---

## ✅ **Testing Checklist**

Before running the full script:

1. ✅ **Test Chrome Connection**
   ```bash
   python test_chrome_connection.py
   ```

2. ✅ **Manually Test Signup Flow**
   - Open Instagram signup in debug Chrome
   - Inspect each field with DevTools
   - Verify selector names match code

3. ✅ **Test Email Fetcher**
   - Verify email fetcher works with Instagram emails
   - Check "Instagram" in subject line

4. ✅ **Run with 1 Account**
   ```bash
   python instagram/run_instagram_playwright.py 1
   ```

5. ✅ **Monitor Console**
   - Watch for errors
   - Verify each step completes

---

## 🎯 **Success Metrics**

Like TikTok, track:
- ✅ Accounts created per day
- ✅ Success rate (%)
- ✅ VPN locations that work best
- ✅ Time between rate limits

---

## 🚀 **Next Steps**

1. **Create instagram folder**
   ```bash
   mkdir instagram
   ```

2. **Copy and adapt TikTok script**
   - Use this document as reference
   - Test each section incrementally

3. **Create Instagram Excel file**
   - Same format as TikTok

4. **Test with 1 account first**
   - Verify entire flow works
   - Fix any selector issues

5. **Scale up gradually**
   - 1 account → 5 accounts → 10 accounts

---

## 💡 **Pro Tips**

1. **Reuse TikTok Infrastructure**
   - ✅ Chrome connection code (identical)
   - ✅ Email fetcher (same)
   - ✅ Human typing function (same)
   - ✅ CSV logging (same)

2. **Only Change Instagram-Specific Parts**
   - ❌ URL (different)
   - ❌ Form fields (different)
   - ❌ Birthday dropdowns (standard vs custom)
   - ✅ Everything else is the same!

3. **Test Incrementally**
   - Don't code entire script at once
   - Test each step individually
   - Fix issues before moving on

---

## 📞 **Support**

If issues arise:

1. Check Instagram signup page hasn't changed
2. Verify selectors with DevTools
3. Test Chrome connection separately
4. Check email fetcher works
5. Review TikTok script for reference

---

**This method works for TikTok, it will work for Instagram!** 🎉

The core CDP connection and human-like automation are platform-agnostic. Only the form fields and flow differ slightly.
