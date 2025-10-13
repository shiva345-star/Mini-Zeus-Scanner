import argparse
import sys
import shutil
import subprocess
from urllib.parse import urlparse
from colorama import init, Fore, Style

import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))

from modules.header_checker import check_headers
from modules.whois_lookup import get_whois_info
from modules.port_scanner import scan_ports
from modules.spider import spider
from modules.admin_finder import find_admin_panels
from modules.subdomain_finder import find_subdomains
from modules.xss_scanner import xss_scan
from modules.sql_scanner import sql_scan
from modules.clickjacking_scanner import check_clickjacking
from modules.header_checker import check_headers

# Initialize colorama
init(autoreset=True)

BANNER = fr"""{Fore.LIGHTGREEN_EX}
__          __________                             __
   / /          \____    /____  __ __  ______          \ \
  / /    ______   /     // __ \|  |  \/  ___/  ______   \ \
  \ \   /_____/  /     /\  ___/|  |  /\___ \  /_____/   / /
   \_\          /_______ \___  >____//____  >          /_/
                       \/   \/           \/ v1.0.0 (Spider Edition)
{Style.RESET_ALL}"""

def check_and_install_tool(tool_name, install_instructions):
    if shutil.which(tool_name):
        print(f"{Fore.GREEN}{tool_name} is installed.{Style.RESET_ALL}")
        return True
    else:
        print(f"{Fore.RED}{tool_name} is not installed. Please install it manually.{Style.RESET_ALL}")
        print(f"{Fore.YELLOW}Installation instructions: {install_instructions}{Style.RESET_ALL}")
        return False

