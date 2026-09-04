# Task 6: Scraping Structured Data
# This script uses Selenium and XPath to scrape OWASP Top 10 vulnerability titles and links.
# It saves the results to owasp_top_10.csv.

import time
from pathlib import Path

import pandas as pd
from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager


PROJECT_URL = "https://owasp.org/www-project-top-ten/"
TOP10_URL = "https://owasp.org/Top10/2025/"


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


driver = create_driver()
owasp_results = []

try:
    # Read the OWASP project page first.
    driver.get(PROJECT_URL)

    wait = WebDriverWait(driver, 15)
    wait.until(EC.presence_of_element_located((By.TAG_NAME, "body")))

    time.sleep(2)

    # Then read the current OWASP Top 10 list page.
    driver.get(TOP10_URL)

    wait.until(EC.presence_of_element_located((By.TAG_NAME, "body")))

    time.sleep(2)

    # Use XPath to find links that contain A01 through A10.
    risk_links = driver.find_elements(
        By.XPATH,
        '//a[contains(normalize-space(.), "A01:2025") or '
        'contains(normalize-space(.), "A02:2025") or '
        'contains(normalize-space(.), "A03:2025") or '
        'contains(normalize-space(.), "A04:2025") or '
        'contains(normalize-space(.), "A05:2025") or '
        'contains(normalize-space(.), "A06:2025") or '
        'contains(normalize-space(.), "A07:2025") or '
        'contains(normalize-space(.), "A08:2025") or '
        'contains(normalize-space(.), "A09:2025") or '
        'contains(normalize-space(.), "A10:2025")]'
    )

    seen_titles = set()

    for link in risk_links:
        title = " ".join(link.text.split()).strip()
        href = link.get_attribute("href")

        if not title or not href:
            continue

        if title in seen_titles:
            continue

        seen_titles.add(title)

        owasp_results.append({
            "Title": title,
            "Link": href
        })

        if len(owasp_results) == 10:
            break

    print("\nOWASP Top 10 Results:")
    print(owasp_results)

    df = pd.DataFrame(owasp_results)

    print("\nOWASP Top 10 DataFrame:")
    print(df)

    output_file = Path(__file__).parent / "owasp_top_10.csv"

    df.to_csv(output_file, index=False)

    print("\nCSV file created:")
    print(output_file)

finally:
    driver.quit()
