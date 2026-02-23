from bs4 import BeautifulSoup
from urllib.parse import urljoin
from playwright.sync_api import sync_playwright

def get_url():
    """Gets the URL from the user and ensures it has http/https."""
    url = input("Enter URL to scrape: ").strip()
    if not url.startswith('http'):
        url = 'https://' + url
    return url

def fetch_rendered_html(url):
    """Uses Playwright to render JavaScript and returns a BeautifulSoup object."""
    print("Loading page... (please wait)")
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()
        page.goto(url, wait_until="networkidle") # Waits for JS to finish loading
        soup = BeautifulSoup(page.content(), 'html.parser')
        browser.close()
        return soup

def print_extracted_data(soup, base_url):
    """Extracts and prints the title, body, and links."""
    print("\n--- TITLE ---")
    print(soup.title.text.strip() if soup.title else "No Title Found")

    print("\n--- BODY ---")
    print(soup.body.get_text(separator='\n', strip=True) if soup.body else "No Body Found")

    print("\n--- LINKS ---")
    for a_tag in soup.find_all('a', href=True):
        print(urljoin(base_url, a_tag['href']))

def main():
    # 1. Get the URL
    url = get_url()
    
    # 2. Fetch the parsed HTML
    soup = fetch_rendered_html(url)
    
    # 3. Extract and print
    print_extracted_data(soup, url)

if __name__ == "__main__":
    main()