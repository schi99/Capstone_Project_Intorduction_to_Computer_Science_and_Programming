import pandas as pd
from bs4 import BeautifulSoup
import os

__location__ = os.path.realpath(os.path.join(os.getcwd(), os.path.dirname(__file__)))


def table_to_dict(table):
    keys = table.iloc[:, 0].tolist()
    values = table.iloc[:, 1].tolist()
    dictionary = dict(zip(keys, values))
    return dictionary


def read_html_with_beautiful_soup(file_path):
    # Read HTML file
    with open(file_path, encoding="utf-8") as f:
        # Parse HTML using BeautifulSoup
        soup = BeautifulSoup(f, "html.parser")
    # Find all tables in the HTML
    tables = soup.find_all("table")
    # Read tables into DataFrame using read_html()
    dfs = pd.read_html(str(tables))

    # df.shape gives us the number of [rows, columns] in the dataframe.
    # We check all of the dataframes in dfs and only keep the ones that
    # have columns == 2.
    dfs_with_two_cols = []
    for df in dfs:
        if df.shape[1] == 2:
            dfs_with_two_cols.append(df)

    dicts = []
    for df in dfs_with_two_cols:
        dicts.append(table_to_dict(df))

    return dicts


# File path
html_file_path = os.path.join(__location__, "data/scraped_page.htm")

# Read HTML file using BeautifulSoup with read_html()
tables = read_html_with_beautiful_soup(html_file_path)

# Display DataFrame
print(tables)
