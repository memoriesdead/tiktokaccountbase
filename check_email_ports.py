# Check which email ports are available on Oracle server
import socket
import ssl

def check_port(host, port, timeout=5):
    """Check if a port is open"""
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(timeout)
        result = sock.connect_ex((host, port))
        sock.close()
        return result == 0
    except:
        return False

def check_ssl_port(host, port, timeout=5):
    """Check if SSL port is open"""
    try:
        context = ssl.create_default_context()
        context.check_hostname = False
        context.verify_mode = ssl.CERT_NONE

        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(timeout)
        ssock = context.wrap_socket(sock, server_hostname=host)
        result = ssock.connect_ex((host, port))
        ssock.close()
        return result == 0
    except:
        return False

host = "170.9.13.229"

print(f"Checking available ports on {host}...")
print("="*60)

# Email ports to check
ports = {
    25: "SMTP (standard)",
    465: "SMTP (SSL)",
    587: "SMTP (TLS/STARTTLS)",
    110: "POP3 (standard)",
    995: "POP3 (SSL)",
    143: "IMAP (standard)",
    993: "IMAP (SSL)",
    80: "HTTP",
    443: "HTTPS (webmail)",
    8080: "HTTP alternate",
    8443: "HTTPS alternate"
}

open_ports = []

for port, description in ports.items():
    print(f"Checking port {port} ({description})...", end=" ")

    # Try SSL first for common SSL ports
    if port in [443, 465, 993, 995, 8443]:
        is_open = check_ssl_port(host, port)
    else:
        is_open = check_port(host, port)

    if is_open:
        print("[OPEN]")
        open_ports.append((port, description))
    else:
        print("[CLOSED/FILTERED]")

print("\n" + "="*60)
print("SUMMARY:")
print("="*60)

if open_ports:
    print("Open ports found:")
    for port, desc in open_ports:
        print(f"  - Port {port}: {desc}")
else:
    print("No open ports found (firewall may be blocking)")

print("\n" + "="*60)
print("RECOMMENDATIONS:")
print("="*60)

if any(p[0] in [993, 143] for p in open_ports):
    print("✓ IMAP is available - can fetch emails directly!")
elif any(p[0] in [995, 110] for p in open_ports):
    print("✓ POP3 is available - can fetch emails!")
elif any(p[0] in [443, 80, 8443, 8080] for p in open_ports):
    print("✓ Only web ports available - need to use webmail scraping")
else:
    print("✗ No email ports accessible - may need VPN or firewall config")
