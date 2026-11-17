# Examination Management Portal (MAD1 Project)

## Description
A role-based Examination Management System built with Flask and SQLite. It features different workflows for Admins, Examiners, and Students. Built using the MVC architecture and following strictly to a Zero-JavaScript constraint.

## Features
* **Admin:** Manage courses, create examinations, and approve examiner registrations.
* **Examiner:** Register for approval, create, and manage examination time slots.
* **Student:** Register, view available slots, and book examinations without overbooking.

## Tech Stack
* **Backend:** Python, Flask, Flask-SQLAlchemy, Flask-Login
* **Frontend:** Jinja2 Templates, Bootstrap 5, HTML5/CSS3
* **Database:** SQLite

## How to Run Locally
1. Clone the repository:
   `git clone https://github.com/24f2006584/examination-management-portal.git`
2. Create and activate a virtual environment:
   `python -m venv .venv`
   `source .venv/bin/activate` (Linux/Mac) OR `.venv\Scripts\activate` (Windows)
3. Install dependencies:
   `pip install -r requirements.txt`
4. Run the application:
   `python run.py`
