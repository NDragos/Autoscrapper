from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import pandas as pd
import csv
import math

import conversion
import os

def init_driver():
    chrome_options = Options()
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
    chrome_options.add_argument("--window-size=1920,1080")
    return webdriver.Chrome(options=chrome_options)

def get_safely_data(driver, path):
    try:
        html_content = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, path)))
        return html_content.get_attribute("textContent")
    except:
        return "N/A"


def get_links_on_page(driver, make, model, page):
    car_links = []

    try:
        print(f"Navigating to page {page}...")
        driver.get("https://www.autovit.ro/autoturisme/" + make + "/" + model + "?page=" + page)

        # input("Press Enter after the page loads completely...")

        # Get all links on the page
        all_links = driver.find_elements(By.TAG_NAME, "a")
        # print(f"Found {len(all_links)} total links on page")

        # Filter for car listing links
        for link in all_links:
            href = link.get_attribute("href")
            if href and "/anunt/" in href and make in href.lower():
                if href not in car_links:
                    car_links.append(href)
                    # print(f"Found: {href}")

        # print(f"\nTotal unique car links on page {page}: {len(car_links)}")

    except Exception as e:
        print(f"Error on page {page}: {e}")
    
    return car_links

def get_links(driver, make, model):
    try:
        driver.get("https://www.autovit.ro/autoturisme/" + make + "/" + model)
        number_ads = get_safely_data(driver, "//div/p/b")
    except Exception as e:
        print(f"Error getting count: {e}")
        return []

    # Don't quit driver here, we need it!
    
    time.sleep(1)
    if number_ads == "N/A":
        print("Could not find number of ads, defaulting to 1 page.")
        number_pages = 1
    else:
        number_ads = conversion.str_to_int(number_ads)
        number_pages = math.floor(number_ads / 32) + 1 #32 is the number of ads per page 
    
    print(f"Found {number_ads} ads, scraping {number_pages} pages...")
    
    page = 1
    all_links = []
    while page <= number_pages:
        all_links += get_links_on_page(driver, make, model, str(page))
        page += 1
        time.sleep(1)
    
    return all_links

def scrape_car_data(driver, link):
    CAR = {
        "Marca": "N/A",
        "Model": "N/A",
        "An fabricație": "N/A",
        "Preț": "N/A",
        "Km": "N/A",
        "Combustibil": "N/A",
        "Tip Cutie de viteze": "N/A",
        "Tip Caroserie": "N/A",
        "Capacitate Cilindrică": "N/A",
        "Putere": "N/A",
        "Link": "N/A",
    }

    try:
        driver.get(link)

        CAR["Marca"] = get_safely_data(driver, "//div[@data-testid='make']/div[1]/p")

        CAR["Model"] = get_safely_data(driver, "//div[@data-testid='model']/div[1]/p")

        CAR["An fabricație"] = get_safely_data(driver, "//div[@data-testid='year']/div[1]/p")

        CAR["Preț"] = get_safely_data(driver, "//h3/span[1]")
        CAR["Preț"] = conversion.str_to_float(CAR["Preț"])

        CAR["Km"] = get_safely_data(driver, "//div[@data-testid='mileage']/div[1]/p")
        CAR["Km"] = conversion.str_to_float(CAR["Km"])

        CAR["Combustibil"] = get_safely_data(driver, "//div[@data-testid='fuel_type']/div[1]/p")

        CAR["Tip Cutie de viteze"] = get_safely_data(driver, "//div[@data-testid='gearbox']/div[1]/p")
        
        CAR["Tip Caroserie"] = get_safely_data(driver, "//div[@data-testid='body_type']/div[1]/p")

        if CAR["Combustibil"] != "Electric":
            CAR["Capacitate Cilindrică"] = get_safely_data(driver, "//div[@data-testid='engine_capacity']/div[1]/p")
            CAR["Capacitate Cilindrică"] = conversion.delete_let(CAR["Capacitate Cilindrică"])
            CAR["Capacitate Cilindrică"] = CAR["Capacitate Cilindrică"][:-1]


        CAR["Putere"] = get_safely_data(driver, "//div[@data-testid='engine_power']/div[1]/p")
        CAR["Putere"] = conversion.str_to_float(CAR["Putere"])
        
        CAR["Link"] = link
    except Exception as e:
        print(f"Error: {e}")
        return None

    finally:
        driver.quit()
        return CAR

def scrape_autovit(make, model):
    data_list = [ ]
    data_csv = make + model + ".csv"
    # Save to data folder
    data_path = os.path.join(os.path.dirname(__file__), '..', 'data', data_csv)
    
    fieldname = ["Marca", "Model", "An fabricație", "Preț", "Km", "Combustibil", 
        CAR["Putere"] = conversion.str_to_float(CAR["Putere"])
        
        CAR["Link"] = link
    except Exception as e:
        print(f"Error scraping car {link}: {e}")
        return None

    # Do not quit driver here
    return CAR

def scrape_autovit(make, model):
    data_list = [ ]
    data_csv = make + model + ".csv"
    # Save to data folder
    data_path = os.path.join(os.path.dirname(__file__), '..', 'data', data_csv)
    
    fieldname = ["Marca", "Model", "An fabricație", "Preț", "Km", "Combustibil", 
                "Tip Cutie de viteze", "Tip Caroserie",  "Capacitate Cilindrică", "Putere", "Link"]

    driver = init_driver()
    try:
        links = get_links(driver, make, model)
        print(f"Found {len(links)} total links. Starting scrape...")
        
        for i, lnk in enumerate(links):
            print(f"Scraping {i+1}/{len(links)}: {lnk}")
            CAR = scrape_car_data(driver, lnk)
            if CAR:
                data_list.append( CAR )
            
            time.sleep(1)
    finally:
        driver.quit()

    with open(data_path, mode = 'w', newline='', encoding='utf-8') as file:
        writer = csv.DictWriter(file, fieldnames=fieldname)
        # writer.writeheader()
        writer.writerows(data_list)
    
    print(f"Successfully saved {len(data_list)} cars to {data_csv}")

if __name__ == "__main__":
    import sys
    if len(sys.argv) > 2:
        # Use arguments if provided: python scrapper.py bmw x5
        scrape_autovit(sys.argv[1], sys.argv[2])
    else:
        # Default fallback
        scrape_autovit("dacia", "sandero")
