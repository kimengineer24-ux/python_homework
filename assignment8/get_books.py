# Task 1: Review robots.txt to Ensure Policy Compliance
# I reviewed https://durhamcountylibrary.org/robots.txt before scraping.
# This script scrapes the public Durham County Library search results page slowly and responsibly.

# Task 2: Understanding HTML and the DOM
# The search results are stored inside li elements.
# This script searches li elements and then looks inside each result for title, author, and format/year data.

# Task 3: Write a Program to Extract this Data

import json
import re
import time
from pathlib import Path

import pandas as pd
from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager


URL = "https://durhamcounty.bibliocommons.com/v2/search?query=learning%20spanish&searchType=smart"


def create_driver():
    options = webdriver.ChromeOptions()
    options.add_argument("--headless=new")
    options.add_argument("--window-size=1920,1080")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")

    driver = webdriver.Chrome(
        service=ChromeService(ChromeDriverManager().install()),
        options=options
    )
    return driver


def clean_text(value):
    return " ".join(value.split()).strip()


def get_format_year(text):
    pattern = r"(Book|eBook|Audiobook|DVD|Music CD|Streaming Video|Magazine|Large Print|Kit).*?(19|20)\d{2}"
    match = re.search(pattern, text, re.IGNORECASE)

    if match:
        return clean_text(match.group(0))

    lines = text.split("\n")
    for line in lines:
        if re.search(r"(19|20)\d{2}", line):
            return clean_text(line)

    return ""


driver = create_driver()
results = []

try:
    driver.get(URL)
    time.sleep(5)

    # Find all li elements and keep only the ones that look like book search results.
    li_entries = driver.find_elements(By.TAG_NAME, "li")
    print("Total li elements found:", len(li_entries))

    for entry in li_entries:
        entry_text = entry.text.strip()

        if not entry_text:
            continue

        record_links = entry.find_elements(By.CSS_SELECTOR, 'a[href*="/v2/record/"]')

        if len(record_links) == 0:
            continue

        title = clean_text(record_links[0].text)

        if not title:
            continue

        # Find author links. Some books may have multiple authors.
        author_links = entry.find_elements(
            By.CSS_SELECTOR,
            'a[href*="author"], a[href*="contributors"], a[href*="creator"]'
        )

        authors = []

        for author_link in author_links:
            author_name = clean_text(author_link.text)
            if author_name and author_name.lower() != title.lower():
                authors.append(author_name)

        # Backup author search from visible text if author links are not found.
        if len(authors) == 0:
            for line in entry_text.split("\n"):
                line = clean_text(line)
                if line.lower().startswith("by "):
                    authors.append(line.replace("by ", "", 1).strip())

        author = "; ".join(authors)

        format_year = get_format_year(entry_text)

        book = {
            "Title": title,
            "Author": author,
            "Format-Year": format_year
        }

        results.append(book)

    # Remove duplicate results.
    unique_results = []
    seen_titles = set()

    for item in results:
        title_key = item["Title"].lower()

        if title_key not in seen_titles:
            unique_results.append(item)
            seen_titles.add(title_key)

    results = unique_results

    df = pd.DataFrame(results)

    print("\nScraped book results:")
    print(df)

    # Task 4: Write out the Data
    output_folder = Path(__file__).parent

    csv_file = output_folder / "get_books.csv"
    json_file = output_folder / "get_books.json"

    df.to_csv(csv_file, index=False)

    with open(json_file, "w", encoding="utf-8") as file:
        json.dump(results, file, indent=4)

    print("\nFiles created:")
    print(csv_file)
    print(json_file)

finally:
    driver.quit()
