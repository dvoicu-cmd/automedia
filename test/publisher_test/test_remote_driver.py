from context import src
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By

driver = webdriver.Remote("http://localhost:9515", options=webdriver.ChromeOptions())
driver.get("http://www.google.com")
