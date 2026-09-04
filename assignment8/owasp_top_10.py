# Task 6: Scraping Structured Data
# This script uses Selenium and XPath to scrape the OWASP Top 10 vulnerability titles and links.
# It starts from the exact page in the assignment: https://owasp.org/www-project-top-ten/

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
    driver.get(PROJECT_URL)

    wait = WebDriverWait(driver, 15)
    wait.until(EC.presence_of_element_located((By.TAG_NAME, "body")))

    time.sleep(2)

    print("Starting page used:")
    print(PROJECT_URL)

    # Find the current OWASP Top Ten release link from the exact assignment page.
    current_release_link = driver.find_element(
        By.XPATH,
        '//a[contains(@href, "/Top10/") and contains(normalize-space(.), "OWASP Top Ten")]'
    )

    current_release_url = current_release_link.get_attribute("href")

    print("\nCurrent OWASP Top Ten release page found:")
    print(current_release_url)

    driver.get(current_release_url)

    wait.until(EC.presence_of_element_located((By.TAG_NAME, "body")))

    time.sleep(2)

    # Find the Top 10 list heading, then use XPath to get the ordered list links after it.
    top10_heading = driver.find_element(
        By.XPATH,
        '//*[contains(normalize-space(.), "Top 10:2025 List")]'
    )

    risk_links = top10_heading.find_elements(
        By.XPATH,
        './following::ol[1]/li/a'
    )

    for link in risk_links:
        title = " ".join(link.text.split()).strip()
        href = link.get_attribute("href")

        if title and href:
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
