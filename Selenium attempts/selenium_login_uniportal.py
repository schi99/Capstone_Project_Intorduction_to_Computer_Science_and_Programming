from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC

"""
This code provides a Selenium-powered login automation to UniPortal until the step of adding 
an authenticator code. 

Author: Heini Järviö

"""

# Login credentials
username = " "
password = " "

# initialize the Selenium Firefox driver
driver = webdriver.Firefox()

# head to uniPortal login page
driver.get("https://portal.unilu.ch/site/studierende/vorlesungen/anmeldungen.aspx")

# Clicking open the dropdown menu for choosing the right university.
# A wait was added to allow the page to download before the click.

result = WebDriverWait(driver, 20).until(
    EC.element_to_be_clickable((By.XPATH, '//*[(@id = "userIdPSelection_iddicon")]'))
)

# Choosing University of Luzern by inputing it as a text to the form.

input = driver.find_element(By.XPATH, '//*[(@id = "userIdPSelection_iddtext")]')

value = "Universität Luzern"
input.send_keys(value)

# Clicking the select

submit = driver.find_element(By.NAME, "Select")
submit.click()

# Adding a wait to allow the page to download.

driver.implicitly_wait(5)

# Inserting a username and moving to the next page

name = driver.find_element(By.ID, "username")
name.send_keys(username)

driver.find_element(By.ID, "button-submit").click()

# Inserting a password and moving to the next page

pass1 = driver.find_element(By.ID, "password")
pass1.send_keys(password)

driver.find_element(By.ID, "button-proceed").click()
