from selenium import webdriver
from selenium.webdriver.chrome.service import Service

# Specify the path to chromedriver using the Service class
s = Service('/usr/local/bin/chromedriver')
driver = webdriver.Chrome(service=s)

# Open a website
driver.get("http://www.google.com")

# ... perform actions or tests ...

# Close the browser
driver.quit()
