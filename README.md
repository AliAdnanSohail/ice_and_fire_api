# Ice And Fire AP
 ## Summary
  Django Restframework Project to CRUD books from local database and retrieve books from external-api **Ice and Fire** on basis of name of book

## Prerequisite
 - Python3
 - Sqlite3
 - Django
 - virtualenv

## Project Setup
 - Clone this project
 - Go to ice_and_fire_api folder
 - Run `virtualenv --python=python3 venv` (to create new virtual machine)
 - Run `source venv/bin/activate`
 - Run `pip3 install --requirement requirements.txt` (to install all project dependencies)
 - Run `python3 manage.py migrate`
 - Run `python3 manage.py runserver` (to start server)
 - Go to http://localhost:8000/api/books/
 - Run `python3 manage.py test` (to run test cases

## Endpoint Details
API Documentation: https://documenter.getpostman.com/view/9493445/SW7W6q2f?version=latest
