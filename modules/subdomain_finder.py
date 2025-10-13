import requests

SUBDOMAINS = [
    'www',
    'mail',
    'ftp',
    'localhost',
    'webmail',
    'smtp',
    'pop',
    'ns1',
    'ns2',
    'admin',
    'autodiscover',
    'blog',
    'cpanel',
    'dev',
    'developer',
    'docs',
    'forum',
    'git',
    'gitlab',
    'imap',
    'm',
    'mobile',
    'news',
    'pop3',
    'portal',
    'shop',
    'sql',
    'ssh',
    'staging',
    'status',
    'support',
    'test',
    'testing',
    'webdisk',
    'wiki',
]

def find_subdomains(domain):
    """Finds common subdomains for a given domain."""
    found_subdomains = []
    for subdomain in SUBDOMAINS:
        subdomain_url = f'http://{subdomain}.{domain}'
        try:
            requests.get(subdomain_url, timeout=1)
            found_subdomains.append(subdomain_url)
        except requests.exceptions.RequestException:
            pass
    return found_subdomains