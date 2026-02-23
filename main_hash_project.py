import re
from collections import Counter
from bs4 import BeautifulSoup
from playwright.sync_api import sync_playwright

def fetch_rendered_html(url):
    """Uses Playwright to render JavaScript and returns a BeautifulSoup object."""
    print(f"Loading page: {url}... (please wait)")
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()
        # Set a generous timeout in case the page is slow
        page.goto(url, wait_until="networkidle", timeout=60000) 
        soup = BeautifulSoup(page.content(), 'html.parser')
        browser.close()
        return soup

def get_word_frequencies(soup):
    """
    Extracts text from the body, converts to lowercase, 
    keeps only alphanumeric sequences, and counts frequencies.
    """
    if not soup.body:
        return Counter()
    
    # Get all text in the body, separated by spaces
    text = soup.body.get_text(separator=' ', strip=True)
    
    # Convert to lowercase
    text = text.lower()
    
    # Use regex to find sequences of alphanumeric characters
    words = re.findall(r'[a-z0-9]+', text)
    
    # Return a frequency dictionary (Counter)
    return Counter(words)

def polynomial_rolling_hash(word):
    """
    Computes a 64-bit hash for a word using the polynomial rolling hash function:
    hash(s) = sum(s[i] * p^i) mod m
    where p = 53 and m = 2^64.
    """
    p = 53
    m = 2**64
    hash_value = 0
    
    for i, char in enumerate(word):
        # ord(char) gets the ASCII value of the character
        hash_value = (hash_value + ord(char) * (p ** i)) % m
        
    return hash_value

def compute_simhash(word_frequencies):
    """
    Computes a 64-bit Simhash for a document based on word frequencies.
    """
    # Initialize a 64-element list/vector with zeros
    v = [0] * 64
    
    for word, weight in word_frequencies.items():
        word_hash = polynomial_rolling_hash(word)
        
        # Iterate through all 64 bits of the hash
        for i in range(64):
            # Check if the i-th bit of the hash is 1 or 0
            bit_is_set = (word_hash >> i) & 1
            
            if bit_is_set:
                v[i] += weight
            else:
                v[i] -= weight
                
    # Reconstruct the final 64-bit simhash
    simhash = 0
    for i in range(64):
        if v[i] > 0:
            simhash |= (1 << i) # Set the i-th bit to 1
            
    return simhash

def count_common_bits(hash1, hash2):
    """
    Compares two 64-bit hashes and returns the number of identical bits.
    """
    # XOR (^) gives 1 for differing bits, 0 for matching bits
    xor_result = hash1 ^ hash2
    
    # Count the number of differing bits
    differing_bits = bin(xor_result).count('1')
    
    # The common bits are the total bits minus the differing bits
    return 64 - differing_bits

def main():
    # 1. Ask the user for inputs interactively
    print("--- Simhash URL Comparator ---")
    url1 = input("Enter the first URL: ").strip()
    url2 = input("Enter the second URL: ").strip()
    
    if not url1 or not url2:
        print("Error: Both URLs must be provided to run the comparison.")
        return
    
    if not url1.startswith('http'): url1 = 'https://' + url1
    if not url2.startswith('http'): url2 = 'https://' + url2

    # 2. Process first URL
    soup1 = fetch_rendered_html(url1)
    freq1 = get_word_frequencies(soup1)
    simhash1 = compute_simhash(freq1)
    
    # 3. Process second URL
    soup2 = fetch_rendered_html(url2)
    freq2 = get_word_frequencies(soup2)
    simhash2 = compute_simhash(freq2)
    
    # 4. Compare and print results
    common_bits = count_common_bits(simhash1, simhash2)
    
    print("\n--- Results ---")
    # Print the hashes in 64-bit binary format so you can see them visually
    print(f"Simhash 1: {simhash1:064b}")
    print(f"Simhash 2: {simhash2:064b}")
    print(f"\nNumber of common bits: {common_bits}/64")

if __name__ == "__main__":
    main()
