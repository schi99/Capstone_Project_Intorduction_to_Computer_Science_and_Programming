from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
import numpy as np
import time
import os 



"""
This code provides a Selenium-powered login automation to UniPortal until the step of adding 
an authenticator code. (The the step of adding the authenticator can is not nessecary if the 
usere saved the option that the authentifivation code has to be asked just once a period of time.)

Author: Heini Järviö

"""

# Login credentials (manuel input)

username = "a"
password = "a"

# initialize the Selenium Firefox driver
driver = webdriver.Chrome()

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

# Adding a wait to allow the page to load.$

driver.implicitly_wait(40) # changed 

# Click on print_all

xpath = "//*[contains(@class, 'button-big')]"

print_all = WebDriverWait(driver, 15).until(EC.presence_of_element_located((By.XPATH, xpath)))

driver.execute_script("arguments[0].scrollIntoView();", print_all)

print_all.click()

# downloade HTML

time.sleep(10) 

html_content = driver.page_source

# Define the folder name and ensure it exists
folder_name = "scraped_pages"
project_root = os.getcwd()  # This gets the current working directory
folder_path = os.path.join(project_root, folder_name)
os.makedirs(folder_path, exist_ok=True)  # Create the folder if it doesn't exist

# Save the HTML file in the folder
file_name = "scraped_page.html"
file_path = os.path.join(folder_path, file_name)
with open(file_path, "w", encoding="utf-8") as file:
    file.write(html_content)

print(f"HTML page saved successfully at {file_path}")


# Adding click: Details anzeigen to load the full page  (Was the first attemp didn't work)
# (in the german version there is always vorlesungView_showDetailsLink' in the xpath has to be checked in the english version)
 
'''
There where no informations found on https://portal.unilu.ch/robots.txt so I assumed that it is allowed to scrape the page.

Got the error ('Connection aborted.', ConnectionResetError(10054, 'Eine vorhandene 
Verbindung wurde vom Remotehost geschlossen', None, 10054, None)) when trying to click
So I added a time.sleep(2) to wait for the page to load before clicking the elements.
Further added a random sleep to avoid detection of the bot.


Error clicking element 2: Message: stale element reference: stale element not found
(Session info: chrome=131.0.6778.140); For documentation on this error, please visit: 
https://www.selenium.dev/documentation/webdriver/troubleshooting/errors#stale-element-reference-exception

I failed to loed the hole page but i found that all information can be downloaded 


xpath = "//*[contains(@id, 'showDetailsLink')]"

try:
    while True:
        try:
            # Wait for elements to be present
            elements = WebDriverWait(driver, 15).until(EC.presence_of_all_elements_located((By.XPATH, xpath)))

            for i in range(len(elements)):
                try:
                    # Wait for the page to load before interacting with elements
                    time.sleep(2)
                    driver.implicitly_wait(2)

                    # Adding a random delay to avoid bot detection
                    delay = max(np.random.normal(4, 0.5))  # Ensure delay is valid
                    time.sleep(delay)
                    if isinstance(delay, float):  # Ensure delay is a float before using in sleep
                         time.sleep(delay)

                    # Scroll into view and click
                    element = elements[i]
                    driver.execute_script("arguments[0].scrollIntoView();", element)
                    driver.implicitly_wait(2)
                    element.click()
                    print(f"Clicked element {i + 1}")

                except Exception as e:
                    print(f"Error clicking element {i + 1}: {e}")
                    continue  # Skip stale element errors and retry fetching the element

            # Re-fetch elements after interaction to handle updates
            elements = WebDriverWait(driver, 15).until(EC.presence_of_all_elements_located((By.XPATH, xpath)))

        except Exception as e:
            print(f"Outer loop error: {e}")
            break  # Break outer loop if elements are not found or errors occur

except Exception as e:
    print(f"Unexpected error: {e}")
finally:
    driver.quit()
'''