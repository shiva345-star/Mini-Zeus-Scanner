import requests
import os
import importlib.util
from colorama import Fore, Style

def detect_wafs(url):
    print(f'{Fore.YELLOW}--- WAF Detection ---')
    project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')) # This is C:/Users/mahav/Zeus-Scanner/
    try:
        import sys
        if project_root not in sys.path:
            sys.path.insert(0, project_root)

        response = requests.get(url, timeout=10)
        content = response.text
        headers = response.headers
        status = response.status_code

        detected_wafs = []
        firewall_modules_path = os.path.join(project_root, 'lib', 'firewall')
        
        if not os.path.exists(firewall_modules_path):
            print(f'{Fore.RED}Error: Firewall modules directory not found at {firewall_modules_path}')
            return

        for filename in os.listdir(firewall_modules_path):
            if filename.endswith('.py') and not filename.startswith('__'):
                module_name = filename[:-3]
                module_path = os.path.join(firewall_modules_path, filename)
                
                spec = importlib.util.spec_from_file_location(f"lib.firewall.{module_name}", module_path)
                if spec and spec.loader:
                    waf_module = importlib.util.module_from_spec(spec)
                    spec.loader.exec_module(waf_module)

                    if hasattr(waf_module, 'detect') and hasattr(waf_module, '__item__'):
                        if waf_module.detect(content, headers=headers, status=status):
                            detected_wafs.append(waf_module.__item__)
                
        if detected_wafs:
            print(f'{Fore.GREEN}Detected WAFs:')
            for waf in detected_wafs:
                print(f'- {waf}')
        else:
            print(f'{Fore.CYAN}No known WAF detected.')
    except requests.exceptions.RequestException as e:
        print(f'{Fore.RED}Error during WAF detection: {e}')
    finally:
        if project_root in sys.path:
            sys.path.remove(project_root)
        print()