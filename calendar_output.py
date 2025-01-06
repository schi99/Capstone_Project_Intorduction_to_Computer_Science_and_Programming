import icalendar
import dataclasses
from datetime import datetime
from dateutil.parser import parse
import os
import pprint
from reading_html import load_tables
import tempfile

"""
This code loads the parsed course data and extracts the information needed for 
the calendar event creation. This includes the name of the course and the lesson times.

Author: Heini Järviö
"""

__location__ = os.path.realpath(os.path.join(os.getcwd(), os.path.dirname(__file__)))

# Loading the scraped courses

course_info = load_tables(os.path.join(__location__, "data/my-tables.pkl"))

# Using pretty print to verify the data has loaded

# pprint.pprint(course_info)

# Using one of the courses to create a template for parsing the information for calendar output
course1 = course_info[0]
# Testing that it worked

# pprint.pprint(course1)

# Extracting the information we need for the calendar output
course_name = course1["Titel"]
course_teacher = course1["Dozent/in"]
course_schedule = course1["Termine"]

# Testing it worked

# print(course_name)
# print(course_teacher)
# print(course_schedule)

# Special case if a course is weekly and only has information on the first lesson
# Removing the "wöchentlich" and adding to the the course name for user's information
# Removing "ab" as this breaks the code
weekly = "wöchentlich"
if weekly in course_schedule:
    course_schedule = course_schedule.replace(" ab ", "").replace(weekly, "")
    course_name += " (" + weekly + ")"


# Using dataclasses to label different elements in the course information
@dataclasses.dataclass
class Lesson:
    name: str
    room: str
    day_of_week: str
    date: datetime.date
    start_time: datetime.time
    end_time: datetime.time


# Function to create the calendar element
def create_event(lesson):
    event = icalendar.Event()
    event.add("summary", lesson.name)
    event.add("dtstart", datetime.combine(lesson.date, lesson.start_time))
    event.add("dtend", datetime.combine(lesson.date, lesson.end_time))
    event["location"] = icalendar.vText(lesson.room)

    return event


def create_lessons(name, course_schedule):
    cal = icalendar.Calendar()
    """This function turns a course schedule into a list of lessons."""

    # Separating the different elements in the schedule into a list
    course_schedule_split = course_schedule.split(sep=",")
    # Removing blanks to clean the element
    course_schedule_split = [text.strip() for text in course_schedule_split]
    # Making a loop to go through the course information list to label different elements
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
        # Date is placed on the second index, parsing the date to a useful format using the parser
        date = parse(course_schedule_split[j + 1], dayfirst=True)
        # Time is placed on the third index; we remove "Uhr" as this is not relevant
        course_schedule_split[j + 2] = course_schedule_split[j + 2].replace(" Uhr", "")
        start_time, end_time = course_schedule_split[j + 2].split(" - ")
        start_time = datetime.strptime(start_time, "%H:%M").time()
        end_time = datetime.strptime(end_time, "%H:%M").time()
        # Appending the lesson information together to create the separate lessons
        lesson = Lesson(
            name=name,
            room=room,
            day_of_week=day_of_week,
            date=date,
            start_time=start_time,
            end_time=end_time,
        )
        # Creating a calendar event of a lesson
        ev = create_event(lesson)
        # Adding it to the calendar
        cal.add_component(ev)

    return cal


lessons = create_lessons(name=course_name, course_schedule=course_schedule)
# Test on one of the cases that all events were created
# assert len(lessons.events) == 4
print(lessons)

# Saving the calendar file
f = open(os.path.join(__location__, "data/example.ics"), "wb")
f.write(lessons.to_ical())
f.close()
