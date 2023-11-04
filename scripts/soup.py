from selenium import webdriver
from selenium.webdriver.firefox.options import Options
from bs4 import BeautifulSoup

# Set up headless firefox driver
options = Options()
options.headless = True
driver = webdriver.Firefox(options=options)

# Set our target website
driver.get("https://nordvpn.com/ovpn/")

# Wait for page to load
print("loading page")
driver.implicitly_wait(time_to_wait=10)

# Get the page contents
html = driver.page_source
soup = BeautifulSoup(html, "html.parser")

# Quit driver
driver.quit()

soup.get()