import requests
from urllib.parse import urljoin
import warnings

ADMIN_PANELS = [
    'admin/',
    'administrator/',
    'admin/login.php',
    'wp-admin/',
    'admin.aspx',
    'adminlogin.aspx',
    'login/',
    'cpanel',
    'webadmin',
    'admin/account.php',
    'admin/index.php',
    'admin/admin.php',
    'admin_area/',
    'admin_area/login.php',
    'admin_area/admin.php',
    'panel-administracion/',
    'memberadmin/',
    'administratorlogin/',
    'adm/',
    'bb-admin/',
    'siteadmin/login.php',
    'siteadmin/index.php',
    'adm_auth',
    'admin1',
    'admin2',
    'admin/account',
    'admin/controlpanel',
    'admin/cp',
    'admincp/login',
    'admin/home',
    'administr8',
    'administration',
    'administrator/account',
    'administrator/login',
    'adminitem',
    'adminitems',
    'adminpanel',
    'admins',
    'auth',
    'authadmin',
    'authenticate',
    'authentication',
    'authuser',
    'autologin',
    'blog/wp-login',
    'check',
    'checkadmin',
]

def find_admin_panels(url):
    """Finds common admin panels on a website."""
    found_panels = []
    for panel in ADMIN_PANELS:
        panel_url = urljoin(url, panel)
        try:
            with warnings.catch_warnings():
                warnings.simplefilter("ignore")
                response = requests.get(panel_url, verify=False)
            if response.status_code == 200:
                found_panels.append(panel_url)
        except requests.exceptions.RequestException:
            pass
    return found_panels