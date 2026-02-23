# Simhash Project

A lightweight Python tool that compares the textual similarity of two web pages using the **Simhash** algorithm and a custom **Polynomial Rolling Hash**. 

Instead of doing an exact word-for-word comparison, this script generates a 64-bit fingerprint (Simhash) for the body text of each URL. It then compares the two fingerprints at the bit level to determine how many bits they share, giving a fast and space-efficient measure of similarity.

## Features

* **Targeted Web Scraping:** Automatically fetches HTML and extracts text exclusively from the `<body>` tag.
* **Text Normalization:** Converts all text to lowercase and strips out non-alphanumeric characters.
* **Custom Hashing:** Implements a 64-bit polynomial rolling hash for individual words using a specific mathematical formula, without relying on Python's built-in `hash()` function.
* **Interactive CLI:** Prompts the user for URLs dynamically at runtime.
* **Bitwise Comparison:** Uses XOR operations to quickly count differing bits and calculate the total matching bits out of 64.

## Prerequisites & Requirements

This script relies mostly on Python's built-in libraries (`urllib`, `re`, `collections`), but requires **BeautifulSoup4** to parse the HTML document.

* **Python 3.x**
* **beautifulsoup4**

### Installation

You can install the required dependency using pip:

```bash
pip install beautifulsoup4
