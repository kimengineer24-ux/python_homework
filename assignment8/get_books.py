# Task 1: Review robots.txt to Ensure Policy Compliance
# I reviewed https://durhamcountylibrary.org/robots.txt before scraping.
# This script scrapes the public Durham County Library search results page responsibly.

# Task 2: Understanding HTML and the DOM for the Durham Library Site
# The assignment asks us to find the li search result elements,
# then find the title, author link(s), and format/year element inside each li.

# Task 3: Write a Program to Extract this Data
# Task 4: Write out the Data

import json
import re
import time
from pathlib import Path

import pandas as pd
from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager


URL = "https://durhamcounty.bibliocommons.com/v2/search?query=learning%20spanish&searchType=smart"

# DOM selectors saved from the search results page.
# These target the li result, title element, author links, and format/year container.
RESULT_LI_SELECTOR = 'li[class*="search-result-item"], li[class*="cp-search-result-item"]'
TITLE_SELECTOR = 'a[class*="title-content-title"], a[class*="title-content"], a[href*="/v2/record/"]'
AUTHOR_LINK_SELECTOR = 'a[class*="author"], a[href*="searchType=author"]'
FORMAT_YEAR_CONTAINER_SELECTOR = 'div[class*="display-info"], div[class*="format"]'
FORMAT_YEAR_SPAN_SELECTOR = "span"


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


def looks_like_format_year(value):
    value = clean_text(value)

    if not value:
        return False

    has_year = re.search(r"(18|19|20)\d{2}", value) is not None
    has_format = re.search(
        r"Book|eBook|Audiobook|DVD|CD|Large Print|Magazine|Video|Kit",
        value,
        re.IGNORECASE
    ) is not None

    return has_year or has_format


driver = create_driver()
results = []

try:
    driver.get(URL)

    wait = WebDriverWait(driver, 20)
    wait.until(EC.presence_of_element_located((By.TAG_NAME, "li")))

    time.sleep(3)

    # Find the li elements that represent search result entries.
    result_items = driver.find_elements(By.CSS_SELECTOR, RESULT_LI_SELECTOR)

    # Backup: still only keeps li elements, but requires a record link inside the li.
    if len(result_items) == 0:
        result_items = driver.find_elements(
            By.XPATH,
            '//li[.//a[contains(@href, "/v2/record/")]]'
        )

    print("Search result li elements found:", len(result_items))

    for item in result_items:
        # Find title from the title element inside the li.
        title_elements = item.find_elements(By.CSS_SELECTOR, TITLE_SELECTOR)

        if len(title_elements) == 0:
            continue

        title = clean_text(title_elements[0].text)

        if not title:
            continue

        # Find author link elements inside the same li.
        author_elements = item.find_elements(By.CSS_SELECTOR, AUTHOR_LINK_SELECTOR)

        authors = []

        for author_element in author_elements:
            author_text = clean_text(author_element.text)
            author_href = author_element.get_attribute("href") or ""
            author_class = author_element.get_attribute("class") or ""

            if not author_text:
                continue

            if author_text == title:
                continue

            if "author" in author_href.lower() or "author" in author_class.lower():
                if author_text not in authors:
                    authors.append(author_text)

        author = "; ".join(authors)

        # Find the format/year container and then the span inside it.
        format_year = ""
        format_containers = item.find_elements(
            By.CSS_SELECTOR,
            FORMAT_YEAR_CONTAINER_SELECTOR
        )

        for container in format_containers:
            span_elements = container.find_elements(
                By.CSS_SELECTOR,
                FORMAT_YEAR_SPAN_SELECTOR
            )

            for span in span_elements:
                span_text = clean_text(span.text)

                if looks_like_format_year(span_text):
                    format_year = span_text
                    break

            if format_year:
                break

            container_text = clean_text(container.text)

            if looks_like_format_year(container_text):
                format_year = container_text
                break

        book = {
            "Title": title,
            "Author": author,
            "Format-Year": format_year
        }

        results.append(book)

    # Remove duplicate titles while keeping the first result.
    unique_results = []
    seen_titles = set()

    for book in results:
        title_key = book["Title"].lower()

        if title_key not in seen_titles:
            unique_results.append(book)
            seen_titles.add(title_key)

    results = unique_results

    df = pd.DataFrame(results)

    print("\nScraped book results:")
    print(df)

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
