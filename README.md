# TikTok Account Creator - Fully Automated 🤖

**Version 6.0** - 100% Automated TikTok account creation with automatic email verification

Original concept by [Hendrik Bgr](https://github.com/hendrikbgr) - Enhanced with full automation by memoriesdead

---

## ✨ Features

### ✅ Fully Automated (v6.0)
- **100% Hands-Off Account Creation** - No manual intervention required
- **Auto Birthday Selection** - Automatically sets May 3, 2002 (18+ years)
- **Smart Form Filling** - Email and password from Excel
- **Multi-Method Button Clicking** - 3 fallback methods for reliability
- **Automatic Email Code Fetching** - Selenium-based webmail access
- **Batch Processing** - Create 1-91+ accounts sequentially
- **Progress Tracking** - CSV logging with success/failure status
- **Resume Support** - Skips already processed accounts

### 🔧 Technical Highlights
- Custom dropdown handling (`div[role='combobox']`)
- Firewall bypass using Selenium for email
- Screenshot debugging
- CAPTCHA detection with 60s pause
- Success detection via URL redirect

---

## 🚀 Quick Start

### Prerequisites
- Python 3.7+
- Chrome browser
- Excel file with account details

### Installation

1. **Clone repository:**
```bash
git clone https://github.com/memoriesdead/automationbase.git
cd automationbase
```

2. **Install dependencies:**
```bash
pip install -r requirements.txt
```

3. **Create `accounts.xlsx`** with columns:
   - First Name
   - Last Name
   - Email
   - Password

### Usage

**Windows (Recommended):**
```bash
start.bat
```

**Manual:**
```bash
python run_chrome_modern.py
```

---

## 📋 How It Works

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

## 📁 File Structure

```
TikTok-Account-Creator/
├── run_chrome_modern.py           # Main script (v6.0)
├── email_fetcher_selenium.py      # Selenium email fetcher
├── email_fetcher.py               # HTTP email fetcher (fallback)
├── check_email_ports.py           # Port checker
│
├── accounts.xlsx                  # Input: Credentials
├── created_accounts.csv           # Output: Results
├── processed_accounts.txt         # Processed emails
│
├── start.bat                      # Windows launcher
├── requirements.txt               # Dependencies
└── README.md                      # This file
```

---

## ⚙️ Configuration

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

---

## 🐛 Troubleshooting

### Birthday dropdowns not found
TikTok uses custom dropdowns. Check console for debug info.

### "Send code" button not clicked
Script saves screenshot: `before_send_code.png`

### Email fetcher timeout
- Verify webmail accessible in browser
- Check email credentials
- Script falls back to manual entry

### CAPTCHA appears
Script detects and pauses 60 seconds. Solve manually, script continues.

---

## 📊 Output Files

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

## 🔒 Security

- ✅ `.gitignore` configured - Sensitive files excluded
- ✅ No hardcoded credentials
- ✅ Passwords stored only in Excel (not committed)
- ✅ CSV files excluded from Git

**Never commit:**
- `accounts.xlsx`
- `*.csv`
- `*.png` (screenshots)

---

## 📝 Requirements

```
selenium>=4.0.0
webdriver-manager>=3.8.0
pandas>=1.3.0
openpyxl>=3.0.0
requests>=2.26.0
urllib3>=1.26.0
```

---

## 📜 Version History

### v6.0 (Current - November 2025)
- ✅ Selenium-based email fetching
- ✅ Firewall bypass solution
- ✅ 100% automation achieved
- ✅ Manual fallback for edge cases

### v5.0
- ✅ Custom dropdown handling
- ✅ Multi-method button clicking

### v0.0.1 (Original by Hendrik Bgr)
- Basic account creation
- Manual verification required

---

## 🎯 Improvements Over Original

| Feature | v0.0.1 | v6.0 |
|---------|--------|------|
| Birthday Selection | Manual | **Automatic** |
| Email Entry | Manual | **Automatic** |
| Send Code Click | Manual | **Automatic** |
| Code Fetching | Manual | **Automatic** |
| Success Detection | Manual | **Automatic** |
| Batch Processing | No | **Yes (1-91+)** |
| Progress Tracking | Basic | **Advanced CSV** |

---

## ⚖️ Legal Disclaimer

**Educational purposes only.** Users are responsible for:
- Complying with TikTok's Terms of Service
- Not using for spam or malicious purposes
- Following all applicable laws

Use responsibly and ethically.

---

## 🤝 Contributing

1. Fork the repository
2. Create feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit changes (`git commit -m 'Add AmazingFeature'`)
4. Push to branch (`git push origin feature/AmazingFeature`)
5. Open Pull Request

---

## 📧 Support

- Open an issue on GitHub
- Check existing issues for solutions

---

## 👥 Credits

- **Original Author:** [Hendrik Bgr](https://github.com/hendrikbgr)
- **Full Automation:** memoriesdead
- **Community Contributors:** Thank you! ❤️

---

## 📄 License

Educational purposes. See original repository for licensing.

---

**⭐ Star this repo if you find it helpful!**

**Made with ❤️ by the automation community** 
