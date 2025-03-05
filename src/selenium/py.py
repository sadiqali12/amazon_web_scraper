from crewai import Agent, Task, Crew
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import time

class WebAutomationAgent:
    def search_google(self, query):
        # Launch the browser
        driver = webdriver.Chrome()
        driver.get("https://www.google.com")

        # Search for the query
        search_box = driver.find_element(By.NAME, "q")
        search_box.send_keys(query)
        search_box.send_keys(Keys.RETURN)

        # Wait for results and get the first link
        time.sleep(3)
        first_result = driver.find_element(By.CSS_SELECTOR, "h3").text

        driver.quit()
        return first_result

# Create an AI agent in CrewAI
web_agent = Agent(
    role="Web Researcher",
    goal="Search Google and find relevant information",
    backstory="An expert at navigating the web and extracting useful details.",
    verbose=True,
    allow_delegation=False
)

# Define a task for the agent
search_task = Task(
    description="Use Selenium to search Google for 'Selenium Python' and return the top result.",
    agent=web_agent,
    expected_output="The title of the first search result"
)

# Create the Crew
crew = Crew(
    agents=[web_agent],
    tasks=[search_task]
)

# Run the task
result = crew.kickoff()
print("🔍 Search Result:", result)
