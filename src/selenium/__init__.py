from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import csv

# Set up Chrome options to prevent bot detection
options = webdriver.ChromeOptions()
options.add_argument("--headless")  # Run in headless mode
options.add_argument("--disable-blink-features=AutomationControlled")  # Prevent detection
options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/110.0.0.0 Safari/537.36")

# Initialize WebDriver
driver = webdriver.Chrome(options=options)

# Open Amazon search results page
query = "laptop"
url = f"https://www.amazon.in/s?k={query}"
driver.get(url)

# Open CSV file to save data
with open("amazon_products.csv", "w", newline="", encoding="utf-8") as file:
    writer = csv.writer(file)
    writer.writerow(["Title", "Price (INR)", "Product Link"])  # CSV Header

    # Loop through multiple pages
    page_number = 1
    while True:
        print(f"📄 Scraping Page {page_number}...")

        # Wait for products to load
        WebDriverWait(driver, 10).until(
            EC.presence_of_all_elements_located((By.XPATH, "//div[@data-component-type='s-search-result']"))
        )

        # Find all product containers
        products = driver.find_elements(By.XPATH, "//div[@data-component-type='s-search-result']")

        for product in products:
            try:
                # Extract Title
                title_element = product.find_element(By.XPATH, ".//span[contains(@class, 'a-text-normal')]")
                title = title_element.text.strip()
            except:
                title = "N/A"

            try:
                # Extract Price
                price_element = product.find_element(By.XPATH, ".//span[@class='a-price-whole']")
                price_fraction_element = product.find_element(By.XPATH, ".//span[@class='a-price-fraction']")
                price = f"{price_element.text.strip()}.{price_fraction_element.text.strip()}"
            except:
                price = "N/A"

            try:
                # Extract Product Link
                link_element = product.find_element(By.XPATH, ".//a[contains(@class, 'a-link-normal')]")
                product_link = link_element.get_attribute("href")
            except:
                product_link = "N/A"

            # Save to CSV
            writer.writerow([title, price, product_link])

        # Check if next page exists and is clickable
        try:
            next_page_button = WebDriverWait(driver, 5).until(
                EC.element_to_be_clickable((By.XPATH, "//a[contains(@class, 's-pagination-next') and not(contains(@class, 's-pagination-disabled'))]"))
            )
            next_page_button.click()
            time.sleep(5)
            page_number += 1
        except:
            print("⚠️ No more pages or pagination blocked. Exiting...")
            break

print("✅ Successfully saved all products to amazon_products.csv!")
driver.quit()
