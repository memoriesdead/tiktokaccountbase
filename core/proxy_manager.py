"""
Smart Proxy Manager with Rate Limit Detection & Auto-Switching
================================================================
Handles intelligent proxy rotation when TikTok rate limits are detected.

Features:
- Proxy blacklist tracking (temporary ban list)
- Cooldown periods for rate-limited proxies
- Smart proxy selection (avoids recently failed IPs)
- Usage statistics and logging
"""

import json
import time
import random
import sys
import io
import os
from datetime import datetime, timedelta

# Fix Windows console encoding
if sys.platform == 'win32':
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')
    sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8', errors='replace')


class ProxyManager:
    """Manages proxy rotation with intelligent rate limit handling"""

    def __init__(self, proxy_config_path='proxy_config.json', cooldown_minutes=30):
        """
        Initialize proxy manager

        Args:
            proxy_config_path: Path to proxy_config.json
            cooldown_minutes: How long to blacklist a rate-limited proxy (default: 30 min)
        """
        self.config_path = proxy_config_path
        self.cooldown_minutes = cooldown_minutes
        self.proxies = []
        self.blacklist = {}  # {proxy_host: timestamp_when_banned}
        self.usage_stats = {}  # {proxy_host: {'success': 0, 'failed': 0, 'rate_limited': 0}}
        self.last_used_index = -1

        self._load_proxies()

    def _load_proxies(self):
        """Load proxies from JSON config"""
        try:
            # If running from core/ directory, look in parent directory
            if not os.path.exists(self.config_path):
                parent_path = os.path.join('..', self.config_path)
                if os.path.exists(parent_path):
                    self.config_path = parent_path

            with open(self.config_path, 'r') as f:
                data = json.load(f)

            # Handle both formats: list or dict with "proxies" key
            if isinstance(data, list):
                self.proxies = data
            elif isinstance(data, dict) and 'proxies' in data:
                self.proxies = data['proxies']
            else:
                print(f"⚠ Warning: Unexpected format in {self.config_path}")
                self.proxies = []
                return

            print(f"✓ Loaded {len(self.proxies)} proxies from {self.config_path}")
        except FileNotFoundError:
            print(f"⚠ Warning: {self.config_path} not found!")
            self.proxies = []
        except json.JSONDecodeError:
            print(f"⚠ Warning: Invalid JSON in {self.config_path}")
            self.proxies = []

    def get_available_proxies(self):
        """Get list of proxies that are NOT currently blacklisted"""
        current_time = time.time()
        available = []

        for proxy in self.proxies:
            host = proxy['host']

            # Check if proxy is blacklisted
            if host in self.blacklist:
                banned_time = self.blacklist[host]
                time_since_ban = current_time - banned_time
                cooldown_seconds = self.cooldown_minutes * 60

                # Remove from blacklist if cooldown period has passed
                if time_since_ban >= cooldown_seconds:
                    print(f"   ✓ Proxy {host} cooldown expired (was banned {int(time_since_ban/60)} min ago)")
                    del self.blacklist[host]
                    available.append(proxy)
                else:
                    remaining = int((cooldown_seconds - time_since_ban) / 60)
                    # print(f"   ⏳ Proxy {host} still cooling down ({remaining} min remaining)")
                    continue
            else:
                available.append(proxy)

        return available

    def get_next_proxy(self, strategy='smart'):
        """
        Get next proxy to use

        Args:
            strategy: 'smart' (avoid recent failures), 'round_robin', or 'random'

        Returns:
            dict: Proxy configuration or None if no proxies available
        """
        available = self.get_available_proxies()

        if not available:
            print("\n⚠ WARNING: All proxies are rate-limited!")
            print(f"   Waiting for cooldown ({self.cooldown_minutes} minutes)...")
            print(f"   Blacklisted: {len(self.blacklist)} proxies")

            # Use the proxy that was banned longest ago (closest to cooldown expiry)
            if self.blacklist:
                oldest_banned = min(self.blacklist.items(), key=lambda x: x[1])
                oldest_host = oldest_banned[0]
                print(f"   Using oldest banned proxy: {oldest_host} (desperate mode)")

                # Find the proxy object
                for proxy in self.proxies:
                    if proxy['host'] == oldest_host:
                        return proxy

            return None

        if strategy == 'smart':
            # Prefer proxies with fewer failures
            available_sorted = sorted(
                available,
                key=lambda p: self.usage_stats.get(p['host'], {}).get('rate_limited', 0)
            )
            return available_sorted[0]

        elif strategy == 'random':
            return random.choice(available)

        elif strategy == 'round_robin':
            self.last_used_index = (self.last_used_index + 1) % len(available)
            return available[self.last_used_index]

        else:
            return available[0]

    def mark_rate_limited(self, proxy):
        """
        Mark a proxy as rate-limited (add to blacklist)

        Args:
            proxy: Proxy dict with 'host' key
        """
        host = proxy['host']
        self.blacklist[host] = time.time()

        # Update stats
        if host not in self.usage_stats:
            self.usage_stats[host] = {'success': 0, 'failed': 0, 'rate_limited': 0}
        self.usage_stats[host]['rate_limited'] += 1

        print(f"\n🚫 PROXY BLACKLISTED: {host}")
        print(f"   → Cooldown: {self.cooldown_minutes} minutes")
        print(f"   → Total rate limits for this proxy: {self.usage_stats[host]['rate_limited']}")
        print(f"   → Available proxies: {len(self.get_available_proxies())}/{len(self.proxies)}")

    def mark_success(self, proxy):
        """Mark a proxy as successful"""
        host = proxy['host']
        if host not in self.usage_stats:
            self.usage_stats[host] = {'success': 0, 'failed': 0, 'rate_limited': 0}
        self.usage_stats[host]['success'] += 1

    def mark_failed(self, proxy, reason='unknown'):
        """Mark a proxy as failed (non-rate-limit failure)"""
        host = proxy['host']
        if host not in self.usage_stats:
            self.usage_stats[host] = {'success': 0, 'failed': 0, 'rate_limited': 0}
        self.usage_stats[host]['failed'] += 1

    def get_stats(self):
        """Get usage statistics for all proxies"""
        return {
            'total_proxies': len(self.proxies),
            'available_proxies': len(self.get_available_proxies()),
            'blacklisted_proxies': len(self.blacklist),
            'usage_stats': self.usage_stats
        }

    def print_stats(self):
        """Print proxy usage statistics"""
        stats = self.get_stats()
        print("\n" + "="*60)
        print("PROXY STATISTICS")
        print("="*60)
        print(f"Total Proxies: {stats['total_proxies']}")
        print(f"Available: {stats['available_proxies']}")
        print(f"Blacklisted: {stats['blacklisted_proxies']}")
        print()

        if stats['usage_stats']:
            print("Per-Proxy Stats:")
            for host, data in sorted(stats['usage_stats'].items(),
                                    key=lambda x: x[1].get('rate_limited', 0),
                                    reverse=True):
                print(f"  {host}:")
                print(f"    ✓ Success: {data.get('success', 0)}")
                print(f"    ✗ Failed: {data.get('failed', 0)}")
                print(f"    🚫 Rate Limited: {data.get('rate_limited', 0)}")

        print("="*60 + "\n")

    def clear_blacklist(self):
        """Clear all blacklisted proxies (emergency use)"""
        count = len(self.blacklist)
        self.blacklist.clear()
        print(f"✓ Cleared {count} proxies from blacklist")


# Convenience function for quick usage
def create_proxy_manager(cooldown_minutes=30):
    """Create a ProxyManager instance with default settings"""
    return ProxyManager(cooldown_minutes=cooldown_minutes)


if __name__ == "__main__":
    # Test the proxy manager
    print("Testing Proxy Manager...")
    pm = ProxyManager(cooldown_minutes=5)  # 5 min cooldown for testing

    # Get first proxy
    proxy1 = pm.get_next_proxy()
    if proxy1:
        print(f"\nGot proxy: {proxy1['host']}")

        # Simulate rate limit
        pm.mark_rate_limited(proxy1)

        # Try to get another proxy
        proxy2 = pm.get_next_proxy()
        if proxy2:
            print(f"Got different proxy: {proxy2['host']}")

        # Print stats
        pm.print_stats()
