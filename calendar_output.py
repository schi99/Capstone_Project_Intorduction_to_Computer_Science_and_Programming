import icalendar
import datetime
import os
import pickle
import pprint
from reading_html import load_tables

__location__ = os.path.realpath(os.path.join(os.getcwd(), os.path.dirname(__file__)))

course_info = load_tables(os.path.join(__location__, "data/my-tables.pkl"))

pprint.pprint(course_info)
