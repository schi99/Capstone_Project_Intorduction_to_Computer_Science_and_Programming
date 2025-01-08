import pandas as pd
from bs4 import BeautifulSoup
import os
import pickle
from io import StringIO

"""
This code reads the previously stored "scraped_page" html-file 
that contains the information of a student's course selection. This file contains the necessary information
in a set of tables, where one table contains the information from one course.

The beautifulsoup library is used to read the file into a list that is then 
combined into a dictionary object for easier future use. This dictionary is 
then stored as a binary object using the pickle module.

Author: Heini Järviö

"""

# Defining the location of the working directory
__location__ = os.path.realpath(os.path.join(os.getcwd(), os.path.dirname(__file__)))

# File path to the stored html file
html_file_path = os.path.join(__location__, "data/uniportal.htm")

# A function that is used to create a dictionary of a table in the data by combining
# the information from first index of the list with information from the second index


def table_to_dict(table):
    keys = table.iloc[:, 0].tolist()
    values = table.iloc[:, 1].tolist()
    dictionary = dict(zip(keys, values))
    return dictionary


# A function to parse data from the stored html file


def read_html_with_beautiful_soup(file_path):
    # Read HTML file, making sure encoding is utf-8
    with open(file_path, encoding="utf-8") as f:
        # Parse HTML using BeautifulSoup
        soup = BeautifulSoup(f, "html.parser")
    # Find all tables in the HTML
    tables = soup.find_all("table")
    # Convert the tables to a string and wrap it in a StringIO object
    tables_str = str(tables)
    tables_io = StringIO(tables_str)
    # Read tables into DataFrame using read_html()
    dfs = pd.read_html(tables_io)

    # df.shape gives us the number of [rows, columns] in the dataframe.
    # We check all of the dataframes in dfs and only keep the ones that
    # have columns == 2.
    dfs_with_two_cols = []
    for df in dfs:
        if df.shape[1] == 2:
            dfs_with_two_cols.append(df)

    # Using the earlier defined function, we combine all tables into a nested dictionary

    dicts = []
    for df in dfs_with_two_cols:
        dicts.append(table_to_dict(df))

    return dicts


# Saving our dictionary of tables using pickle
def save_tables(filename, tables):
    with open(filename, "wb") as file:
        pickle.dump(tables, file)


# A function to load our data again; testing that it was stored correctly
def load_tables(filename):
    with open(filename, "rb") as file:
        return pickle.load(file)


# We add this part so that the whole code is not run when we import a function to another script

if __name__ == "__main__":
    # Read HTML file using BeautifulSoup with read_html()
    tables = read_html_with_beautiful_soup(html_file_path)

    # Defining the file name and location in the data-folder
    save_tables(os.path.join(__location__, "data/my-tables.pkl"), tables)

    loaded_tables = load_tables(os.path.join(__location__, "data/my-tables.pkl"))

    # Displaying the loaded dataframe
    print(loaded_tables)

    __location__ = os.path.realpath(
        os.path.join(os.getcwd(), os.path.dirname(__file__))
    )
    file_path = os.path.join(__location__, "data/my-tables.pkl")
    print(os.path.exists(file_path))
