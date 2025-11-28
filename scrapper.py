from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
import time
import pandas as pd


def scrape_autovit_debug():
    """
    Debug version with visible browser
    """

    # Setup Chrome options for debugging (visible browser)
    chrome_options = Options()
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
    chrome_options.add_argument("--window-size=1920,1080")
    # Remove headless to see what's happening

    driver = webdriver.Chrome(options=chrome_options)
    car_links = []

    try:
        print("Opening browser - watch what happens...")
        driver.get("https://www.autovit.ro/autoturisme/aixam")

        input("Press Enter after the page loads completely...")

        # Get all links on the page
        all_links = driver.find_elements(By.TAG_NAME, "a")
        print(f"Found {len(all_links)} total links on page")

        # Filter for car listing links
        for link in all_links:
            href = link.get_attribute("href")
            if href and "/anunt/" in href and "aixam" in href.lower():
                if href not in car_links:
                    car_links.append(href)
                    print(f"Found: {href}")

        print(f"\nTotal unique car links: {len(car_links)}")

    except Exception as e:
        print(f"Error: {e}")
    finally:
        driver.quit()

    return car_links


# Quick test version
if __name__ == "__main__":
    print("=== Debug Version - Visible Browser ===")
    links = scrape_autovit_debug()

    if links:
        df = pd.DataFrame({"links": links})
        df.to_csv("autovit_debug_links.csv", index=False)
        print(f"Saved {len(links)} links to autovit_debug_links.csv")