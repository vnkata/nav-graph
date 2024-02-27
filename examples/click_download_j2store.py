import chromedriver_binary

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webelement import WebElement

options = Options()
# options.add_argument('--headless')
options.add_argument('--disable-gpu')
options.add_argument('--no-sandbox')
options.add_argument('--disable-dev-shm-usage')
driver = webdriver.Chrome(options=options)

driver.get("https://www.j2store.org/")
download_btn = driver.find_element(By.XPATH, """//nav[@id='t3-mainnav']/div[2]/div/div/ul/li[2]/div/div/div/div/div/ul/li/a""")
download_btn.click()


print ("Done~")