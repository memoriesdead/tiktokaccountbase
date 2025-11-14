# Codebase Cleanup Plan

**Date:** November 13, 2025
**Version:** 7.0 - After Playwright CDP Implementation

---

## 📁 **Current Status**

We now use **Playwright CDP (v7.0)** which makes many old files obsolete.

---

## ✅ **Files to KEEP (Active)**

### **Core Scripts**
- ✅ `core/run_playwright_chrome.py` - **MAIN SCRIPT** (v7.0)
- ✅ `core/email_fetcher_selenium.py` - Email verification fetcher
- ✅ `core/captcha_solver.py` - CAPTCHA integration
- ✅ `core/proxy_manager.py` - Proxy/VPN manager

### **Batch Files**
- ✅ `START_CHROME_DEBUG.bat` - Start Chrome for CDP
- ✅ `RUN_WITH_YOUR_CHROME.bat` - One-click launcher

### **Test/Utility**
- ✅ `test_chrome_connection.py` - CDP connection test

### **Data Files**
- ✅ `accounts.xlsx` - Input accounts
- ✅ `created_accounts.csv` - Output results
- ✅ `requirements.txt` - Dependencies

### **Documentation**
- ✅ `README.md` - Main documentation
- ✅ `V7_RELEASE_NOTES.md` - v7.0 release notes
- ✅ `INSTAGRAM.md` - Instagram adaptation guide
- ✅ `PROJECT_STRUCTURE.md` - Project overview

---

## 🗑️ **Files to MOVE TO ARCHIVE (Deprecated)**

### **Old Scripts (v6.0 and earlier)**
- ❌ `core/run_chrome_modern.py` - Old undetected-chromedriver method
- ❌ `core/run_edge_modern.py` - Edge browser attempt
- ❌ `RUN_FRESH_PROFILE.py` - Old method
- ❌ `RUN_WITH_MANUAL_VPN.py` - Deprecated

### **Old Batch Files**
- ❌ `OPEN_YOUR_EDGE.bat` - Edge launcher (deprecated)

### **Temporary/Debug Files**
- ❌ `nul` - Windows null file artifact
- ❌ `Screenshot 2025-11-13 195218.png` - Debug screenshot
- ❌ `Screenshot 2025-11-13 203921.png` - Debug screenshot
- ❌ `core/before_send_code.png` - Debug screenshot

### **Empty/Unused**
- ❌ `proxy_config.json` - Not used with manual VPN
- ❌ `proxy.gif` - Demo file

---

## 📂 **Folders to KEEP**

- ✅ `core/` - Core scripts
- ✅ `archive/` - Old versions (already archived)
- ✅ `docs/` - Documentation
- ✅ `data/` - Data files
- ✅ `results/` - Output results
- ✅ `__pycache__/` - Python cache (auto-generated)

---

## 🚀 **Cleanup Actions**

### **Action 1: Move Deprecated Scripts**
```bash
# Move old scripts to archive
mkdir -p archive/v6_deprecated
mv core/run_chrome_modern.py archive/v6_deprecated/
mv core/run_edge_modern.py archive/v6_deprecated/
mv RUN_FRESH_PROFILE.py archive/v6_deprecated/
mv RUN_WITH_MANUAL_VPN.py archive/v6_deprecated/
mv OPEN_YOUR_EDGE.bat archive/v6_deprecated/
```

### **Action 2: Clean Debug Files**
```bash
# Move screenshots to archive
mkdir -p archive/debug_screenshots
mv "Screenshot 2025-11-13 195218.png" archive/debug_screenshots/
mv "Screenshot 2025-11-13 203921.png" archive/debug_screenshots/
mv core/before_send_code.png archive/debug_screenshots/
```

### **Action 3: Remove Artifacts**
```bash
# Remove null file
rm nul

# Remove unused config
mv proxy_config.json archive/unused/
mv proxy.gif archive/unused/
```

### **Action 4: Clean Python Cache**
```bash
# Remove Python cache (will regenerate)
rm -rf __pycache__
rm -rf core/__pycache__
```

---

## 📋 **Final Structure (After Cleanup)**

```
TikTok-Account-Creator/
├── core/
│   ├── run_playwright_chrome.py       ✅ MAIN (v7.0)
│   ├── email_fetcher_selenium.py      ✅ Email fetcher
│   ├── proxy_manager.py               ✅ Proxy manager
│   └── captcha_solver.py              ✅ CAPTCHA solver
│
├── archive/
│   ├── v6_deprecated/                 📦 Old scripts
│   ├── debug_screenshots/             📦 Screenshots
│   └── unused/                        📦 Unused files
│
├── docs/                              📚 Documentation
├── data/                              💾 Data files
├── results/                           📊 Results
│
├── START_CHROME_DEBUG.bat             ✅ Chrome launcher
├── RUN_WITH_YOUR_CHROME.bat           ✅ One-click run
├── test_chrome_connection.py          ✅ Connection test
│
├── accounts.xlsx                      ✅ Input
├── created_accounts.csv               ✅ Output
│
├── README.md                          📖 Main docs
├── V7_RELEASE_NOTES.md                📖 Release notes
├── INSTAGRAM.md                       📖 Instagram guide
├── PROJECT_STRUCTURE.md               📖 Structure
├── CLEANUP_PLAN.md                    📖 This file
│
└── requirements.txt                   ⚙️ Dependencies
```

---

## 🎯 **Benefits of Cleanup**

1. **Clarity** - Only v7.0 files in root
2. **Less Confusion** - No mixing old/new methods
3. **Faster Navigation** - Easier to find files
4. **Git Clean** - Cleaner repository
5. **Maintenance** - Easier to maintain

---

## ⚠️ **Important Notes**

### **DO NOT Delete Archive Folder**
- Contains old scripts that might be referenced
- Historical record of development
- Can revert if needed

### **Keep Git History**
- Use `git mv` instead of `rm` for tracked files
- Preserves file history

### **Backup First**
- Consider creating a full backup before cleanup
- ZIP the entire folder

---

## ✅ **Cleanup Checklist**

- [ ] Backup entire folder
- [ ] Move deprecated scripts to archive/v6_deprecated/
- [ ] Move screenshots to archive/debug_screenshots/
- [ ] Move unused files to archive/unused/
- [ ] Remove `nul` artifact
- [ ] Clean __pycache__ folders
- [ ] Test that v7.0 script still works
- [ ] Update .gitignore if needed
- [ ] Commit cleanup changes

---

## 🚀 **Run Cleanup**

Execute the cleanup script:
```bash
# Windows (PowerShell or Git Bash)
bash cleanup.sh

# Or run commands manually from this plan
```

---

**After cleanup, you'll have a clean v7.0 codebase with only active files!**
