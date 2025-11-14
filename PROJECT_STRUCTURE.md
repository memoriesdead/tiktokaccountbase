# TikTok Account Creator - Clean Project Structure

## 📁 Active Files (What You Need)

### Main Scripts
- **RUN_WITH_MANUAL_VPN.py** - 🎯 MAIN SCRIPT - Semi-automated account creator with VPN switching support
- **OPEN_YOUR_EDGE.bat** - Opens Edge browser with debug port for automation

### Core Automation Files (core/)
- **run_chrome_modern.py** - Main automation engine (works with Edge via run_edge_modern.py)
- **run_edge_modern.py** - Edge adapter that connects to your existing Edge browser
- **email_fetcher_selenium.py** - Auto-fetches verification codes from webmail
- **proxy_manager.py** - Manages proxy rotation (optional, not actively used)
- **captcha_solver.py** - CAPTCHA solving utilities (if needed)

### Configuration Files
- **accounts.xlsx** - Account credentials to create (First Name, Last Name, email, password)
- **proxy_config.json** - 50 rotating proxy IPs from Webshare (for future use)
- **requirements.txt** - Python dependencies

### Data/Results
- **core/created_accounts.csv** - Log of created accounts
- **core/before_send_code.png** - Screenshot before clicking "Send code" button
- **data/** - Additional data files
- **results/** - Results and logs

---

## 🗂️ Archived Files (Old/Unused)

### archive/chrome_fixes/
- Chrome troubleshooting files (not needed - using Edge now)
- FIX_SMARTSCREEN_PERMANENT.reg
- RESTORE_CHROME_ACCESS.bat
- CHROME_FIX_GUIDE.md
- SIMPLE_START_CHROME.bat
- PERMANENT_FIX_INSTRUCTIONS.md

### archive/old_scripts/
- run_simple.py - Old simple version
- START_EDGE_DEBUG.bat - Replaced by OPEN_YOUR_EDGE.bat
- START_EDGE_AND_RUN.py - Replaced by RUN_WITH_MANUAL_VPN.py
- run_edge_with_proxy.py - Proxy version (not working)
- create_proxy_extension.py - Chrome extension creator (not needed for Edge)

### archive/ (other)
- CLEANUP_COMPLETE.md - Previous cleanup documentation

---

## 🚀 How to Use

### Setup (One Time):
1. Install dependencies: `pip install -r requirements.txt`
2. Add account info to `accounts.xlsx`
3. Install ProtonVPN extension in Edge

### Run Automation:
```bash
python RUN_WITH_MANUAL_VPN.py 3
```

### Workflow:
1. Script opens Edge automatically
2. Fills forms and fetches codes
3. When "max attempts" appears → You switch VPN
4. Press Enter → Script retries automatically
5. Repeats until account succeeds
6. Moves to next account

---

## 📊 Current Stats
- Accounts in Excel: 1 (Ahmed Benali)
- Available Proxies: 50 (not actively used)
- Success Rate: Depends on VPN switching

---

## 🔧 Troubleshooting

**Edge won't connect?**
- Run `OPEN_YOUR_EDGE.bat` manually first
- Wait 10 seconds for Edge to fully start

**No verification email?**
- Switch VPN to different country
- Try again with same account

**"Max attempts" error?**
- Switch ProtonVPN server
- Press Enter to retry

---

## 📝 Notes
- Birthday is hardcoded to May 3, 2002
- Email verification is automatic via Selenium webmail access
- Each account needs fresh IP (manual VPN switch)
- No time limits - runs until successful
