# Report: Project UniCal

#### *Introduction to Computer Science and Programming, University of Luzern, Autumn 2024, Kai Waelti*

#### Group 4: Heini Järviö & Benjamin Schibli


## 1. Introduction

*Project UniCal* was initiated to provide a useful tool for students in University of Luzern: an automated way to get their course schedule from the Uniportal site directly to their calendar software. To our knowledge, such tool does not yet exist although it would be highly useful for all students, as it saves time and helps avoid human errors that can result from manual addition of said information. The usage requires only beginner skills in computer use. 

This report will provide an overview of the UniCal program and the key steps in the development process. In the next section, we will describe the background of the project. This is followed by description of development process, including a summary of methods used, solutions to encountered problems and details on how the results of the project were achieved. Finally, I will summarise the results, including limitations and directions for future development. 

## 2. Background

Currently, course timetables are available to students in a text format on the university's Uniportal platform. This means that a student who wishes to have their course schedule readily available on their electronic calendar or other format outside of Uniportal has to manually enter all lessons separately to a calendar. While we assume that there might be universities that already offer students a downloadable calendar in electronic format, we were not able to find any resources that would provide the source code for this. Furthermore, we aknowledge that such code would not work for this project as universities tend to use different systems for student information. Thus, this project creates a novel approach to a course timetable creation to be specifically used in University of Luzern. Being the first of its kind, this project can also be used as a starting point for further development ideas.

While there are some tutorials and examples online on how to turn a scraped information to a calendar file, we did not find one that would apply to the same data structure. Therefore the current approach is a patchwork quilt of our own ideas and solutions to small sub-problems found on websites like stackoverload or github.

## 3. Project

The initial plan for the project consisted of four sub-tasks:

 1. Automating the login to Uniportal using Selenium
 2. Scraping the course information from Uniportal and saving it as an HTML file
 3. Parsing the scraped information to a more usable form
 4. Using the parsed information and creating a .ics file of the course timetable

 The implementation process was as follows:

 1. Automating the login to Uniportal using Selenium (spesific file: selenium_login_uniportal.py)

 For this step we used a Selenium driver combined with stored user credentials. The driver would open Uniportal in a new window, and would be directed to the Switch edu-ID login. The login involves choosing the right university and sending the user creadentials to the correct fields, which were identified using XPATH notation. Switch edu-ID, that is used to login to Uniportal, requires two-factor-authentication. Surprisingly, one the group members was available to skip the autenticator code -step of the login process while the other one was not. While requiring a two-factor-login this feature was deemed quite impractical, as the user would have to provide authenticator code each time they wanted to use the feature, which would make the automation pointless.

To go around this issue,  we also attempted to create a Selenium browser automation that could access a pre-existing browser window. The reasoning for this step was that accessing an existing window would utilise saved cookies, therefore avoiding the problem of the two-factor authentication. The process involved using the browser's profiles-functionality and installation of the geckodriver. However, this attempt, too, was unsuccesful. The github repository includes a python file that shows an attempt at this (selenium_profiles_uniportal.py). Thus, step 1 was discarded as we could not guarantee it works for all users.

 2. Scraping the course information from Uniportal and saving it as a HTML file

 Following from challenges in step one, the goal of automated login an scraping process was dropped. Thus, this part was left to do manually by the user. Uniportal offers a "print all" possibility on the 'Courses' (or 'Lehrveranstaltungen') page, that allows one to access all course data on one page and to save the course information as a HTML-file on their computer. Instructions to this step were written to the readme file in Github.

 3. Parsing the scraped information to a more usable form (spesific file: reading_html.py)

 The uniportal page gives the course information in a table format, with one table for one course. Typically, the tables have two columns and several rows, and the first column has the "title" of the information (e.g. Course code, content) that standardised for all courses and the second lists the course-specific details for said title. 

To read and parse the information from the html file, *pandas* and *beautifulsoup* libraries were used. First, we used the html parser from beautifulsoup to parse the data and then identified all the tables (courses). The tables were converted to a string and then, using the pandas library, read to a list of tables. 

To better usability, we wanted to store the data as a list of dictionaries. This would allow accessing specific rows by naming the key (e.g. "Termine" or "Events") and one course at a time. This was done by creating a table_to_dict function that reads and element on the first index of a table to a list of list of keys and on the second index to a list of values. These key and value lists were then "zipped" together to create a dictionary.

During this process we noticed an error occuring for some of the courses. This error was traced back to the structure of the data; some rows in the course information tables had a table in them. As this occured in rows that were not relevant for the project, a function was added to identify and add only those tables with two columns. 

Finally, the newly created list of dictionaries was saved using the pickle module of python. This allowed us to access the information later in the exact same format.

 4. Using the parsed information, creating a .ics file of the course timetable (spesific file: calendar_output.py)

 For the final step, date and calendar related modules (*icalendar* and *datetime*) as well as the dataclasses module were used. To start, a parsing code and calendar output were created for the first course in the dictionary as a test element. When this was succesful, the code was generalised to work for all the courses in the dictionary. In the end, three functions were necessary for creation of the calendar output.

To create the planned calendar output, it was necessary to identify four elements for each class of each course: the date, start time, end time and the room. Additionally, each calendar event should include the name of the course. For easier sorting, we used the dataclasses module to identify these elements in one course.

The implementation has three key functions: 1. creating the separate course events (classes) of one course, 2. creating an icalendar compatible object of these course events and 3. lastly, to combine all events from all courses to one calendar. In 1. we looped over all events of one course. In 2. the the events were formated using the icalendar module to comply with the .ics file requirements and in 3. we looped over all courses and applied the earlier steps to form a complete calendar. 

