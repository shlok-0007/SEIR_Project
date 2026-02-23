# Webpage Simhash Comparator 🕸️🔍

A powerful Python tool designed to measure the textual and structural similarity between any two webpages. Unlike standard scrapers, this tool handles modern, JavaScript-heavy websites by rendering them in a headless browser before extracting and comparing their contents using a **64-bit Simhash** algorithm.

## 📖 Overview

When comparing documents, standard cryptographic hashes (like SHA-256) change completely if even a single character is modified. **Simhash**, on the other hand, is a *Locality-Sensitive Hash (LSH)*. It generates similar hashes for similar documents, allowing us to calculate exactly how closely related two webpages are by comparing their bits.

This project was built to accurately quantify webpage similarities by utilizing:
* **Playwright:** For rendering dynamic, client-side JavaScript content.
* **BeautifulSoup:** For precise HTML parsing and text extraction.
* **Polynomial Rolling Hash:** For generating unique identifiers for individual words.
* **Simhash:** For aggregating word frequencies into a final 64-bit document fingerprint.

---

## ⚙️ Under the Hood

The comparison process runs through four main stages:

1. **JavaScript Rendering & Text Extraction:** The script launches a headless Chromium browser to fully load the target URLs. It extracts the `<body>` HTML, converts all text to lowercase, and uses Regular Expressions to isolate pure alphanumeric words.
2. **Word Hashing:** Every unique word is hashed into a 64-bit integer using a custom polynomial rolling hash function:
   
   $$hash(s) = \sum_{i=0}^{n-1} s[i] \cdot p^i \pmod m$$
   
   *(Where $p = 53$, $m = 2^{64}$, and $s[i]$ is the ASCII value of the character).*
3. **Simhash Vector Generation:** A 64-element vector is created. The algorithm iterates through the 64-bit hash of every word. If a bit is `1`, the word's frequency is *added* to that vector position. If it is `0`, the frequency is *subtracted*. Positive vector positions become `1`s and negative positions become `0`s to form the final document hash.
4. **Bitwise Comparison:** The two final 64-bit document hashes are compared using an `XOR` (`^`) bitwise operator. The number of identical bits dictates the similarity score.

---

## 🚀 Installation & Setup

### Prerequisites
You will need **Python 3.7+** installed on your machine.

### 1. Clone the repository
```bash
git clone [https://github.com/yourusername/main_hash_project.git](https://github.com/yourusername/main_hash_project.git)
cd main_hash_project
