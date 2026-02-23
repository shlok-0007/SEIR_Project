import re
import urllib.request
from collections import Counter
from bs4 import BeautifulSoup

def fetch_body_text(url):
    req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
    html = urllib.request.urlopen(req).read()
    soup = BeautifulSoup(html, 'html.parser')
    
    if not soup.body:
        return ""
        
    return soup.body.get_text(separator=' ', strip=True).lower()

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
        hash_value = (hash_value + ord(char) * (p ** i)) % m
        
    return hash_value

def get_simhash(text):
 
    freqs = Counter(re.findall(r'[a-z0-9]+', text))
    
    v = [0] * 64
    for word, count in freqs.items():
        h = polynomial_rolling_hash(word)
        for i in range(64):
           
            if (h >> i) & 1:
                v[i] += count
            else:
                v[i] -= count
            
    # Reconstruct the final 64-bit hash using bitwise OR logic
    simhash = 0
    for i in range(64):
        if v[i] > 0:
            simhash |= (1 << i)
            
    return simhash

def main():
    # 1. Take two URLs via interactive input
    print("--- Simhash---")
    url1 = input("Enter the first URL (e.g., https://example.com): ").strip()
    url2 = input("Enter the second URL (e.g., https://example.com): ").strip()

    if not url1 or not url2:
        print("Error: Both URLs are required to run the comparison.")
        return
        
    print("\nFetching and processing URLs... please wait.")

    # 2. Scrape the body text
    text1 = fetch_body_text(url1)
    text2 = fetch_body_text(url2)

    # 3. Compute Simhashes
    hash1 = get_simhash(text1)
    hash2 = get_simhash(text2)
    
    # 4. Compare common bits (XOR gives differing bits, subtract from 64)
    common_bits = 64 - bin(hash1 ^ hash2).count('1')

    # Print how many bits are common as required
    print(f"\nNumber of common bits: {common_bits}/64")

if __name__ == "__main__":
    main()
