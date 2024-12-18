import pandas as pd
from bs4 import BeautifulSoup
import os

__location__ = os.path.realpath(os.path.join(os.getcwd(), os.path.dirname(__file__)))


def read_html_with_beautiful_soup(file_path):
    # Read HTML file
    with open(file_path, encoding="utf-8") as f:
        # Parse HTML using BeautifulSoup
        soup = BeautifulSoup(f, "html.parser")
    # Find all tables in the HTML
    tables = soup.find_all("table")
    # Read tables into DataFrame using read_html()
    df = pd.read_html(str(tables))[0]
    return df


# File path
html_file_path = os.path.join(__location__, "data/scraped_page.htm")

# Read HTML file using BeautifulSoup with read_html()
df = read_html_with_beautiful_soup(html_file_path)

# Display DataFrame
print(df)
