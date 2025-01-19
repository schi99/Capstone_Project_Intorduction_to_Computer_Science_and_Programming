# Project report

## 1. Introduction

*Project UniCal* was initiated to provide a useful tool for students in University of Luzern: an automated way to get their course schedule directly to their calendar software. To our knowledge, such tool does not yet exist although it would be highly useful for all students, as it saves time and helps avoid human errors that can result from manual addition of said information. 

This report will provide an overview of the UniCal program and the key steps in the development process. In the next section, we will describe the background of the project. This is followed by description of the project, including a summary of methods used, solutions to encountered problems and details on how the results of the project were achieved. 

- Provide a description of your program, including its purpose and functionality (scope and goal)
- Explain where and how the program is used (context)
- Discuss why the project is important
- Summarize the content and structure of the report

## 2. Background

Currently, course timetables are available to students in a text format on the university's Uniportal platform. This means that a student who wishes to have their course schedule readily available on their electronic calendar or other format outside of Uniportal has to manually enter all lessons separately to a calendar. While we assume that there might be universities that already offer students a downloadable electronic format, we were not able to find any resources that would provide the source code for this. Furthermore, we aknowledge that such code would not work for this project as universities tend to use different systems for student information. Thus, this project creates a novel approach to a course timetable creation.

While there are some tutorials and examples online on how to turn a scraped information to a calendar file, we did not find one that would apply to the same data structure. Therefore the current approach is a patchwork quilt of our own ideas and solutions to small sub-problems found on websites like stackoverload or github.

- Outline prior research or projects relevant to your work, citing references as appropriate
- Discuss limitations or shortcomings in previous approaches
- Explain how your work improves upon or differs from existing solutions
- Provide any additional details necessary for understanding your project (context)

## 3. Project

The initial plan for the project consisted of four sub-tasks:
 1. Automating the login to Uniportal using Selenium
 2. Scraping the course information from Uniportal and saving it as a HTML file
 3. Parsing the scraped information to a more usable form
 4. Using the parsed information, creating a .ics file of the course timetable

 Additionally, we a had an optional goal of using LLM integration to create calendar events for important assignment deadlines based on information available at Uniportal. However, this goal was abandoned fairly early on in the project due to time constraints. 

 The implementation process was as follows:

 1. Automating the login to Uniportal using Selenium (spesific file: selenium_login_uniportal.py)

 For this step we used a Selenium driver combined with stored user credentials. The driver would open Uniportal link in a new window, and would be directed to the Switch edu-ID login. The login involves choosing the right university and sending the user creadentials to the correct fields, which were identified using the XPATH notation. The Switch edu-ID uses two-factor-authentication. Surprisingly, one of us was available to skip the autenticator code -step of the login process while the other one was not. While requiring a two-factor-login this feature was deemed quite impractical, as the user would have to provide authenticator code each time they wanted to use the feature, which would make the automation pointless.

To go around this issue,  we also attempted to create a Selenium browser automation that could access a pre-existing browser window, where user had already completed the log-in process to UniPortal and subsequently automate the remaining steps. The reasoning for this step was that accessing an existing window would utilise saved cookies, therefore avoiding the problem of the two-factor authentication. The process involved use the browser's profiles-functionality and installation of the geckodriver. However, this attempt, too, was unsuccesful. The github repository includes a python file that shows an attempt at this.

 2. Scraping the course information from Uniportal and saving it as a HTML file

 Following from challenges in step one, the goal of automated login an scraping process was dropped. Thus, this part was left to do manually by the user. Uniportal offers a "print all" possibility on the 'Courses' (or 'Lehrveranstaltungen') page, that allows one to access all course data on one page and to save the course information as a HTML-file on their computer. Instructions to this step were written to the readme file. 

 3. Parsing the scraped information to a more usable form (spesific file: reading_html.py)

 The uniportal page gives the course information in a table format, with one table for one course. Typically, the tables have two columns and several rows, and the first column has the "title" of the information (e.g. Course code, content) that standardised for all courses and the second lists the details for said title. 

To read and parse the information from the html file, the pandas and beautiful soup libraries were used. First, we used the html parser from beautifulsoup to parse the data and then identified all the tables (courses). The tables were converted to a string and then, using the pandas library, read to a list of tables. 

To better usability, we wanted to store the data as a list of dictionaries. This would allow accessing specific rows by naming the key (e.g. "Termine" or "Events") and one course at a time. This was done by creating a table_to_dict function, that reads and element on the first index of a table to a list of list of keys and on the second index to a list of values. These key and value lists were then "zipped" together to create a dictionary.

During this process we noticed an error occuring for some of the courses. This error was traced back to the structure of the data; some rows in the course information tables had a table in them. As this occured in rows that were not relevant for the project, a function was added to identify and add only those tables with two columns. 

Finally, the newly created list of dictionaries was saved using the pickle module of python. This allowed us to access the information later while ensuring the same format. 

 4. Using the parsed information, creating a .ics file of the course timetable (spesific file: calendar_output.py)

- Describe your methodology and problem-solving strategies
- Clearly state what you developed and how (implementation)

Beautifulsoup package was used to parse this data into a meaningful dataframe. The parser makes a list of the data that was then modified to a dictionary object, as this was deemed more useful for the next steps of the project.

### 3.1. Design details

- Describe pre-existing resources and their origins
- Highlight additions or modifications made during the project

    *The original plan for this program was to provide a code that would automate the login, leading to the webscraping and calendar output creation process. However, multiple attempts revealed that this part was beyond the scope of this project due to issues related to two-factor-authentication and browser specifications. Thus, the goal was updated to include the remaining steps implemented on a HTML-document saved directly from UniPortal.*

- Use visuals such as drawings, screenshots, or plots to support your explanations

### 3.2. Results

- Explain what worked and what did not

    *As the login automation did not work for both of us despite extensive attempts, this part was deemed beyond the scope of this project and inessential for the main goal of the project. Thus, a revision was made to download the course information directly from UniPortal as a HTML document and implement the remaining steps from there.*

- Include relevant data, such as graphs, equations, or images, to illustrate results

## 4. Conclusion

- Recap what was accomplished and the key learnings from the project
- Identify aspects you would approach differently in hindsight
- Propose potential next steps or extensions for the project

## 5. References

- Provide a complete list of works and resources referenced during the project

https://www.selenium.dev/documentation/
https://github.com/mozilla/geckodriver 