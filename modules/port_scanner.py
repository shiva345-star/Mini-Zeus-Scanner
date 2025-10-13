import nmap
import socket
from urllib.parse import urlparse

def scan_ports(url):
    """Performs a port scan on the domain of the given URL."""
    try:
        domain = urlparse(url).netloc
        ip_address = socket.gethostbyname(domain)
        nm = nmap.PortScanner()
        nm.scan(ip_address, '21-443')
        return nm.csv()
    except (socket.gaierror, nmap.PortScannerError) as e:
        return str(e)