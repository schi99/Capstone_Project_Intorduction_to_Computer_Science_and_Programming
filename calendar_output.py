import icalendar
import dataclasses
from datetime import datetime
from dateutil.parser import parse
import os
import pickle
import pprint
import string
from reading_html import load_tables

"""
This code loads the parsed course data and extracts the information needed for 
the calendar event creation. This includes the course schedule, name of the course and the teacher. 

Author: Heini Järviö
"""

__location__ = os.path.realpath(os.path.join(os.getcwd(), os.path.dirname(__file__)))

course_info = load_tables(os.path.join(__location__, "data/my-tables.pkl"))

# Using pretty print to verify the data has loaded

# pprint.pprint(course_info)

# Using one of the courses to create a template for parsing the information for calendar output
course1 = course_info[1]

# Testing that it worked

# pprint.pprint(course1["Termine"])

# Extracting the information we need for the calendar output
course_name = course1["Titel"]
course_teacher = course1["Dozent/in"]
course_schedule = course1["Termine"]

# Testing it worked

# print(course_name)
# print(course_teacher)
# print(course_schedule)

# Separating the different elements in the schedule into a list
course_schedule_split = course_schedule.split(sep=",")
# Removing blanks to clean the element
course_schedule_split = [text.strip() for text in course_schedule_split]


# Using dataclasses to label different elements in the course information
@dataclasses.dataclass
class Lesson:
    room: str
    day_of_week: str
    date: datetime.date
    start_time: datetime.time
    end_time: datetime.time


# Making a loop to go through the course information list to label different elements
lessons = []
# Dividing by 3 as one lesson time consists of 3 elements
# (Room and day of the week are combined to two as they were not separated by comma in the data)
for i in range(len(course_schedule_split) // 3):
    # j refers to one 'appointment'
    j = i * 3
    room = "unknown"
    day_of_week = course_schedule_split[j]

    # Not all elements have both day and room: if they do, we separate the two
    # Room is placed on the first index of one appointment
    if " " in course_schedule_split[j]:
        room, day_of_week = course_schedule_split[j].rsplit(" ", maxsplit=1)
    # Date is placed on the second index
    date = parse(course_schedule_split[j + 1])
    # Time is placed on the third index; we remove "Uhr" as this is not relevant
    course_schedule_split[j + 2] = course_schedule_split[j + 2].replace(" Uhr", "")
    start_time, end_time = course_schedule_split[j + 2].split(" - ")
    start_time = datetime.combine(date, (datetime.strptime(start_time, "%H:%M").time()))
    end_time = datetime.combine(date, (datetime.strptime(end_time, "%H:%M").time()))
    # Appending the lesson information together to create the separate lessons
    lessons.append(
        Lesson(
            room=room,
            day_of_week=day_of_week,
            date=date,  # Parsing the date to a useful format using the parser
            start_time=start_time,
            end_time=end_time,
        )
    )

print(lessons)
