
import requests

def check_clickjacking(url):
    try:
        response = requests.get(url)
        headers = response.headers
        if "X-Frame-Options" in headers:
            print(f"URL: {url}")
            print(f"X-Frame-Options header is present: {headers['X-Frame-Options']}")
            return True
        else:
            print(f"URL: {url}")
            print("X-Frame-Options header is not present. This website is vulnerable to clickjacking.")
            return False
    except requests.exceptions.RequestException as e:
        print(f"An error occurred: {e}")
        return False

if __name__ == "__main__":
    target_url = "http://www.google.com"
    check_clickjacking(target_url)
