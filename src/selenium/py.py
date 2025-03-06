import csv
import time
import random
from crewai import Agent, Task, Crew
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager

class AmazonScraper:
    def __init__(self, query="laptop", max_products=10, max_pages=2):
        self.query = query
        self.max_products = max_products
        self.max_pages = max_pages
        self.products_collected = 0
        self.csv_filename = "amazon_products.csv"

    def setup_driver(self):
        chrome_options = Options()
        chrome_options.add_argument("--disable-blink-features=AutomationControlled")
        chrome_options.add_argument("--incognito")  
        chrome_options.add_argument("start-maximized")
        chrome_options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/110.0.0.0 Safari/537.36")
        driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=chrome_options)
        return driver

    def scrape_amazon(self):
        driver = self.setup_driver()
        url = f"https://www.amazon.in/s?k={self.query}"
        driver.get(url)
        time.sleep(random.uniform(3, 6))

        with open(self.csv_filename, mode="w", newline="", encoding="utf-8") as file:
            writer = csv.writer(file)
            writer.writerow(["Title", "Price", "Rating"])  

            for page in range(1, self.max_pages + 1):
                print(f"📄 Scraping Page {page}...")

                elements = driver.find_elements(By.XPATH, "//div[@data-component-type='s-search-result']")
                for elem in elements:
                    if self.products_collected >= self.max_products:
                        break  

                    try:
                        title = elem.find_element(By.TAG_NAME, "h2").text
                    except:
                        title = "N/A"

                    try:
                        price = elem.find_element(By.CLASS_NAME, "a-price-whole").text
                    except:
                        price = "N/A"

                    try:
                        rating = elem.find_element(By.CLASS_NAME, "a-icon-alt").text
                    except:
                        rating = "N/A"

                    writer.writerow([title, price, rating])
                    self.products_collected += 1

                try:
                    next_button = driver.find_element(By.XPATH, "//a[contains(@class, 's-pagination-next')]")
                    if "disabled" in next_button.get_attribute("class"):
                        print("🚨 No more pages available.")
                        break  
                    next_button.click()
                    time.sleep(random.uniform(5, 8))
                except:
                    print("⚠️ Could not find Next Page button. Exiting...")
                    break

        driver.quit()
        return f"✅ Successfully saved {self.products_collected} products to {self.csv_filename}!"

# CrewAI Agent
amazon_agent = Agent(
    role="Amazon Product Researcher",
    goal="Find and extract product details from Amazon based on a given search query.",
    backstory="An AI agent skilled in web scraping and data extraction, capable of searching Amazon for product details.",
    verbose=True,
    allow_delegation=False
)

# CrewAI Task
amazon_task = Task(
    description="Scrape Amazon for 10 products related to 'laptop' and store their details in a CSV file.",
    agent=amazon_agent,
    expected_output="A CSV file containing product titles, prices, and ratings."
)

# CrewAI Crew
crew = Crew(
    agents=[amazon_agent],
    tasks=[amazon_task]
)

# Run the CrewAI Task
scraper = AmazonScraper(query="laptop", max_products=10, max_pages=2)
result = scraper.scrape_amazon()
print(result)
