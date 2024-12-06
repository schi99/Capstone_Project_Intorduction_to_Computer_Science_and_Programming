import pathlib

from selenium import webdriver
from selenium.webdriver.firefox.service import Service
from selenium.webdriver.firefox.options import Options

"""
Note: this code did not work and is only provided to show which trials were made in the process.

The aim of this code was to access an existing firefox window through the use of profile functionality 
to utilise the saved cookies for web scraping automation. The path information has been removed for simplicity.

For this code, geckodriver was downloaded from https://github.com/mozilla/geckodriver and added to the project's directory.

Author: Heini Järviö

"""

# path to Firefox installation
firefox_binary_path = pathlib.Path(
    "C:\\Program Files (x86)\\Mozilla Firefox\\firefox.exe"
)

# Path to your Firefox profile in the existing browser
firefox_profile_path = pathlib.Path("profile path here")  # add profile path

# Path to geckodriver
geckodriver_path = pathlib.Path("geckodriver path here")

# Setting up Firefox options to use the existing profile
options = webdriver.FirefoxOptions()
options.add_argument("-profile")
options.add_argument(r"profile path here")

# setting up the options for the Webdriver
profile = webdriver.FirefoxProfile(str(firefox_profile_path))
options.binary_location = str(firefox_binary_path)
options.profile = profile

# Create a WebDriver instance with the profile
driver = webdriver.Firefox(options=options)

try:
    # Navigate to the target website
    driver.get("https://portal.unilu.ch/site/studierende/vorlesungen/anmeldungen.aspx")

    # Scraping code would go here

    print(driver.page_source)  # Testing if the driver can print the html source

finally:
    # Closing the browser when the scraping is finished
    driver.quit()
