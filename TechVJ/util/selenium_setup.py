from selenium.webdriver.chrome.service import Service
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import os

CHROMEDRIVER_PATH = os.getenv("CHROMEDRIVER_PATH")  # Path environment variable se lo

def setup_selenium():
    options = Options()
    options.add_argument("--headless")  # GUI ke bina run kare
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")

    service = Service(CHROMEDRIVER_PATH)  # ChromeDriver ka path yahaan pass karo
    driver = webdriver.Chrome(service=service, options=options)
    return driver