Identifying the different time artefacts and the room from the course schedule posed greatest challenges. This was because this information was all given on set of rows with differing separators (e.g. "Tue, 4.12., 8.00-16.00, B3.456"). Splitting with commas to separate the elements (day of week, date, time, room) led to suitable results for the date and time information, but problems arose for identifying the room number, as this was separated from the next line only with a blank. For this reason, an additional loop was added to split day of the week and room to two separate elements, thus creating a list of the course information where one course has a lenght of four items. 

Additional challenge came from courses that would occur weekly, as these would be listed in Uniportal with only the starting date. For these courses we needed to remove the "ab" or "from" from the schedule and establish a recurrence. A proximal solution was found by repeating the event 14 times, as this is the length of a semester in Switzerland. This solution was seen as sufficient although not entirely accurate, as it may ran into conflict with holidays. Finally, the compelete calendar was saved as .ics file and main.py was created to combine all necessary functions to one file for easier use. 

### 3.1. Design details

As this was the first attempt at creating a calendar file from Uniportal's course information, our approach was novel and rather than following an existing blueprint, it combined advice from versatile resources. Unsurprisingly, some modifications were made during the process. 

As stated earlier, the original plan for this program was to provide a code that would automate the login, leading to the webscraping and calendar output creation process. However, multiple attempts revealed that this part was beyond the scope of this project due to issues related to two-factor-authentication and browser specifications. Thus, the goal was updated to include the remaining steps implemented on a HTML-document saved directly from UniPortal by the user.

The most important resources were related to the use of the icalendar and datetime modules. In the case of datetime, stackoverflow was used frequently to troubleshoot and brainstorm ideas on how to format the scraped schedule into a usable time object. Additionally, the icelandar documentation was referenced for the spesifics of the usage of this module and for creating the specific cases such as recurring events.

 Throughout the coding process, breakpoints and printing were used to debug the code and search for errors. For testing, we used our own course data from Uniportal, assuming this would provide the potential variations in the way course information is announced.

Additionally, we a had an optional goal of using LLM integration to create calendar events for important assignment deadlines based on information available at Uniportal. However, this goal was abandoned fairly early on in the project due to time constraints. 

### 3.2. Results

This project managed to reach most of its goals in a robust manner. The current code succesfully generates a calendar output (as shown below in outlook calendar) and provides the room information. Based on our test cases the event creation is reliable and accurate, apart from overlaps with holiday times. All in all, the project has succesfully created a useful tool for students in University of Luzern that can save time and that can modernise some of the university systems.

![alt text](report_pic.PNG)

At its current stage, the program has some limitations. Most importantly, the current code only works on the German version of Uniportal, requiring more attentive work by the user. Additionally, the current code relies on a semester lenght of 14 weeks and is not able to detect conflicting events. Thus, user should not fully rely on the output and for weekly events, should check the correctness of the output.

## 4. Conclusion

Project UniCal was created to offer a useful tool for transfering their course schedule from Uniportal to an electronic calendar for students in University of Luzern. Achieving this main goal has been successful - the output created by our code works in a robust and accurate manner and is fairly simple to use even for those with limited computer fluency. 

The current solution provides a good starting point for further innovation and development. First, as the code currently works only for the German language version of Uniportal, a natural next step could be extending the functionality to the English language site. Second, a clear improvement in accessibility would be creating a simple website that students could use to create the calendar file. As this course did not include web development this was currently beyond the scope of this project. However, a website like this would make the use a lot easier and straightforward, and would thus be a significant development. Lastly, the original planning for the project included a LLM-powered study support in the shape of creating calendar deadline events. Although this goal was now discarded, it could be a potential improvement for the program. Such feature would identify the final assignments from the existing course information and create events for essay/exam deadlines and potentially additional sub-deadlines. Thus, the project could also serve as support for study skills building. 

For our group, this project has been an opportunity to learn about webscraping and data manipulation, and given a useful overview of steps involved in simple program development. Further, it has been a practical exercise in debugging and problem-solving, and the persistent work ethic sometimes needed in the process, when even the best efforts seem to have failed. Setting milestones and deadlines helped to pace the work and identify appropriate time spent on one task - this is a method we could have utilised even more during the process. All in all, the project has increased our self-efficacy and confidence in applying the learned skills to future projects.

## 5. References

Selenium automation:
https://www.selenium.dev/documentation/
<br>
https://github.com/mozilla/geckodriver 
<br>
Beautifulsoup, pandas:
https://beautiful-soup-4.readthedocs.io/en/latest/
https://pandas.pydata.org/docs/user_guide/index.html
<br>
Pickle module:
https://docs.python.org/3/library/pickle.html
<br>
Data classes:
https://medium.com/@pouyahallaj/python-data-classes-the-key-to-clean-maintainable-code-a76a740d9884
<br>
https://stackoverflow.com/questions/47955263/what-are-data-classes-and-how-are-they-different-from-common-classes
<br>
Icalendar:
https://icalendar.readthedocs.io/en/latest/usage.html
<br>
https://github.com/collective/icalendar
<br>
https://icalendar.org/
<br>
datetime module:
https://docs.python.org/3/library/datetime.html
<br>
Python documentation was read for basic operations for e.g. strings
https://docs.python.org/3/
<br>
Countless stackoverflow discussions were read in the process of problem solving.
LLMs such as ChatGPT and github copilot were used to resolve bugs.
