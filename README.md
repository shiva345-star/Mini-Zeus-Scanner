# Gemini Scanner

Gemini Scanner is a modular web security scanner designed to help identify various vulnerabilities and gather information about target websites. It's built with Python and offers a range of scanning capabilities, from basic information gathering to more advanced vulnerability checks.

## Features

*   **Header Check:** Retrieve HTTP headers of a given URL.
*   **WHOIS Lookup:** Get WHOIS information for a domain.
*   **Port Scan:** Scan common ports of the target host.
*   **Spider:** Crawl a website to discover all accessible links within the same domain.
*   **Admin Panel Finder:** Attempt to locate common admin panel login pages.
*   **Subdomain Finder:** Discover subdomains associated with a given domain.
*   **XSS Scanner:** Scan for Cross-Site Scripting (XSS) vulnerabilities.
*   **SQL Injection Scanner:** Scan for SQL Injection vulnerabilities.
*   **Integrated SQLMap:** Optionally run `sqlmap` on URLs discovered by the spider (requires `sqlmap` to be installed).
*   **Integrated Nmap:** Optionally run `nmap` on unique domains discovered by the spider (requires `nmap` to be installed).

## Installation

### Prerequisites

*   Python 3.x
*   `pip` (Python package installer)

### Steps

1.  **Clone the repository:**
    ```bash
    git clone https://github.com/your-username/gemini-scanner.git
    cd gemini-scanner
    ```
    *(Replace `your-username` with your actual GitHub username or the repository owner's username)*

2.  **Install Python dependencies:**
    ```bash
    pip install -r requirements.txt
    ```

3.  **Install external tools (Optional, but recommended for full functionality):**
    *   **SQLMap:**
        *   **Linux:** `sudo apt-get install sqlmap` (Debian/Ubuntu) or equivalent for your distribution.
        *   **Windows:** Download from the official website: [sqlmap.org](https://sqlmap.org/)
    *   **Nmap:**
        *   **Linux:** `sudo apt-get install nmap` (Debian/Ubuntu) or equivalent for your distribution.
        *   **Windows:** Download from the official website: [nmap.org](https://nmap.org/download.html)

## Usage

Run the scanner from your terminal:

```bash
python main.py <URL> [OPTIONS]
```

**Example:** `python main.py https://example.com --spider`

### Options:

*   `<URL>`: The target URL to scan (e.g., `https://example.com`).

*   `--headers`: Get HTTP headers of the URL.
    ```bash
    python main.py https://example.com --headers
    ```

*   `--whois`: Get WHOIS information of the URL.
    ```bash
    python main.py https://example.com --whois
    ```

*   `--ports`: Scan common ports of the URL's host.
    ```bash
    python main.py https://example.com --ports
    ```

*   `--spider`: Crawl the URL to find all links within the same domain. After crawling, you will be prompted to optionally run `sqlmap` and `nmap` on the discovered URLs/domains.
    ```bash
    python main.py https://example.com --spider
    ```

*   `--admin-finder`: Find common admin panel paths.
    ```bash
    python main.py https://example.com --admin-finder
    ```

*   `--subdomains`: Find subdomains for the given URL's domain.
    ```bash
    python main.py https://example.com --subdomains
    ```

*   `--xss`: Scan for XSS vulnerabilities.
    ```bash
    python main.py https://example.com --xss
    ```

*   `--sql`: Scan for SQL injection vulnerabilities.
    ```bash
    python main.py https://example.com --sql
    ```

*   `--no-banner`: Do not display the ASCII art banner at startup.
    ```bash
    python main.py https://example.com --no-banner
    ```

## Contributing

Feel free to fork the repository, open issues, and submit pull requests.

## License

This project is open-source and available under the [MIT License](LICENSE).
