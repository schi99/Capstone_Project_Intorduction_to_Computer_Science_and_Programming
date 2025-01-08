import icalendar
import dataclasses
from datetime import datetime, timezone, timedelta
from dateutil.parser import parse
import os
import pprint
from reading_html import load_tables
import uuid

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


# Using dataclasses to label different elements in the course information
@dataclasses.dataclass
class Lesson:
    name: str
    room: str
    day_of_week: str
    date: datetime.date
    start_time: datetime.time
    end_time: datetime.time


CET = timezone(timedelta(hours=1))


# Function to create the calendar element
def create_event(lesson):
    event = icalendar.Event()
    event.add("summary", lesson.name)
    event.add("dtstart", datetime.combine(lesson.date, lesson.start_time))
    event.add("dtend", datetime.combine(lesson.date, lesson.end_time))
    event.add("dtstamp", datetime.now(CET))
    event.add("uid", str(uuid.uuid4()))
    event["location"] = icalendar.vText(lesson.room)
    # Recurring events for weekly courses: a semester lasts 14 weeks
    if "wöchentlich" in lesson.name.lower():
        event.add("rrule", icalendar.vRecur(freq="weekly", count=14))

    return event


def create_lessons(name, course_schedule):
    # Creating an empty list for the lessons to loop over
    lessons = []
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
        # Adding to the list of lessons
        lessons.append(lesson)

    return lessons


def create_calendar(course_info):
    # Initialising the calendar
    calendar_complete = icalendar.Calendar()
    calendar_complete.add("prodid", "-//UniCal//mxm.dk//")
    calendar_complete.add("version", "2.0")
    for i in range(len(course_info)):
        # Extracting the information we need for the calendar output
        course_name = course_info[i].get("Titel", "not found")
        course_schedule = course_info[i].get("Termine", "not found")
        # Special case if a course is weekly and only has information on the first lesson
        # Removing the "wöchentlich" and adding to the the course name for user's information
        # Removing "ab" as this breaks the code
        weekly = "wöchentlich"
        if weekly in course_schedule.lower():
            course_schedule = course_schedule.replace(" ab ", "").replace(weekly, "")
            course_name += " (" + weekly + ")"
        schedule = create_lessons(course_name, course_schedule)
        for lesson in schedule:
            event = create_event(lesson)
            calendar_complete.add_component(event)

    return calendar_complete


lessons = create_calendar(course_info)
# Test on one of the cases that all events were created
# assert len(lessons.events) == 4
# print(lessons)


# Saving the calendar file
def save_calendar(lessons, filename):
    f = open(os.path.join(filename), "wb")
    f.write(lessons.to_ical())
    f.close()


save_calendar(lessons, os.path.join(__location__, "data/unical.ics"))
