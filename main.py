from reading_html import (
    table_to_dict,
    read_html_with_beautiful_soup,
    save_tables,
    load_tables,
)
from calendar_output import create_event, create_lessons, create_calendar, save_calendar
import os

__location__ = os.path.realpath(os.path.join(os.getcwd(), os.path.dirname(__file__)))

html_file_path = os.path.join(__location__, "data/scraped_page.htm")

tables = read_html_with_beautiful_soup(html_file_path)

save_tables(os.path.join(__location__, "data/my-tables.pkl"), tables)

course_info = load_tables(os.path.join(__location__, "data/my-tables.pkl"))

lessons = create_calendar(course_info)

save_calendar(lessons, os.path.join(__location__, "data/unical.ics"))
