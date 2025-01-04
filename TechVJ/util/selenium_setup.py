from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium import webdriver

# ChromeDriver ka exact path yahan specify karein
CHROMEDRIVER_PATH = "install_chromedriver.py"  # Linux/Mac
# CHROMEDRIVER_PATH = "C:\\path\\to\\chromedriver.exe"  # Windows

def setup_selenium():
    options = Options()
    options.add_argument("--headless")  # Background mode
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")

    # ChromeDriver service
    service = Service(CHROMEDRIVER_PATH)
    driver = webdriver.Chrome(service=service, options=options)
    return driver

# Test Selenium Setup
try:
    driver = setup_selenium()
    driver.get("https://www.google.com")
    print("Page Title:", driver.title)
    driver.quit()
except Exception as e:
    print("Error:", e)