def main():
    parser = argparse.ArgumentParser(description='Zeus Scanner - A modular web scanner.')
    parser.add_argument('url', help='The URL to scan.')
    parser.add_argument('--headers', action='store_true', help='Get headers of the URL.')
    parser.add_argument('--whois', action='store_true', help='Get whois info of the URL.')
    parser.add_argument('--ports', action='store_true', help='Scan ports of the URL.')
    parser.add_argument('--spider', action='store_true', help='Spider the URL to find all links.')
    parser.add_argument('--spider-depth', type=int, default=1, help='Depth for spider to crawl (default: 1).')
    parser.add_argument('--spider-max-links', type=int, default=-1, help='Maximum number of links to crawl (default: -1 for no limit).')
    parser.add_argument('--admin-finder', action='store_true', help='Find admin panels.')
    parser.add_argument('--subdomains', action='store_true', help='Find subdomains.')
    parser.add_argument('--xss', action='store_true', help='Scan for XSS vulnerabilities.')
    parser.add_argument('--sql', action='store_true', help='Scan for SQL injection vulnerabilities.')
    parser.add_argument('--clickjacking', action='store_true', help='Scan for clickjacking vulnerability.')
    parser.add_argument('--header-check', action='store_true', help='Perform header checks.')
    parser.add_argument('--sqlmap', action='store_true', help='Run sqlmap on the URL.')
    parser.add_argument('--nmap', action='store_true', help='Run nmap on the URL.')
    parser.add_argument('--no-banner', action='store_true', help='Do not display the banner.')
    args = parser.parse_args()

    if not args.no_banner:
        sys.stdout.write(BANNER.strip() + '\n')
        sys.stdout.flush()

    print(f'{Fore.GREEN}Scanning {args.url}...\n')

    if args.headers:
        print(f'{Fore.YELLOW}--- Headers ---')
        check_headers(args.url)
        print('\n')

    if args.whois:
        print(f'{Fore.YELLOW}--- Whois Info ---')
        whois_info = get_whois_info(args.url)
        print(whois_info)
        print('\n')

    if args.ports:
        print(f'{Fore.YELLOW}--- Port Scan ---')
        port_scan_results = scan_ports(args.url)
        print(port_scan_results)
        print('\n')

    if args.spider:
        print(f'{Fore.YELLOW}--- Spider ---')
        links = spider(args.url, depth=args.spider_depth, max_links=args.spider_max_links)
        if isinstance(links, list):
            print(f'{Fore.GREEN}Found {len(links)} unique links.{Style.RESET_ALL}')
            print('\n')

            # Run sqlmap scan if --sqlmap argument is provided
            if args.sqlmap:
                print(f'{Fore.YELLOW}--- SQLMap Scan ---')
                if check_and_install_tool('sqlmap', 'On Linux: sudo apt-get install sqlmap; On Windows: Download from sqlmap.org'):
                    for link in links:
                        print(f'{Fore.CYAN}Running: sqlmap -u {link}{Style.RESET_ALL}')
                        try:
                            subprocess.run(['sqlmap', '-u', link])
                        except Exception as e:
                            print(f'{Fore.RED}Error running sqlmap on {link}: {e}{Style.RESET_ALL}')
                print('\n')

            # Run nmap scan if --nmap argument is provided
            if args.nmap:
                print(f'{Fore.YELLOW}--- Nmap Scan ---')
                if check_and_install_tool('nmap', 'On Linux: sudo apt-get install nmap; On Windows: Download from nmap.org'):
                    unique_domains = set()
                    for link in links:
                        parsed_link = urlparse(link)
                        if parsed_link.netloc:
                            unique_domains.add(parsed_link.netloc)

                    for domain in unique_domains:
                        print(f'{Fore.CYAN}Running: nmap {domain}{Style.RESET_ALL}')
                        try:
                            subprocess.run(['nmap', domain])
                        except Exception as e:
                            print(f'{Fore.RED}Error running nmap on {domain}: {e}{Style.RESET_ALL}')
                print('\n')

        else:
            print(f'{Fore.RED}{links}')
        print('\n')

    if args.admin_finder:
        print(f'{Fore.YELLOW}--- Admin Panels ---')
        panels = find_admin_panels(args.url)
        if panels:
            for panel in panels:
                print(f'{Fore.GREEN}{panel}')
        else:
            print('No admin panels found.')
        print('\n')

    if args.subdomains:
        print(f'{Fore.YELLOW}--- Subdomains ---')
        domain = urlparse(args.url).netloc
        subdomains = find_subdomains(domain)
        if subdomains:
            for subdomain in subdomains:
                print(f'{Fore.GREEN}{subdomain}')
        else:
            print('No subdomains found.')
        print('\n')

    if args.xss:
        print(f'{Fore.YELLOW}--- XSS Scan ---')
        vulnerable_forms = xss_scan(args.url)
        if vulnerable_forms:
            print(f'{Fore.RED}Vulnerable forms found:')
            for form in vulnerable_forms:
                print(f'{Fore.CYAN}Action: {Style.RESET_ALL}{form[0]}, {Fore.CYAN}Method: {Style.RESET_ALL}{form[1]}, {Fore.CYAN}Payload: {Style.RESET_ALL}{form[2]}')
        else:
            print('No XSS vulnerabilities found.')
        print('\n')

    if args.sql:
        print(f'{Fore.YELLOW}--- SQL Injection Scan ---')
        vulnerable_forms = sql_scan(args.url)
        if vulnerable_forms:
            print(f'{Fore.RED}Vulnerable forms found:')
            for form in vulnerable_forms:
                print(f'{Fore.CYAN}Action: {Style.RESET_ALL}{form[0]}, {Fore.CYAN}Method: {Style.RESET_ALL}{form[1]}, {Fore.CYAN}Payload: {Style.RESET_ALL}{form[2]}')
        else:
            print('No SQL injection vulnerabilities found.')
        print('\n')

    if args.clickjacking:
        print(f'{Fore.YELLOW}--- Clickjacking Scan ---')
        check_clickjacking(args.url)
        print('\n')

    if args.header_check:
        check_headers(args.url)

    if args.sqlmap:
        print(f'{Fore.YELLOW}--- SQLMap Scan ---')
        if check_and_install_tool('sqlmap', 'On Linux: sudo apt-get install sqlmap; On Windows: Download from sqlmap.org'):
            print(f'{Fore.CYAN}Running: sqlmap -u {args.url}{Style.RESET_ALL}')
            try:
                subprocess.run(['sqlmap', '-u', args.url])
            except Exception as e:
                print(f'{Fore.RED}Error running sqlmap: {e}{Style.RESET_ALL}')
        print('\n')

    if args.nmap:
        print(f'{Fore.YELLOW}--- Nmap Scan ---')
        if check_and_install_tool('nmap', 'On Linux: sudo apt-get install nmap; On Windows: Download from nmap.org'):
            parsed_url = urlparse(args.url)
            target_host = parsed_url.netloc
            if target_host:
                print(f'{Fore.CYAN}Running: nmap {target_host}{Style.RESET_ALL}')
                try:
                    subprocess.run(['nmap', target_host])
                except Exception as e:
                    print(f'{Fore.RED}Error running nmap on {domain}: {e}{Style.RESET_ALL}')
            else:
                print(f'{Fore.RED}Could not extract host from URL for Nmap scan.{Style.RESET_ALL}')
        print('\n')

if __name__ == '__main__':
    main()