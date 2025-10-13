import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin, urlparse
import warnings
import time
from colorama import Fore, Style

def spider(url, depth=1, max_links=50):
    """Crawls a website and returns all found links up to a specified depth."""
    visited_links = set()
    links_to_visit = [(url, 10)]  # (link, current_depth)
    all_found_links = set()

    while links_to_visit and (max_links == -1 or len(all_found_links) < max_links):
        current_url, current_depth = links_to_visit.pop(0)

        if current_url in visited_links or current_depth > depth:
            continue

        visited_links.add(current_url)
        all_found_links.add(current_url)

        print(f"{Fore.BLUE}Crawling: {current_url} (Depth: {current_depth}){Style.RESET_ALL}")

        try:
            with warnings.catch_warnings():
                warnings.simplefilter("ignore")
                response = requests.get(current_url, verify=False, timeout=5)
            soup = BeautifulSoup(response.content, 'html.parser')

            for a_tag in soup.find_all('a', href=True):
                link = a_tag['href']
                full_link = urljoin(current_url, link)
                parsed_root_url = urlparse(url)
                parsed_full_link = urlparse(full_link)

                if parsed_root_url.netloc == parsed_full_link.netloc and full_link not in visited_links:
                    if len(all_found_links) < max_links:
                        links_to_visit.append((full_link, current_depth + 1))
                    else:
                        break
            time.sleep(0.3)  # Add delay here

        except requests.exceptions.RequestException as e:
            print(f"{Fore.RED}Error crawling {current_url}: {e}{Style.RESET_ALL}")
        except Exception as e:
            print(f"{Fore.RED}An unexpected error occurred while crawling {current_url}: {e}{Style.RESET_ALL}")

    return list(all_found_links)