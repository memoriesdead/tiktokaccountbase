# TikTok Account Creator - Fully Automated

**Version 7.0** - Playwright CDP with YOUR Chrome Browser

**WORKING SOLUTION:** Connects to YOUR Chrome via CDP - Tested & Verified Nov 2025!

Original concept by [Hendrik Bgr](https://github.com/hendrikbgr) - Enhanced with full automation by memoriesdead

---

## 🚀 LATEST: Playwright CDP Solution (v7.0) ✅ WORKING

**The closest to full automation - Uses YOUR Chrome with YOUR ProtonVPN!**

### How It Works (Simple Workflow)

1. **Start Chrome** with debugging enabled (one command)
2. **Enable ProtonVPN** in that Chrome window
3. **Run the script** - It creates accounts automatically
4. **When rate-limited** - Switch VPN location, script continues
5. **Repeat** - Rinse and repeat for unlimited accounts

### Why This Method Works

- ✅ **Uses YOUR Chrome** - Real browser fingerprint, no bot detection
- ✅ **ProtonVPN Integration** - Your VPN stays active during automation
- ✅ **Playwright CDP** - Industry standard (Netflix, Microsoft, Google use it)
- ✅ **Human-Like Typing** - 100-400ms delays per character
- ✅ **Chrome 136+ Compatible** - Works with latest Chrome (2025)
- ✅ **Rate Limit Handling** - Detects limits, pause & switch VPN
- ✅ **Username Auto-Creation** - Handles post-auth username page
- ✅ **Email Auto-Fetch** - Selenium-based verification code retrieval

### Quick Start (3 Steps)

```bash
# Step 1: Start Chrome with debugging
START_CHROME_DEBUG.bat

# Step 2: Enable ProtonVPN in that Chrome

# Step 3: Run automation
python core/run_playwright_chrome.py 1
```

**OR use the one-click launcher:**
```bash
RUN_WITH_YOUR_CHROME.bat
```

---

## 🌐 Oracle Cloud IP Rotation (v6.1)

**Bypass TikTok rate limits with unlimited datacenter IPs - completely FREE!**

- **Unlimited IPs** - Oracle Cloud Free Tier provides fresh IPs via VM rotation
- **$0 Cost Forever** - Oracle Free Tier never expires
- **No Rate Limits** - Each batch uses a new Oracle VM with fresh IP
- **Automated** - One-click startup after 30-minute setup
- **Scalable** - Create 10 or 10,000 accounts

**Quick Start:**
```bash
START_ORACLE_FARM.bat
```

**Full Guide:** [ORACLE_INTEGRATION_COMPLETE.md](ORACLE_INTEGRATION_COMPLETE.md)
**Quick Reference:** [ORACLE_QUICK_START.md](ORACLE_QUICK_START.md)

---

## Features

### Fully Automated (v6.0)
- **100% Hands-Off Account Creation** - No manual intervention required
- **Auto Birthday Selection** - Automatically sets May 3, 2002 (18+ years)
- **Smart Form Filling** - Email and password from Excel
- **Multi-Method Button Clicking** - 3 fallback methods for reliability
- **Automatic Email Code Fetching** - Selenium-based webmail access
- **Automatic CAPTCHA Solving** - 2Captcha API integration (optional)
- **Batch Processing** - Create 1-91+ accounts sequentially
- **Progress Tracking** - CSV logging with success/failure status
- **Resume Support** - Skips already processed accounts

### Human-Like Automation (v6.2)
- **Character-by-Character Typing** - 100-400ms random delays per character
- **Email Checking Simulation** - 8-12 second random wait (mimics human checking inbox)
- **Code Review Pause** - 2-4 second random delay after entering code
- **Natural Interactions** - Uses Playwright's human-like mouse movements
- **Real Browser Fingerprint** - YOUR Chrome with YOUR extensions and settings
- **VPN Integration** - ProtonVPN stays active throughout automation

### Oracle Cloud Integration (v6.1)
- **IP Rotation** - Fresh datacenter IP for each batch
- **VM Automation** - Automatic Oracle VM creation and destruction
- **Free Forever** - Uses Oracle Free Tier (2 x86 VMs)
- **No Proxies Needed** - Saves $50-500/month on proxy services
- **Multiple Regions** - us-phoenix-1, us-ashburn-1, uk-london-1, etc.

### Technical Highlights
- Custom dropdown handling (`div[role='combobox']`)
- Firewall bypass using Selenium for email
- Screenshot debugging
- CAPTCHA detection with 60s pause
- Success detection via URL redirect
- Oracle Cloud API integration via OCI CLI

---

## Quick Start

### Prerequisites
- Python 3.7+
- Chrome browser
- Excel file with account details

### Installation

1. **Install dependencies:**
```bash
pip install -r requirements.txt
```

2. **Create `accounts.xlsx`** with columns:
   - First Name
   - Last Name
   - Email
   - Password

3. **Optional: Enable CAPTCHA Solving**
```bash
# Get API key from https://2captcha.com/
set CAPTCHA_API_KEY=your_api_key_here
```
See [CAPTCHA_SETUP.md](CAPTCHA_SETUP.md) for detailed instructions.

### Usage

**RECOMMENDED - Playwright CDP (v7.0):**
```bash
# One-click method
RUN_WITH_YOUR_CHROME.bat

# Or manual method
START_CHROME_DEBUG.bat                    # Terminal 1: Start Chrome
python core/run_playwright_chrome.py 5    # Terminal 2: Create 5 accounts

# Test connection first
python test_chrome_connection.py
```

**Legacy Methods (Deprecated):**
```bash
start.bat                   # Old method (may not work with Chrome 136+)
python run_chrome_modern.py # Old method
```

**Check Progress:**
```bash
python check_progress.py
```

### Typical Workflow

1. **Morning**: Start Chrome with ProtonVPN → Run script for 10 accounts
2. **Rate Limited?** Switch VPN location (UK → US → Canada)
3. **Continue**: Run another batch of 10 accounts
4. **Repeat**: Create 50-100 accounts per day per VPN location

**Pro Tip:** Use multiple VPN locations throughout the day to avoid rate limits

---

## How It Works

1. Opens TikTok signup page
2. Auto-selects birthday (May 3, 2002)
3. Fills email and password from Excel
4. Clicks "Send code" button
5. **Opens webmail in background Chrome**
6. **Logs in and fetches verification code**
7. Enters code on TikTok automatically
8. Verifies success and saves to CSV
9. Repeats for next account

**Total Time Per Account:** ~30-60 seconds

---

## File Structure

```
TikTok-Account-Creator/
├── core/
│   ├── run_playwright_chrome.py       # ✅ MAIN SCRIPT (v7.0 Playwright CDP)
│   ├── email_fetcher_selenium.py      # Email verification code fetcher
│   ├── proxy_manager.py               # Proxy/VPN rotation manager
│   └── captcha_solver.py              # CAPTCHA solving integration
│
├── START_CHROME_DEBUG.bat             # ✅ Start Chrome with debugging
├── RUN_WITH_YOUR_CHROME.bat           # ✅ One-click launcher
├── test_chrome_connection.py          # ✅ Test CDP connection
│
├── accounts.xlsx                      # Input: Account credentials
├── created_accounts.csv               # Output: Success/failure results
├── processed_accounts.txt             # Processed email list
│
├── requirements.txt                   # Python dependencies
└── README.md                          # This file

Legacy Files (v6.0 and earlier):
├── run_chrome_modern.py               # Old method (deprecated)
├── start.bat                          # Old launcher
└── TROUBLESHOOTING.md                 # Legacy troubleshooting
```

---

## Configuration

### Email Webmail URL
Edit `email_fetcher_selenium.py`:
```python
webmail_url = "https://YOUR-SERVER/mail"
```

### Birthday Settings
Edit `run_chrome_modern.py`:
```python
month = 5   # May
day = 3
year = 2002
```

### Batch Size Limits
Edit `run_chrome_modern.py`:
```python
MAX_BATCH_SIZE = 50          # Max accounts per run
EMAIL_FETCH_DELAY = 5        # Seconds between email fetches
ACCOUNT_DELAY = 3            # Seconds between accounts
```

---

## Troubleshooting

### v7.0 Playwright CDP Issues

**"Could not connect to Chrome on port 9222"**
```bash
# Solution:
1. Make sure START_CHROME_DEBUG.bat is running
2. Check if Chrome opened (look in taskbar)
3. Visit http://localhost:9222/json in another browser
4. If you see JSON data, Chrome is ready

# Test connection:
python test_chrome_connection.py
```

**Chrome 136+ "Remote debugging not working"**
```bash
# Chrome 136+ requires custom user-data-dir
# START_CHROME_DEBUG.bat already handles this
# If still issues, close ALL Chrome windows and retry
```

**"Page timeout" or "Navigation timeout"**
```bash
# Solution: Internet/VPN issue
1. Check ProtonVPN is connected
2. Manually visit tiktok.com in the debug Chrome
3. If it loads, retry the script
```

**"Rate limited" message**
```bash
# Solution: Switch VPN location
1. Change ProtonVPN to different country
2. Wait 2-3 minutes
3. Continue running script
```

### Legacy Issues (v6.0 and earlier)

See [TROUBLESHOOTING.md](TROUBLESHOOTING.md) for detailed solutions.

**ModuleNotFoundError: No module named 'webdriver_manager'**
```bash
pip install webdriver-manager
```

**Birthday dropdowns not found**
- TikTok uses custom dropdowns. Check console for debug info.

**"Send code" button not clicked**
- Script saves screenshot: `before_send_code.png`

**Email fetcher timeout**
- Verify webmail accessible in browser
- Check email credentials
- Script falls back to manual entry

**CAPTCHA appears**
- Script detects and pauses 60 seconds
- Solve manually, script continues automatically

---

## Output Files

### `created_accounts.csv`
```
First Name,Last Name,Email,Password,Status,Notes,Timestamp
John,Doe,john@example.com,Pass123!,Success,Completed automatically,2025-11-10 21:49:45
```

### `processed_accounts.txt`
```
john@example.com
jane@example.com
```

---

## Security

- `.gitignore` configured - Sensitive files excluded
- No hardcoded credentials
- Passwords stored only in Excel (not committed)
- CSV files excluded from Git

**Never commit:**
- `accounts.xlsx`
- `*.csv`
- `*.png` (screenshots)

---

## Requirements

```
selenium>=4.0.0
webdriver-manager>=3.8.0
undetected-chromedriver>=3.5.0
selenium-stealth>=1.0.6
pandas>=1.3.0
openpyxl>=3.0.0
requests>=2.26.0
urllib3>=1.26.0
```

---

## Version History

### v7.0 (November 2025) ✅ **CURRENT - WORKING**
- ✅ **Playwright CDP Connection** - Connects to YOUR Chrome via CDP
- ✅ **Chrome 136+ Compatible** - Works with latest Chrome (requires `--user-data-dir`)
- ✅ **Username Auto-Creation** - Handles post-auth username page
- ✅ **Human-Like Typing** - 100-400ms random delays per character
- ✅ **ProtonVPN Integration** - Uses YOUR browser with YOUR VPN
- ✅ **Rate Limit Detection** - Detects TikTok rate limits
- ✅ **Real Browser Fingerprint** - Zero bot detection
- ✅ **Tested & Verified** - Confirmed working Nov 13, 2025

**This is the closest to full automation achieved.**

### v6.2 (November 2025) - Deprecated
- Microsoft Playwright Integration (early version)
- CDP Connection attempts
- Issues with Chrome 136+ compatibility

### v6.1 (November 2025)
- Oracle Cloud IP rotation
- Automated VM creation/destruction
- Free unlimited datacenter IPs

### v6.0 (November 2025)
- Selenium-based email fetching
- Firewall bypass solution
- 100% automation achieved
- Manual fallback for edge cases

### v5.0
- Custom dropdown handling
- Multi-method button clicking

### v0.0.1 (Original by Hendrik Bgr)
- Basic account creation
- Manual verification required

---

## Improvements Over Original

| Feature | v0.0.1 | v6.0 | v7.0 ✅ |
|---------|--------|------|---------|
| Birthday Selection | Manual | **Automatic** | **Automatic** |
| Email Entry | Manual | **Automatic** | **Human-Like** |
| Send Code Click | Manual | **Automatic** | **Automatic** |
| Code Fetching | Manual | **Automatic** | **Automatic** |
| Username Creation | Manual | Not handled | **Automatic** ✅ |
| Success Detection | Manual | **Automatic** | **Automatic** |
| Batch Processing | No | **Yes (1-91+)** | **Yes (1-91+)** |
| Progress Tracking | Basic | **Advanced CSV** | **Advanced CSV** |
| Browser Control | New Chrome | New Chrome | **YOUR Chrome** ✅ |
| VPN Support | No | Manual | **ProtonVPN Built-in** ✅ |
| Typing Speed | Instant | Instant | **Human (100-400ms)** |
| Bot Detection | High | Medium | **None (CDP)** ✅ |
| Chrome 136+ Support | N/A | ❌ Broken | ✅ **Working** |
| Rate Limit Handling | None | Basic | **Detected** ✅ |

---

## Legal Disclaimer

**Educational purposes only.** Users are responsible for:
- Complying with TikTok's Terms of Service
- Not using for spam or malicious purposes
- Following all applicable laws

Use responsibly and ethically.

---

## Credits

- **Original Author:** [Hendrik Bgr](https://github.com/hendrikbgr)
- **Full Automation:** memoriesdead

---

## License

Educational purposes. See original repository for licensing. 
