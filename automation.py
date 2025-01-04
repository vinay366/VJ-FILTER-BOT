from selenium import webdriver
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager

# Set up the Chrome driver
driver = webdriver.Chrome(ChromeDriverManager().install())

# Open a website
driver.get("https://example.com")

# Print the title of the page
print("Page Title:", driver.title)

# Close the browser
driver.quit()
