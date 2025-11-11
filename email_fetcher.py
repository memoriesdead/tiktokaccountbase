# Auto Email Verification Code Fetcher
# Fetches TikTok verification codes from your Oracle Cloud webmail

import requests
import re
import time
from urllib3.exceptions import InsecureRequestWarning
requests.packages.urllib3.disable_warnings(InsecureRequestWarning)

class WebmailFetcher:
    def __init__(self, webmail_url="https://170.9.13.229/mail"):
        self.webmail_url = webmail_url
        self.session = requests.Session()
        self.session.verify = False  # For self-signed SSL certificates
        # Increase timeout to 30 seconds
        self.timeout = 30

    def login(self, email, password):
        """Login to webmail"""
        try:
            # Try Roundcube login
            login_url = f"{self.webmail_url}/"

            # Get login page first
            response = self.session.get(login_url, verify=False, timeout=self.timeout, allow_redirects=True)

            # Extract token if exists
            token_match = re.search(r'name="_token"\s+value="([^"]+)"', response.text)
            token = token_match.group(1) if token_match else ""

            # Login data
            login_data = {
                '_task': 'login',
                '_action': 'login',
                '_user': email,
                '_pass': password,
                '_token': token
            }

            # Post login
            response = self.session.post(login_url, data=login_data, verify=False, timeout=self.timeout)

            # Check if login successful
            if '_task=mail' in response.url or 'INBOX' in response.text:
                print(f"   Logged in to {email}")
                return True
            else:
                print(f"   Login failed for {email}")
                return False

        except Exception as e:
            print(f"   Login error: {str(e)}")
            return False

    def fetch_verification_code(self, max_attempts=12, wait_seconds=5):
        """Fetch TikTok verification code from inbox"""
        try:
            for attempt in range(max_attempts):
                # Fetch inbox
                inbox_url = f"{self.webmail_url}/?_task=mail&_action=list&_mbox=INBOX&_refresh=1"
                response = self.session.get(inbox_url, verify=False, timeout=self.timeout)

                # Debug: Show what we got
                if attempt == 0:
                    print(f"   [DEBUG] Inbox response length: {len(response.text)}")
                    if 'tiktok' in response.text.lower():
                        print("   [DEBUG] Found 'tiktok' in inbox!")
                    if 'verification' in response.text.lower():
                        print("   [DEBUG] Found 'verification' in inbox!")

                # Find ALL message IDs (most recent first)
                uid_matches = re.findall(r'"uid":"?(\d+)"?', response.text)

                if uid_matches:
                    print(f"   [DEBUG] Found {len(uid_matches)} messages in inbox")

                    # Check each message (starting with most recent)
                    for uid in uid_matches[:5]:  # Check up to 5 most recent messages
                        try:
                            # Fetch the email content
                            message_url = f"{self.webmail_url}/?_task=mail&_action=show&_mbox=INBOX&_uid={uid}"
                            msg_response = self.session.get(message_url, verify=False, timeout=self.timeout)

                            msg_text = msg_response.text.lower()

                            # Check if this is a TikTok email
                            if 'tiktok' in msg_text or 'verification' in msg_text:
                                print(f"   [DEBUG] Found TikTok/verification email (UID: {uid})")

                                # Extract verification code (6 digits)
                                code_match = re.search(r'\b(\d{6})\b', msg_response.text)

                                if code_match:
                                    code = code_match.group(1)
                                    print(f"   SUCCESS! Found verification code: {code}")
                                    return code
                                else:
                                    print(f"   [DEBUG] Email found but no 6-digit code in UID {uid}")
                        except Exception as e:
                            print(f"   [DEBUG] Error checking UID {uid}: {e}")
                            continue
                else:
                    print(f"   [DEBUG] No messages found in inbox")

                # Wait before next attempt
                if attempt < max_attempts - 1:
                    print(f"   Waiting for email... (attempt {attempt + 1}/{max_attempts})")
                    time.sleep(wait_seconds)

            print(f"   No verification code found after {max_attempts} attempts")
            return None

        except Exception as e:
            print(f"   Error fetching code: {str(e)}")
            return None

    def logout(self):
        """Logout from webmail"""
        try:
            logout_url = f"{self.webmail_url}/?_task=logout"
            self.session.get(logout_url, verify=False, timeout=5)
        except:
            pass

def get_verification_code(email, password, max_wait=60):
    """
    Main function to get verification code

    Args:
        email: Email address
        password: Email password
        max_wait: Maximum seconds to wait for email (default 60)

    Returns:
        Verification code string or None
    """
    print(f"\n Fetching verification code for: {email}")

    fetcher = WebmailFetcher()

    # Login
    if not fetcher.login(email, password):
        return None

    # Wait and fetch code
    code = fetcher.fetch_verification_code(max_attempts=int(max_wait/5), wait_seconds=5)

    # Logout
    fetcher.logout()

    return code

# Test function
if __name__ == "__main__":
    print("Testing Email Fetcher...")
    print("=" * 60)

    # Test with first account
    test_email = "eveline.ross@pumplabsweb3.com"
    test_password = "Welcome2025!"

    print(f"Testing with: {test_email}")
    print("NOTE: This will only work if there's a recent TikTok email")
    print("=" * 60)

    code = get_verification_code(test_email, test_password)

    if code:
        print(f"\n SUCCESS! Code: {code}")
    else:
        print(f"\n Could not fetch code")
