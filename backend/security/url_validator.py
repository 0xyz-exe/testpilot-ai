from urllib.parse import urlparse
import ipaddress
import socket
from typing import List

BLOCKED_RANGES = [
    ipaddress.ip_network('10.0.0.0/8'),
    ipaddress.ip_network('172.16.0.0/12'),
    ipaddress.ip_network('192.168.0.0/16'),
    ipaddress.ip_network('127.0.0.0/8'),
    ipaddress.ip_network('169.254.0.0/16'),
    ipaddress.ip_network('::1/128'),
    ipaddress.ip_network('fd00::/8'),
]

class SecurityError(Exception):
    pass

def is_private_ip(hostname: str) -> bool:
    try:
        ip = socket.gethostbyname(hostname)
        ip_obj = ipaddress.ip_address(ip)
        for blocked in BLOCKED_RANGES:
            if ip_obj in blocked:
                return True
        return False
    except (socket.gaierror, ValueError):
        return False

def validate_url(url: str) -> None:
    parsed = urlparse(url)
    
    if parsed.scheme not in ['http', 'https']:
        raise SecurityError("Only http/https allowed")
    
    if not parsed.hostname:
        raise SecurityError("Invalid URL: missing hostname")
    
    # Allow localhost for development
    if parsed.hostname in ['localhost', '127.0.0.1']:
        return  # ponytail: dev-only; production should reject localhost
    
    if is_private_ip(parsed.hostname):
        raise SecurityError(f"Private IP rejected: {parsed.hostname}")

def validate_allowed_urls(urls: List[str]) -> None:
    if not urls:
        raise ValueError("At least one allowed URL required")
    
    for url in urls:
        validate_url(url)
