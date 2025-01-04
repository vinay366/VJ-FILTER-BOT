
import os
import platform
import requests
import zipfile
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options

def install_chromedriver():
    chrome_version = os.popen("google-chrome --version").read().strip().split()[-1]
    major_version = chrome_version.split(".")[0]

    # Get the latest ChromeDriver version for the installed Chrome
    url = f"https://chromedriver.storage.googleapis.com/LATEST_RELEASE_{major_version}"
    response = requests.get(url)
    if response.status_code != 200:
        raise Exception("Failed to fetch ChromeDriver version.")
    latest_version = response.text.strip()

    # Determine the system's platform
    system = platform.system().lower()
    arch = "64" if platform.architecture()[0] == "64bit" else "32"
    chromedriver_url = f"https://chromedriver.storage.googleapis.com/{latest_version}/chromedriver_{system}{arch}.zip"

    # Download ChromeDriver
    response = requests.get(chromedriver_url, stream=True)
    if response.status_code != 200:
        raise Exception("Failed to download ChromeDriver.")
    with open("chromedriver.zip", "wb") as file:
        file.write(response.content)

    # Extract ChromeDriver to the `bin/` folder
    if not os.path.exists("./bin"):
        os.makedirs("./bin")
    with zipfile.ZipFile("chromedriver.zip", "r") as zip_ref:
        zip_ref.extractall("./bin/")

    os.remove("chromedriver.zip")
    print("ChromeDriver installed successfully.")

def setup_selenium():
    # Install ChromeDriver
    install_chromedriver()

    # Set up Chrome options
    options = Options()
    options.add_argument("--headless")  # Run in headless mode
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")

    # Path to ChromeDriver
    chromedriver_path = "./bin/chromedriver"
    service = Service(chromedriver_path)

    # Initialize WebDriver
    driver = webdriver.Chrome(service=service, options=options)
    return driver

if __name__ == "__main__":
    try:
        driver = setup_selenium()
        # Example: Open a webpage
        driver.get("https://www.google.com")
        print("Page title:", driver.title)
        driver.quit()
    except Exception as e:
        print("Error:", e)
