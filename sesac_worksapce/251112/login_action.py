from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
import time

options = Options()
options.add_experimental_option("detach",True)

driver = webdriver.Chrome(options=options)

url = "https://www.naver.com/"
driver.get(url)
time.sleep(2)

login_btn = driver.find_element(By.XPATH,//*[@id="account"]/div/a)
login_btn.click()