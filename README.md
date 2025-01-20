# Project UniCal

This code allows a student from University of Luzern to create a calendar file with their course schedule from their Uniportal account. The code works currently only for the German version of the site.

Instructions to use:

To successfully use this program, the user will need the scripts "reading_html.py", "calendar_output.py" and "main.py" from this repository.

1. User should create a folder on their computer and place the scripts there. Additionally, this folder should have a subfolder called "data". 

2. Using their login credentials, student should login to https://portal.unilu.ch/site/studierende/vorlesungen/anmeldungen.aspx and open their course schedule by clicking "Alle drucken". The now opening website should be saved (Ctrl + S or Command + S) as uniportal.html in the "data" subfolder. NOTE: the language in Uniportal should be set to German.

3. Running main.py will create the calendar file, unical.ics in the "data" subfolder. To access the course schedule, the user simply has to open the file in their calendar application of choice.

This project was realised for the course "Introduction to Computer Science and Programming" taught in University of Luzern, autumn semester of 2024. 
