import requests
from colorama import Fore, Style

def check_headers(url):
    print(f'{Fore.YELLOW}--- Header Check ---')
    try:
        response = requests.get(url, timeout=10)
        headers = response.headers

        print(f'{Fore.GREEN}Headers for {url}:')
        for key, value in headers.items():
            print(f'{Fore.CYAN}{key}: {Style.RESET_ALL}{value}')

    except requests.exceptions.RequestException as e:
        print(f'{Fore.RED}Error during header check: {e}')
    except Exception as e:
        print(f'{Fore.RED}An unexpected error occurred: {e}')
    print()