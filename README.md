Task Tracker Web App

# Overview
Task Tracker is a web-based productivity application built using Flask, SQLite, HTML, CSS, and Bootstrap. The goal of this project is to provide users with a simple and intuitive tool to create, manage, and complete daily tasks while tracking their progress. It includes user authentication, task creation, completion, and deletion features. Users can view incomplete and completed tasks separately, and the app displays a real-time summary of task completion statistics.

This project was built as part of the CS50 course’s final project to apply all the skills I’ve learned throughout the term, including templating with Jinja2, routing with Flask, managing user sessions, working with SQL databases, and implementing authentication and logic securely and cleanly.

# Features
User Registration and Login: Secure user authentication using password hashing with scrypt. Only registered users can access and manage their tasks.

## Task Creation
Users can add tasks with optional descriptions and due dates.

Task Completion
## Tasks can be marked as complete using a “✓ Complete” button, which updates the database and task counters.

## Task Deletion
Users can delete any of their tasks. If a completed task is deleted, the completed count is updated accordingly.

## Progress Summary
On both the home page and tasks view, users see a real-time count of completed tasks out of total tasks.

## Session Management
Ensures only logged-in users can access task-related routes and prevents unauthorized access.

## Input Validation
All forms include server-side validation, such as requiring non-empty fields and a password of at least 8 characters.

# File Structure and Description

## app.py
This is the core backend of the application, built with Flask. It defines all routes, handles session management, connects to the SQLite database using CS50’s SQL library, and processes all form data. Key routes include:

## /register
Handles new user registration and ensures passwords are hashed securely.

## /login
Authenticates users using stored hashes and logs them in by storing user_id in session.

## /logout
Clears the session to log the user out.

## /home
Displays incomplete tasks and shows a counter of completed vs total tasks.

## /create
Form to create new tasks.

## /complete/<int:task_id>
Marks a task as complete.

## /delete/<int:task_id>
Deletes a task from the database.

## /tasks
Displays both incomplete and completed tasks, along with statistics.

# Templates (.html files in the templates folder)

## layout.html
The base layout used across all pages. Includes the navigation bar and Bootstrap integration.

## index.html
The landing page. Provides a link to login or register.

## login.html
Form for users to log in. It uses Bootstrap for styling and provides flash messages for feedback.

## register.html
Form for new users to sign up. Validates password length and matches confirmation.

## home.html
Displays a table of all incomplete tasks and shows the number of completed out of total tasks.

## create.html
A simple form to add new tasks with optional description and due date.

## tasks.html
Shows both completed and incomplete tasks. Each task includes a button to complete or delete it.

# Design Decisions

## Authentication
Instead of storing passwords in plain text, I chose to use werkzeug.security’s generate_password_hash and check_password_hash to hash passwords using scrypt. When a user registers, their password is securely hashed and stored, and the same hash is verified during login. The use of scrypt is intentional—it is a secure password-based key derivation function and is appropriate for web applications.

## Route Protection
All task-related routes are protected by checking if "user_id" not in session: to ensure that unauthorized users are redirected to the login page. This simple but effective method secures the application and keeps user data private.

## Flash Messaging
To enhance the user experience, I included flash() messages throughout the app. These provide instant feedback to users, whether it’s for successful login, task creation, deletion, or errors in input.

## Task Statistics
I wanted users to not just manage tasks but also visualize their progress. That’s why I added a feature that counts and displays how many tasks have been completed out of the total. This is computed using SQL COUNT(*) queries and passed to the home.html and tasks.html templates.

# Conclusion
Building this task tracker has been a fulfilling way to consolidate the concepts I’ve learned in CS50—from Flask routing and session management to frontend templating and SQL queries. The application is user-friendly, secure, and offers enough features to be a practical daily tool for managing tasks. While there are opportunities for further enhancement (such as adding due date reminders or task categories), I am proud of what I’ve achieved and confident in how it demonstrates my understanding of full-stack web development.

# References
ChatGPT: https://chatgpt.com/
ChatGPT was used to assist in the development of the Task Tracker website.


