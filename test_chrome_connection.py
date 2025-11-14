#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Quick test to verify Playwright can connect to Chrome

from playwright.sync_api import sync_playwright
import sys
import io

# Fix Windows console encoding
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')

print("=" * 60)
print("Testing Playwright CDP Connection to Chrome")
print("=" * 60)

try:
    with sync_playwright() as playwright:
        print("\n[1/3] Connecting to Chrome on port 9222...")

        browser = playwright.chromium.connect_over_cdp("http://localhost:9222")
        print("[OK] Successfully connected to Chrome!")

        print("\n[2/3] Getting browser contexts...")
        if len(browser.contexts) > 0:
            context = browser.contexts[0]
            print(f"[OK] Found {len(browser.contexts)} context(s)")

            print("\n[3/3] Getting pages...")
            if len(context.pages) > 0:
                page = context.pages[0]
                print(f"[OK] Found {len(context.pages)} page(s)")

                print(f"\n   Current URL: {page.url}")
                print(f"   Page Title: {page.title()}")

                print("\n" + "=" * 60)
                print("CONNECTION SUCCESSFUL!")
                print("=" * 60)
                print("\nYour Chrome is ready for automation!")
                print("You can now run: python core\\run_playwright_chrome.py")
                sys.exit(0)
            else:
                print("[ERROR] No pages found. Open a new tab in Chrome.")
                sys.exit(1)
        else:
            print("[ERROR] No contexts found!")
            sys.exit(1)

except Exception as e:
    print(f"\n[ERROR] Connection failed!")
    print(f"   Error: {str(e)}")
    print("\n" + "=" * 60)
    print("TROUBLESHOOTING:")
    print("=" * 60)
    print("1. Make sure Chrome is running (check taskbar)")
    print("2. Run START_CHROME_DEBUG.bat if Chrome is not open")
    print("3. Check http://localhost:9222/json in another browser")
    print("4. Close all Chrome windows and try again")
    print("=" * 60)
    sys.exit(1)
