import whois
from urllib.parse import urlparse

def get_whois_info(url):
    """Performs a whois lookup on the domain of the given URL."""
    try:
        domain = urlparse(url).netloc
        whois_info = whois.whois(domain)
        return whois_info
    except Exception as e:
        return str(e)