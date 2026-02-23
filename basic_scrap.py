import sys
import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin

def fetch_page(url):
    """Fetches the HTML content of the given URL."""
    try:
        # Added headers to simulate a real browser request (prevents some basic blocks)
        headers = {'User-Agent': 'Mozilla/5.0'}
        response = requests.get(url, headers=headers, timeout=10)
        response.raise_for_status() # Raises an error for bad HTTP status codes
        return response.text
    except requests.exceptions.RequestException as e:
        print(f"Error fetching the URL: {e}")
        sys.exit(1)

def extract_and_print_title(soup):
    """Extracts and prints the page title without HTML tags."""
    print("--- Page Title ---")
    if soup.title:
        print(soup.title.get_text(strip=True))
    else:
        print("No Title Found")
    print() # Empty line for readability

def extract_and_print_body(soup):
    """Extracts and prints the page body text without HTML tags."""
    print("--- Page Body ---")
    if soup.body:
        # Using a newline separator ensures block elements don't squash together
        body_text = soup.body.get_text(separator='\n', strip=True)
        print(body_text)
    else:
        print("No Body Found")
    print()

def extract_and_print_links(base_url, soup):
    """Extracts and prints all URLs that the page links to."""
    print("--- Linked URLs ---")
    # Find all 'a' (anchor) tags that have an 'href' attribute
    links = soup.find_all('a', href=True)
    
    if not links:
        print("No Links Found")
        
    for link in links:
        raw_url = link['href']
        # urljoin converts relative URLs (like '/about') to absolute URLs
        full_url = urljoin(base_url, raw_url)
        print(full_url)

def main():
    # 1. Check if the URL was provided as a command-line argument
    if len(sys.argv) < 2:
        print("Usage: python scraper.py <URL>")
        sys.exit(1)
        
    url = sys.argv[1]
    
    # Ensure the URL has a scheme (http/https)
    if not url.startswith(('http://', 'https://')):
        url = 'https://' + url

    # 2. Fetch the HTML
    html_content = fetch_page(url)
    
    # 3. Parse with BeautifulSoup
    soup = BeautifulSoup(html_content, 'html.parser')
    
    # 4. Extract and print the required data using our functions
    extract_and_print_title(soup)
    extract_and_print_body(soup)
    extract_and_print_links(url, soup)

if __name__ == "__main__":
    main()