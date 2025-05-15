# Django Expense Tracker – Development Log

## Stage 1: Initial Project Setup
- Create the project using the command `django-admin startproject config`
- Create an application named `expense` using the command `python manage.py startapp expenses`
- Add the application to `INSTALLED_APPS` in `settings.py`
- Run `python manage.py migrate` to create the initial SQLite database

## Stage 2: Create Expense model

Created an Expense model in expenses/models.py with the following fields:

- title: short description of the expense.
- amount: decimal value of the expense.
- category: choice field for categorizing the expense.
- date: date of the expense.
- user: ForeignKey to the logged-in user (one-to-many).

Applied migrations:
```python
python manage.py makemigrations tasks
python manage.py migrate
```
This creates the necessary database table to store Expense records.


🚀 Status: Project is on progress