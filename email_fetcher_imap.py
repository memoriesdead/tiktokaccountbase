# IMAP Email Verification Code Fetcher
# Uses IMAP protocol (same as email clients) to fetch TikTok codes

import imaplib
import email
import re
import time
from email.header import decode_header

class IMAPEmailFetcher:
    def __init__(self, imap_server="170.9.13.229", imap_port=993):
        self.imap_server = imap_server
        self.imap_port = imap_port
        self.mail = None

    def login(self, email_address, password):
        """Login to email via IMAP"""

        # Try multiple ports (993 SSL, 143 standard)
        ports_to_try = [993, 143]

        for port in ports_to_try:
            try:
                print(f"   Trying {self.imap_server}:{port}...")

                if port == 993:
                    # SSL connection
                    self.mail = imaplib.IMAP4_SSL(self.imap_server, port, timeout=10)
                else:
                    # Non-SSL connection
                    self.mail = imaplib.IMAP4(self.imap_server, port, timeout=10)

                print(f"   Connected! Logging in as {email_address}...")
                self.mail.login(email_address, password)

                print(f"   [OK] Logged in successfully on port {port}")
                return True

            except imaplib.IMAP4.error as e:
                print(f"   [ERROR] IMAP login error on port {port}: {e}")
                continue
            except Exception as e:
                print(f"   [ERROR] Connection failed on port {port}: {str(e)[:50]}")
                continue

        print("   [FAILED] Could not connect on any IMAP port")
        return False

    def fetch_verification_code(self, max_attempts=18, wait_seconds=5):
        """Fetch TikTok verification code from inbox"""
        try:
            # Select inbox
            self.mail.select("INBOX")

            for attempt in range(max_attempts):
                # Search for ALL emails (we'll filter by date)
                # Search for emails from TikTok or with verification/code in subject
                search_criteria = '(OR (FROM "tiktok") (SUBJECT "verification") (SUBJECT "code"))'

                status, messages = self.mail.search(None, search_criteria)

                if status != "OK":
                    print(f"   [DEBUG] Search failed: {status}")
                    time.sleep(wait_seconds)
                    continue

                message_ids = messages[0].split()

                if attempt == 0:
                    print(f"   [DEBUG] Found {len(message_ids)} TikTok/verification emails total")

                if not message_ids:
                    if attempt < max_attempts - 1:
                        print(f"   Waiting for email... (attempt {attempt + 1}/{max_attempts})")
                        time.sleep(wait_seconds)
                    continue

                # Check the most recent emails first (last 5)
                recent_ids = message_ids[-5:] if len(message_ids) > 5 else message_ids

                for msg_id in reversed(recent_ids):  # Most recent first
                    try:
                        # Fetch the email
                        status, msg_data = self.mail.fetch(msg_id, "(RFC822)")

                        if status != "OK":
                            continue

                        # Parse email
                        email_body = msg_data[0][1]
                        email_message = email.message_from_bytes(email_body)

                        # Get subject
                        subject = email_message.get("Subject", "")
                        if subject:
                            subject, encoding = decode_header(subject)[0]
                            if isinstance(subject, bytes):
                                subject = subject.decode(encoding or "utf-8")

                        # Get from
                        from_addr = email_message.get("From", "")

                        # Get date
                        date = email_message.get("Date", "")

                        print(f"   [DEBUG] Checking email: From={from_addr[:30]}, Subject={subject[:40]}")

                        # Check if it's from TikTok
                        if 'tiktok' not in from_addr.lower() and 'tiktok' not in subject.lower():
                            continue

                        print(f"   [DEBUG] Found TikTok email! Extracting code...")

                        # Get email body
                        body = ""
                        if email_message.is_multipart():
                            for part in email_message.walk():
                                content_type = part.get_content_type()
                                if content_type == "text/plain" or content_type == "text/html":
                                    try:
                                        body += part.get_payload(decode=True).decode()
                                    except:
                                        pass
                        else:
                            try:
                                body = email_message.get_payload(decode=True).decode()
                            except:
                                pass

                        # Look for 6-digit code
                        code_match = re.search(r'\b(\d{6})\b', body)

                        if code_match:
                            code = code_match.group(1)
                            print(f"   ✓✓ SUCCESS! Found code: {code}")
                            return code
                        else:
                            print(f"   [DEBUG] TikTok email found but no 6-digit code")

                    except Exception as e:
                        print(f"   [DEBUG] Error reading email: {e}")
                        continue

                # Wait before next attempt
                if attempt < max_attempts - 1:
                    print(f"   Waiting for email... (attempt {attempt + 1}/{max_attempts})")
                    time.sleep(wait_seconds)

            print(f"   ✗ No verification code found after {max_attempts} attempts")
            return None

        except Exception as e:
            print(f"   ✗ Error fetching code: {e}")
            return None

    def logout(self):
        """Logout from IMAP"""
        try:
            if self.mail:
                self.mail.close()
                self.mail.logout()
        except:
            pass


def get_verification_code_imap(email_address, password, max_wait=90):
    """
    Main function to get verification code via IMAP

    Args:
        email_address: Your email (e.g. eveline.ross@pumplabsweb3.com)
        password: Your email password
        max_wait: Maximum seconds to wait for email (default 90)

    Returns:
        6-digit verification code or None
    """
    print(f"\nFetching verification code via IMAP for: {email_address}")

    fetcher = IMAPEmailFetcher()

    if not fetcher.login(email_address, password):
        return None

    max_attempts = max_wait // 5  # Check every 5 seconds
    code = fetcher.fetch_verification_code(max_attempts=max_attempts, wait_seconds=5)

    fetcher.logout()

    return code


# Test function
if __name__ == "__main__":
    print("Testing IMAP Email Fetcher...")
    print("="*60)

    test_email = "eveline.ross@pumplabsweb3.com"
    test_password = "Welcome2025!"

    code = get_verification_code_imap(test_email, test_password, max_wait=30)

    if code:
        print(f"\n✓ Code retrieved: {code}")
    else:
        print("\n✗ No code found")
