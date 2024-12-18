# Project report

## 1. Introduction

- Provide a description of your program, including its purpose and functionality (scope and goal)
- Explain where and how the program is used (context)
- Discuss why the project is important
- Summarize the content and structure of the report

## 2. Background

- Outline prior research or projects relevant to your work, citing references as appropriate
- Discuss limitations or shortcomings in previous approaches
- Explain how your work improves upon or differs from existing solutions
- Provide any additional details necessary for understanding your project (context)

## 3. Project

- Describe your methodology and problem-solving strategies
- Clearly state what you developed and how (implementation)

### 3.1. Design details

-  Describe pre-existing resources and their origins
- Highlight additions or modifications made during the project

    *The original plan for this program was to provide a code that would automate the login, leading to the webscraping and calendar output creation process. However, multiple attempts revealed that this part was beyond the scope of this project due to issues related to two-factor-authentication and browser specifications. Thus, the goal was updated to include the remaining steps implemented on a HTML-document saved directly from UniPortal.*

- Use visuals such as drawings, screenshots, or plots to support your explanations

### 3.2. Results

- Explain what worked and what did not

    *The original plan was to automate the login process to UniPortal to allow a smooth process for the webscraping and calendar output creation. Attempts to create this feature were made using Selenium browser automation. However, due to the two-factor-login, this feature was deemed quite impractical, as the user would have to provide authenticator code each time they wanted to use the feature, which would make the automation pointless.*

    *To go around this issue, the next attempt  was to create a Selenium browser automation that could access a pre-existing browser window, where user had already completed the log-in process to UniPortal and subsequently automate the remaining steps. The reasoning for this step was that accessing an existing window would utilise saved cookies, therefore avoiding the problem of the two-factor authentication. The process involved use the browser's (Firefox) profiles-functionality and installation of the geckodriver. However, this attempt, too, was unsuccesful.* 
    
    *As these attempts to create the login automation had already involved multiple instances trying out variations of the code, reading documentation online and hours of work, this feature was deemed to be beoynd the scope of the project and inessential for the main goal of the project. Thus, a revision was made to download the course information directly from UniPortal as a HTML document and implement the remaining steps from there.*
- Include relevant data, such as graphs, equations, or images, to illustrate results

## 4. Conclusion

- Recap what was accomplished and the key learnings from the project
- Identify aspects you would approach differently in hindsight
- Propose potential next steps or extensions for the project

## 5. References

- Provide a complete list of works and resources referenced during the project

https://www.selenium.dev/documentation/
https://github.com/mozilla/geckodriver 