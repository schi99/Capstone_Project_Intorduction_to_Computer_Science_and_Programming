from reading_html import read_html_with_beautiful_soup, save_tables
from calendar_output import create_calendar, save_calendar
import os

"""
This code loads the downloaded HTML file, parses the data and
creates a .ics file of the course information for the user to access with thei calendar application.

Author: Heini Järviö
"""

if __name__ == "__main__":

    __location__ = os.path.realpath(
        os.path.join(os.getcwd(), os.path.dirname(__file__))
    )

    html_file_path = os.path.join(__location__, "data/uniportal.htm")

    course_info = read_html_with_beautiful_soup(html_file_path)

    # Saving the tables for later use
    save_tables(os.path.join(__location__, "data/my-tables.pkl"), course_info)

    lessons = create_calendar(course_info)

    save_calendar(lessons, os.path.join(__location__, "data/unical.ics"))
