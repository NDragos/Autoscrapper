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

def get_safely_data(driver, path):
    try:
        html_content = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, path)))
        return html_content.get_attribute("textContent")
    except:
        return "N/A"


def get_links_on_page(make, model, page):

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
        driver.get("https://www.autovit.ro/autoturisme/" + make + "/" + model + "?page=" + page)

        # input("Press Enter after the page loads completely...")

        # Get all links on the page
        all_links = driver.find_elements(By.TAG_NAME, "a")
        print(f"Found {len(all_links)} total links on page")

        # Filter for car listing links
        for link in all_links:
            href = link.get_attribute("href")
            if href and "/anunt/" in href and make in href.lower():
                if href not in car_links:
                    car_links.append(href)
                    print(f"Found: {href}")

        print(f"\nTotal unique car links: {len(car_links)}")

    except Exception as e:
        print(f"Error: {e}")
    finally:
        driver.quit()

    return car_links

def get_links(make, model):
    chrome_options = Options()
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
    chrome_options.add_argument("--window-size=1920,1080")

    driver = webdriver.Chrome(options=chrome_options)

    try:
        driver.get("https://www.autovit.ro/autoturisme/" + make + "/" + model)
        number_ads = get_safely_data(driver, "//div/p/b")
    except Exception as e:
        print(f"Error: {e}")
        return None
    finally:
        driver.quit()

        time.sleep(1)
        number_ads = conversion.str_to_int(number_ads)
        number_pages = math.floor(number_ads / 32) + 1 #32 is the number of ads per page 
        page = 1

        all_links = []
        while page <= number_pages:
            all_links += get_links_on_page(make, model, str(page))
            page += 1
            time.sleep(1)
        
        return all_links

def scrape_car_data(link):
    chrome_options = Options()
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
    chrome_options.add_argument("--window-size=1920,1080")

    driver = webdriver.Chrome(options=chrome_options)
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
    fieldname = ["Marca", "Model", "An fabricație", "Preț", "Km", "Combustibil", 
                "Tip Cutie de viteze", "Tip Caroserie",  "Capacitate Cilindrică", "Putere", "Link"]

    links = get_links(make, model)
    for i, lnk in enumerate(links):
        CAR = scrape_car_data( links[i] )
        data_list.append( CAR )
        
        time.sleep(1)

    with open(data_csv, mode = 'w', newline='') as file:
        writer = csv.DictWriter(file, fieldnames=fieldname)
        # writer.writeheader()
        writer.writerows(data_list)  

if __name__ == "__main__":
    scrape_autovit("dacia", "sandero")

